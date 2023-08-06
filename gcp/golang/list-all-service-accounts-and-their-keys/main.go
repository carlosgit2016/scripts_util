package main

import (
	"context"
	"encoding/csv"
	"io"
	"log"
	"os"
	"os/exec"
	"strings"

	admin "cloud.google.com/go/iam/admin/apiv1"
	"google.golang.org/api/cloudresourcemanager/v1"
	"google.golang.org/api/iterator"
	iampb "google.golang.org/genproto/googleapis/iam/admin/v1"
)

func check_commands(cmds []string) {
	for c := range cmds {
		_, err := exec.LookPath(cmds[c])
		if err != nil {
			log.Fatalf("Command not found %s", cmds[c])
		}
	}
}

func get_accesslog(kn string, sa string, proj string) (string, error) {
	cmd := exec.Command("./get_logs.sh", kn, sa, proj)

	log.Print(cmd.String())
	output, err := cmd.CombinedOutput()
	if err != nil {
		return "", err
	}

	return strings.TrimSpace(string(output)), nil
}

func main() {
	ctx := context.Background()

	lf, err := os.OpenFile("log.out", os.O_CREATE|os.O_WRONLY|os.O_APPEND, 0666)
	if err != nil {
		panic(err)
	}
	defer lf.Close()

	lf.Truncate(0) // cleanup
	out := io.MultiWriter(lf, os.Stdout)
	log.SetOutput(out)

	rmService, err := cloudresourcemanager.NewService(ctx)
	if err != nil {
		panic(err)
	}

	iamClient, err := admin.NewIamClient(ctx)
	if err != nil {
		panic(err)
	}

	file, err := os.Create("service_accounts.csv")
	if err != nil {
		panic(err)
	}
	defer file.Close()

	writer := csv.NewWriter(file)
	defer writer.Flush()

	writer.Write([]string{"project", "service_account", "key_id", "access_logs"})

	projectsReq := rmService.Projects.List()
	if err := projectsReq.Pages(ctx, func(page *cloudresourcemanager.ListProjectsResponse) error {
		for _, project := range page.Projects {
			serviceAccounts := iamClient.ListServiceAccounts(ctx, &iampb.ListServiceAccountsRequest{
				Name: "projects/" + project.ProjectId,
			})

			for {
				sa, err := serviceAccounts.Next()
				if err == iterator.Done {
					break
				}
				if err != nil {
					break
				}

				keysReq, err := iamClient.ListServiceAccountKeys(ctx, &iampb.ListServiceAccountKeysRequest{
					Name: sa.Name,
				})
				if err != nil {
					panic(err)
				}

				if keysReq == nil {
					log.Printf("No keys found for Service account %s", sa.DisplayName)
					continue
				}

				for _, key := range keysReq.Keys {
					if key.GetKeyType() != 1 {
						log.Printf("Service account %s do not contain any user managed key", sa.Email)
						continue
					}

					kns := strings.Split(key.Name, "/")
					kn := kns[len(kns)-1]
					accessLogs, err := get_accesslog(kn, sa.Email, project.ProjectId)
					if err != nil || accessLogs == "" || accessLogs == "[]" {
						log.Printf("No access logs found to %s \n %s", sa.Email, err.Error())
						accessLogs = "N/A"
					}

					line := []string{project.ProjectId, sa.Email, key.Name, accessLogs}
					log.Printf("\n===\n%s\n===\n", strings.Join(line, "\n"))
					writer.Write(line)
				}
			}
		}
		return nil
	}); err != nil {
		panic(err)
	}

	log.Printf("CSV file has been created")
}

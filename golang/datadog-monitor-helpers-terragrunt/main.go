package main

import (
	"context"
	"fmt"
	"os"
	"strings"

	datadog "github.com/DataDog/datadog-api-client-go/api/v1/datadog"
	"github.com/hashicorp/hcl/v2/gohcl"
	"github.com/hashicorp/hcl/v2/hclwrite"
)

type AdditionalTags struct {
	EstimatedUsage string `hcl:"estimated_usage"`
}

type Tags struct {
	Terraform string `hcl:"terraform"`
	Service   string `hcl:"service"`
}

// Monitor represents an individual Datadog monitor
type Monitor struct {
	Name              string         `hcl:"name,label"`
	Type              string         `hcl:"type"`
	WarningThreshold  *float64       `hcl:"warning_threshold"`
	CriticalThreshold *float64       `hcl:"critical_threshold"`
	AdditionalTags    AdditionalTags `hcl:"additional_tags,block"`
	Query             string         `hcl:"query"`
	Message           string         `hcl:"message"`
	SlackChannels     []string       `hcl:"slack_channels"`
}

// Inputs represents the root structure for Terraform inputs
type Inputs struct {
	Tags     Tags      `hcl:"tags,block"`
	Monitors []Monitor `hcl:"monitors,block"`
}

// Terraform represents the Terraform configuration
type Terraform struct {
	Source string `hcl:"source"`
}

// Include represents the include block for Terragrunt configuration
type Include struct {
	Name string `hcl:"name,label"`
	Path string `hcl:"path"`
}

func query() string {
	return "service:costs"
}

func getIngestedTag(monitor datadog.MonitorSearchResult) string {
	_, tag, _ := strings.Cut(monitor.Tags[0], "estimated_usage:")
	return tag
}

func getMonitorDetails(ctx context.Context, apiClient *datadog.APIClient, monitor datadog.MonitorSearchResult) datadog.Monitor {
	resp, r, err := apiClient.MonitorsApi.GetMonitor(ctx, *monitor.Id)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error when calling `MonitorsApi.GetMonitor`: %v\n", err)
		fmt.Fprintf(os.Stderr, "Full HTTP response: %v\n", r)
	}

	return resp
}

func main() {
	ctx := datadog.NewDefaultContext(context.Background())
	configuration := datadog.NewConfiguration()
	apiClient := datadog.NewAPIClient(configuration)

	query := query()
	params := datadog.SearchMonitorsOptionalParameters{Query: &query}
	resp, r, err := apiClient.MonitorsApi.SearchMonitors(ctx, params)

	if err != nil {
		fmt.Fprintf(os.Stderr, "Error when calling `MonitorsApi.SearchMonitors`: %v\n", err)
		fmt.Fprintf(os.Stderr, "Full HTTP response: %v\n", r)
	}

	var monitors []Monitor = []Monitor{}

	for _, monitor := range resp.Monitors {

		monitor_details := getMonitorDetails(ctx, apiClient, monitor)

		monitors = append(monitors, Monitor{
			Name:              *monitor.Name,
			Type:              string(*monitor.Type),
			Query:             monitor.GetQuery(),
			WarningThreshold:  monitor_details.GetOptions().Thresholds.Warning.Get(),
			CriticalThreshold: monitor_details.GetOptions().Thresholds.Critical,
			AdditionalTags: AdditionalTags{
				EstimatedUsage: getIngestedTag(monitor),
			},
			Message:       *monitor_details.Message,
			SlackChannels: []string{"mobility-finops-datadog"},
		})
	}

	hcl := Inputs{
		Monitors: monitors,
	}

	f := hclwrite.NewEmptyFile()
	gohcl.EncodeIntoBody(&hcl, f.Body())

	err = os.WriteFile("test.hcl", f.Bytes(), os.ModePerm)
	if err != nil {
		fmt.Fprint(os.Stderr, err)
	}
}

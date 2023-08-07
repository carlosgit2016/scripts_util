# Service accounts user managed keys lookup

In order to map GCP service account user managed keys you can use this golang script to scan and save the info of all projects

This golang script located at `main.go` is inteded to list all USER_MANAGED keys in all service accounts of all projects and save in a csv file `service_accounts.csv` containing `project, service_account, key_id, last_access_log`

## Usage

### Pre-requisites
- Using Linux
- bash
- gcloud
- logged in gcloud using `gcloud auth login` or equivalent
- jq

```
# saEmail, the service account email to check, it could be a substring
# csvFile, the file to save the output result
go run main.go <sa-email> <csvFile>
# A new file will be created named service_accounts.csv
```

### Improvements
- Add projects filter
- Add regex support argument for projects (e.g. `*-prod-*`)
- Add regex support argument for service accounts (e.g. `preffix-*`)
- Move `get_logs.sh` code to inside golang code and remove the script
# List containers in a storage account
az storage container list --account-name "<storage_account>" -o table

# List blob that given container
az storage blob list --container-name "<container_name>" --account-name "<storage_account>" -o table

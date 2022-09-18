# Filter key vault by name 
az keyvault list -o yaml --query "[?name=='<keyvault-name>']"

# Download keyvault secret
az keyvault secret download --encoding utf-8 --file <filename> --name <secret-name> --vault-name <vault-name>

# List keyvault secrets
az keyvault secret list --vault-name <kevault-name> | jq  -r '.[] | {name}'
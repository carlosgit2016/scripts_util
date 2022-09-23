# Filter key vault by name 
az keyvault list -o yaml --query "[?name=='<keyvault-name>']"

# Download keyvault secret
az keyvault secret download --encoding utf-8 --file <filename> --name <secret-name> --vault-name <vault-name>

# List keyvault secrets
az keyvault secret list --vault-name <kevault-name> | jq  -r '.[] | {name}'

# Check for images in a x repository that contains a 'y' name
az acr repository list -n <x> --query "[?contains(@, '<y>')]" | jq '.'

# Set secrets per environment
set_secret(){
    local env="$1"
    local vault="$2"
    local key="$3"
    local secret="$4"

    az keyvault secret set -n "$env-<suffix>" --vault-name $vault --description "<desc>" --value $key
}

set_secret dev <vault-name> <key> <secret>
set_secret staging <vault-name> <key> <secret>
set_secret prod <vault-name> <key> <secret>
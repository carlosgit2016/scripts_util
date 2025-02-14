#!/bin/bash

set -exo pipefail

SUBSTRING="$1"
FILE="$(uuidgen)-output.csv"
GROUPS_CACHE="groups_cache"

if [ ! -e "$GROUPS_CACHE" ]; then
    az ad group list --query "[?contains(displayName, '$SUBSTRING')].{displayName:displayName}" -otsv > "$GROUPS_CACHE"
fi

groups=$(cat "$GROUPS_CACHE")

echo "group,members" > "$FILE"

for g in $groups; do
    line="$g,"
    members=$(az ad group member list -g "$g" -ojson | jq -r '.[].mail' | tr "\n" ";")
    line+="$members,"
    echo "$line"
    echo "$line" >> "$FILE"
done


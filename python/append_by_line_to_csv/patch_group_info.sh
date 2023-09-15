#!/bin/bash

# Given a patch group, describe the details, maintenance window and the last executions

set -eo pipefail

PATCH_GROUP="$1"

echo "Patch group Details"
aws ssm describe-patch-groups --filters "Key=NAME_PREFIX, Values=$PATCH_GROUP" | yq -P '.Mappings[0]'
echo
echo
echo "Maintenance Window"
aws ssm describe-maintenance-windows-for-target --targets "Key=tag:Patch Group, Values=$PATCH_GROUP" --resource-type "INSTANCE" | jq -r '.WindowIdentities[].Name' | xargs -I {} /bin/bash -c 'aws ssm describe-maintenance-windows --filters "Key=Name, Values={}" | yq -P ".WindowIdentities";echo;echo'

echo
echo

echo "States of last execution per instance"
aws ssm describe-instance-patch-states-for-patch-group --patch-group "$PATCH_GROUP" | yq -P '.'

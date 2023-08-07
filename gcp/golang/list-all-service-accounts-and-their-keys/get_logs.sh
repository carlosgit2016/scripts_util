#!/bin/bash

set -eo pipefail

KEY_NAME="$1"
SA_EMAIL="$2"
PROJECT="$3"

# Loading asdf in case exists
if [ -f "$HOME/.asdf/asdf.sh" ]; then
    source "$HOME/.asdf/asdf.sh"
fi

gcloud logging read "protoPayload.authenticationInfo.principalEmail=$SA_EMAIL" --project="$PROJECT" --format=json --freshness=30d|  jq -r "[.[] | \
    select(.protoPayload.authenticationInfo.serviceAccountKeyName | contains(\"$KEY_NAME\"))][0] | \
    \"lastAccessData: \(.protoPayload.requestMetadata.requestAttributes.time) who: \(.protoPayload.requestMetadata.callerIp)\""
#!/bin/bash

set -euo pipefail

keys='''
<...>
KEYS
<...>
'''


function main(){
   for key in $keys; do
        local k
        local sa
        local project
        k=$(echo -n "$key" | cut -d'/' -f6)
        sa=$(echo -n "$key" | cut -d'/' -f4)
        project=$(echo -n "$key" | cut -d'/' -f2)

        gcloud iam service-accounts keys disable "$k" --iam-account="$sa" --project="$project"
    done
}


main

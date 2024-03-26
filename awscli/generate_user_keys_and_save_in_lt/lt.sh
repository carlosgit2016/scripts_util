#!/bin/bash

function main(){
    local user="$1"
    local data="$2"

    secure_note_name="$user-key-$(date '+%m-%d-%Y')"
    lpass add --sync=now --non-interactive --notes "Shared-ttm-keyrotation/$secure_note_name"<<<"$data"
    echo "Secure note added $secure_note_name"
}

set -eo pipefail
main "$@"

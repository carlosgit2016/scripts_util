#!/bin/bash

set -e

PORT="28082"
BASE_URL="localhost:${PORT:-28082}"

request() {
    local path=$1
    shift 1
    curl -Ls -H 'Content-Type: application/json' "$BASE_URL/$path" "$@"
}

create_port_forward() {
    local namespace=$1
    local svc_name=$2
    kubectl port-forward "-n$namespace" "svc/$svc_name" $PORT
}

list() {
    request "connectors" "$@"
}

status() {
    local connector_name=$1
    shift 1
    request "connectors/$connector_name/status" "-X" "GET" "$@"
}

delete() {
    local connector_name=$1
    shift 1
    request "connectors/$connector_name" "-X" "DELETE" "$@"
}

create() {
    local config_path=$1
    shift 1
    request "connectors" "-X" "POST" -d "@$config_path" "$@"
}

get_connector() {
    local connector_name=$1
    shift 1    
    request "connectors/$connector_name" "$@"    
}

get_error() {
    # Get trace error of the first task of a connector
    local connector_name=$1
    shift 1    
    request "connectors/$connector_name/status" "$@" | jq -r '.tasks[0].trace'
}

validate_connect_config() {
    local config_path=$1
    local connector_type=$2
    shift 2
    request "connector-plugins/$connector_type/config/validate" -X PUT -d "@$config_path" "$@"
}

main() {
    local command=$1
    shift 1

    "$command" "$@"
}

main "$@"

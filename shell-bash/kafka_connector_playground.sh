# Open port k8s forward
kubectl port-forward -ndev <svc-name>

# Return status of each connector within the kafka connect
curl -Ls localhost:28082/connectors | jq -r '.[]' | xargs -I '_' curl -Ls localhost:28082/connectors/_/status | jq -r '.tasks[0].trace'


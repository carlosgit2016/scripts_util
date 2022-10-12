# Validate connectors config
curl -Lsv -X PUT -d @<connector-config>.json  -H 'Content-Type: application/json' localhost:28082/connector-plugins/<connector-type>/config/validate | jq '.'

# Create connector 
curl -Ls -X POST -d @<connector-config>.json -H "Content-Type: application/json" localhost:28082/connectors | jq '.' 

# Check connector status
curl -Ls localhost:28082/connectors/<connector>/status

# Check connector configs
curl -Ls localhost:28082/connectors/<connector> | jq '.'

# Delete connector
curl -Lsv -X DELETE localhost:28082/connectors/<connector>

## List all connectors status
## List all tasks traces to find errors 
curl -Ls localhost:28082/connectors | jq -r '.[]' | xargs -I '_' curl -Ls localhost:28082/connectors/_/status | jq '.'
curl -Ls localhost:28082/connectors | jq -r '.[]' | xargs -I '_' curl -Ls localhost:28082/connectors/_/status | jq -r '.tasks[0].trace'

# get configs of the first connector
curl -Ls localhost:28082/connectors | jq -r '.[]' | head -n1 | xargs -I '_' curl -Ls localhost:28082/connectors/_ | jq '.'
 
# get trace error of the first task of a connector
curl -Ls localhost:28082/connectors/<connector>/status | jq -r '.tasks[0].trace'

# watch for errors in connector 
watch -n 2 "curl -Ls localhost:28082/connectors/alpha-eld-rabbitmq-source-connector-hours-of-service-created/status | jq -r '.'"

# Create a topic
kafka-topics --create --bootstrap-server localhost:9092 --topic "mytopic.test.0" 

# Producing a message to the topic
cat payload.json | tr -d '\n' | kafka-console-producer.sh --bootstrap-server pkc-4k6zp.eastus2.azure.confluent.cloud:9092 --topic pubsub.connector.test.0 --property key.separator=,


cat one_line_cloud_event.json | kafka-console-producer --producer.config /home/cflor/.kafka-tools/config --broker-list pkc-4k6zp.eastus2.azure.confluent.cloud:9092 --topic sample-topic --property parse.key=true --property key.separator=,
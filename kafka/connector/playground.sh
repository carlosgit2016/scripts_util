# Validate connectors config
curl -Lsv -X PUT -d @<connector-config>.json  -H 'Content-Type: application/json' localhost:28082/connector-plugins/<connector-type>/config/validate | jq '.'

# Create connector 
curl -Ls -X POST -d @<connector-config>.json -H "Content-Type: application/json" localhost:28082/connectors | jq '.' 

# Check connector status
curl -Ls "localhost:28082/connectors/$CONNECTOR/status"

# Check connector configs
curl -Ls "localhost:28082/connectors/$CONNECTOR" | jq '.'

# Delete connector
curl -Lsv -X DELETE "localhost:28082/connectors/$CONNECTOR"

## List all connectors status
## List all tasks traces to find errors 
curl -Ls localhost:28082/connectors | jq -r '.[]' | xargs -I '_' curl -Ls localhost:28082/connectors/_/status | jq '.'
curl -Ls localhost:28082/connectors | jq -r '.[]' | xargs -I '_' curl -Ls localhost:28082/connectors/_/status | jq -r '.tasks[0].trace'

# get configs of the first connector
curl -Ls localhost:28082/connectors | jq -r '.[]' | head -n1 | xargs -I '_' curl -Ls localhost:28082/connectors/_ | jq '.'
 
# get trace error of the first task of a connector
curl -Ls "localhost:28082/connectors/$CONNECTOR/status" | jq -r '.tasks[0].trace'

# watch for errors in connector 
watch -n 2 "curl -Ls localhost:28082/connectors/alpha-eld-rabbitmq-source-connector-hours-of-service-created/status | jq -r '.'"

# Create a topic
kafka-topics --create --bootstrap-server localhost:9092 --topic "mytopic.test.0" 

# Producing a message to the topic
cat payload.json | tr -d '\n' | kafka-console-producer.sh --bootstrap-server pkc-4k6zp.eastus2.azure.confluent.cloud:9092 --topic pubsub.connector.test.0 --property key.separator=,

## Using Kafka Facilitator 
# List connectors 
./kfconnect.sh list | jq '.'

# Check connector status
./kfconnect.sh status "dev-sink-pubsub-compliance-recordofdutystatus-qry" | jq '.'

# Validating config
./kfconnect.sh validate_connect_config "dev-sink-pubsub-compliance-recordofdutystatus-qry.config.json" CloudPubSubSinkConnector | jq '.'

# Create port forward
./kfconnect.sh create_port_forward dev tcx-eldkafkaconnect


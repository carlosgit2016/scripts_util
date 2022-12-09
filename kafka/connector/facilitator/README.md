## Kafka Connect facilitator

### Configure

```sh
git clone ssh://git@bitbucket.trimble.tools/pnet-platform/end-to-enders-tools.git $HOME/.end-to-enders-tools
echo "export PATH=\$PATH:$HOME/.end-to-enders-tools/kafka" >> ~/.zshrc
source $HOME/.zshrc
```

### Examples

```sh
# Create port forward
kfconnect create_port_forward dev tcx-eldkafkaconnect

# List connectors 
kfconnect list | jq '.'

# Get connector config 
kfconnect get_connector dev-sink-pubsub-compliance-recordofdutystatus-qry | jq '.'

# Create connector
kfconnect create_connector dev-sink-pubsub-compliance-recordofdutystatus-qry.json -v

# Delete connector
kfconnect delete_connector dev-sink-pubsub-compliance-recordofdutystatus-qry -v

# Get trace error of the first task of a connector
kfconnect get_error dev-sink-pubsub-compliance-recordofdutystatus-qry

# Check connector status
kfconnect status "dev-sink-pubsub-compliance-recordofdutystatus-qry" | jq '.'

# Validating config
kfconnect validate_connect_config "dev-sink-pubsub-compliance-recordofdutystatus-qry.config.json" CloudPubSubSinkConnector | jq '.'
```
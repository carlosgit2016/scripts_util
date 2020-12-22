TABLE_NAME="<table_name>" 
LOCKID_LIKE="<lockid>" # It can be any string
KEY_FILE="key.json"

aws dynamodb scan \
              --table-name $TABLE_NAME \
              --filter-expression 'contains(LockID,:lockid)' \
              --expression-attribute-values "{\":lockid\":{\"S\":\"$LOCKID_LIKE\"}}" --select SPECIFIC_ATTRIBUTES --projection-expression "LockID" > $KEY_FILE
cat $KEY_FILE | jq -r ".Items[] | tojson" | tr '\n' '\0' | xargs -0 -I keyItem aws dynamodb delete-item --table-name $TABLE_NAME --key=keyItem


# It will exlude the specific item in a state lock table created by terraform.

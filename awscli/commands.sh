# Filter instances by tag Name
aws ec2 describe-instances --filters "Name=tag:Name, Values=<name>" | jq '.Reservations'

# Get parameter from parameter store from a specific path and query their value
aws ssm get-parameter --name "<path>" --with-decryption --query 'Parameter.Value' --output text

# List all bucket with the human redable option
aws s3 ls --human-readable

# Get parameters recursively by path and filter their Name / ARN and Value
aws ssm get-parameters-by-path --path '<prefix_path>' --with-decryption --recursive | jq '.Parameters[] | {Name, ARN,Value}'

# Describe all target groups in a specific load balancer using a preffix
local preffix="preffix"
aws elbv2 describe-load-balancers --query="LoadBalancers[?contains(LoadBalancerName, '$preffix')].LoadBalancerArn" | jq -r '.[]' | xargs -I "{}" aws elbv2 describe-target-groups --load-balancer-arn "{}" | jq '.'

# Describe if the targets in those target groups are healthy
aws elbv2 describe-load-balancers --query="LoadBalancers[?contains(LoadBalancerName, '$preffix')].LoadBalancerArn" | jq -r '.[]' | xargs -I "{}" aws elbv2 describe-target-groups --load-balancer-arn "{}" | jq -r '.TargetGroups[].TargetGroupArn' | xargs -I "{}" aws elbv2 describe-target-health --target-group-arn "{}" | jq '.TargetHealthDescriptions[]'
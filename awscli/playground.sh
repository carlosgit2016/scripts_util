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

# Describe instances filtering by tag name 
aws ec2 describe-instances --filters "Name=tag:<tag-name>, Values=<value>" --query "Reservations[*].Instances[?contains(Tags[?Key == 'Name'].Value, 'qa_compliance_ad_web')]" | jq '.[]'

# Describe instances health from classic lb
aws elb describe-instance-health --load-balancer-name <lb-name>

# Copy LC
## Describe LC based on some string in their name
aws autoscaling describe-launch-configurations --query="LaunchConfigurations[?contains(LaunchConfigurationName, '<some-name>')]" | jq '.'

## Create LC using a JSON as input
aws autoscaling create-launch-configuration --cli-input-json "$(cat < lc.json | tr -d '\n')"

# Copy existent ASG

## Create new autoscaling based on a json file
aws autoscaling create-auto-scaling-group --cli-input-json "$( cat asg.json | tr -d '\n'  )"

## Watch autoscaling instances lifecycle 
watch -n2 "aws autoscaling describe-auto-scaling-groups --auto-scaling-group-names <name> | jq '.AutoScalingGroups[].Instances[].LifecycleState'"

## Get all instances and execute a command 
## Using userdata logs 
aws autoscaling describe-auto-scaling-groups --auto-scaling-group-names <name> | jq -r '.AutoScalingGroups[].Instances[].InstanceId' | paste -sd "," - | xargs -I "{}" aws-ssm-cmd -i "{}" -s pwsh -o outputs "Get-Content C:\ProgramData\Amazon\EC2-Windows\Launch\Log\UserdataExecution.log"

# Update assume role policy for a specific role
## Get existent assume role policy
aws iam get-role --role-name "<role>" | jq '.Role.AssumeRolePolicyDocument' > PackerServicePolicy.json
## Update assume role policy
aws iam update-assume-role-policy --role-name '<role>' --policy-document file://PackerServicePolicy.json
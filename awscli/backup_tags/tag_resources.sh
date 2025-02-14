#!/bin/bash

rds_instances='''
'''

vpc_ids='''
'''

instances='''
'''

volumes='''
'''

function check_login() {
    echo "Checking AWS login..."
    aws sts get-caller-identity | jq -r '.Account'
}

function tag_ebs() {
    echo "Adding backup=no to EBS volumes..."
    for vol in $volumes; do
        echo "Adding tag to $vol"
        aws ec2 create-tags --resources "$vol" --tags Key=backup,Value=no
    done
    echo "EBS tagging complete."
}

function tag_ec2() {
    echo "Adding backup=no to EC2 instances..."
    for instance in $instances; do
        echo "Adding tag to $instance"
        aws ec2 create-tags --resources "$instance" --tags Key=backup,Value=no
    done
    echo "EC2 tagging complete."
}

function tag_rds() {
    for rds in $rds_instances; do
        echo aws rds add-tags-to-resource --resource-name "arn:aws:rds:us-east-1:831572230272:db:$rds" --tags Key=backup,Value=no
    done
    echo "RDS tagging complete."
}

function tag_vpc() {
    echo "Adding backup=no to VPCs..."
    xargs -I {} aws ec2 create-tags --resources {} --tags Key=backup,Value=no <<<"$vpc_ids"
}

function list_vpc() {
    echo "Listing all VPCs..."
    xargs -I {} aws ec2 describe-vpcs --vpc-ids {} <<<"$vpc_ids"
}

function list_ec2_vpc() {
    echo "Listing unique VPCs from EC2 instances..."
    echo "$instances" | tr '\n' ' ' | xargs -I {} echo aws ec2 describe-instances --instance-ids {} --query 'reservations[0].instances[0].vpcid' --output text
}

function main() {
    check_login
    action="$1"
    if [ -n "$action" ]; then
        shift
        "$action" "$@"
    else
        echo "Usage: $0 <action>"
        echo "Available actions: tag_ebs, tag_ec2, tag_rds, tag_vpc, list_vpc, list_ec2_vpc"
    fi
}

set -eo pipefail

main "$@"

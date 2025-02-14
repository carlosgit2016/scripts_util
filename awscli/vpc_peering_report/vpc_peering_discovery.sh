#!/bin/bash

accounts='''
account1
'''

echo "account,requester_accountid,requester_vpcid,requester_cidr,accepter_accountid,accepter_vpcid,accepter_cidr,status,tags"

for a in $accounts; do
    saml2aws login --skip-prompt --skip-verify -p "$a" -a "$a" --username username --password "password" > /dev/null
    export AWS_PROFILE="$a"
    export AWS_REGION="us-east-1"
    echo -n "$a"
    aws ec2 describe-vpc-peering-connections --output yaml | yq '.VpcPeeringConnections[]? | ",\(.RequesterVpcInfo.OwnerId),\(.RequesterVpcInfo.VpcId),\(.RequesterVpcInfo.CidrBlock),\(.AccepterVpcInfo.OwnerId),\(.AccepterVpcInfo.VpcId),\(.AccepterVpcInfo.CidrBlock),\(.Status.Message),\([.Tags[] | \"\(.Key)=\(.Value)\"] | join(\" \"))"'
done

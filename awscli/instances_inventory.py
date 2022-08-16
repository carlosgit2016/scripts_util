# %%
import json
import boto3
import os
import tempfile

os.environ['AWS_PROFILE'] = 'prod-admin'
os.environ['REGION'] = 'us-east-1'


client = boto3.client('ec2')

response = client.describe_instances(
    Filters=[
        {
            'Name': 'tag:product',
            'Values': [
                'ttm:compliance',
            ]
        },
    ],
    MaxResults=1000
)

# %%

import tempfile

def extend_instances(response):
    reservations = response['Reservations'] 
    instances = []
    for r in reservations:
        if 'Instances' in r:
            instances.extend(r['Instances'])    
    return instances

def retrieve_volumes(vols_ids):
    res = client.describe_volumes(
        VolumeIds=vols_ids
    )

    return res['Volumes']

def calc_total_vols_usage(vols):

    t_storage = 0
    for v in vols:
        t_storage+=v['Size']

    return {
        "total_storage" : t_storage
    }

def map_instance_to_csv(i):
    vols_ids = list(map(lambda b: b["Ebs"]["VolumeId"], i["BlockDeviceMappings"]))
    volumes = retrieve_volumes(vols_ids)
    vols_data = calc_total_vols_usage(volumes)

    name = list(filter(lambda tag: tag["Key"] == "Name", i["Tags"]))[0]["Value"]
    environment = list(filter(lambda tag: tag["Key"] == "environment", i["Tags"]))[0]["Value"]
    total_storage = vols_data["total_storage"]
    instance_type = i["InstanceType"]
    vpc_id = i["VpcId"]

    return f'{name},{instance_type},{environment},{vpc_id},{total_storage} GB\n'

header = ["Name", "InstanceType","Environment" ,"VPC ID", "Storage size"]
tmpfile = tempfile.NamedTemporaryFile('wt', delete=False, prefix='peoplenet-production', suffix='.csv')
lines = []
lines.append(f'{",".join(header)}\n')
instances = extend_instances(response)
lines.extend(list(map(map_instance_to_csv, instances)))
with tmpfile as f:
    f.writelines(lines)

print(tmpfile.name)

# %%
'''
To JSON
'''
def map_instance(instance):
    i = instance["Instances"][0]
    return {
        "InstanceType": i["InstanceType"],
        "BlockDeviceMappings": list(map(lambda b: {"ebs_volume_id": b["Ebs"]["VolumeId"]} ,i["BlockDeviceMappings"])),
        "VpcId": i["VpcId"],
        "Name": list(filter(lambda tag: tag["Key"] == "Name", i["Tags"]))[0]["Value"]
    }

mapped_instances = list(map(map_instance , response["Reservations"]))




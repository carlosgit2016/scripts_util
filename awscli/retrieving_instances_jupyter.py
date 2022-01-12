# %%
'''
    Describe instances with the filter that should be defined in filters function and map the result with the selector function.
'''
import os
import boto3

os.environ['AWS_PROFILE'] = '<region>'
os.environ['REGION'] = 'us-east'


def extend_instances(response):
    reservations = response['Reservations']
    instances = []
    for r in reservations:
        if 'Instances' in r:
            instances.extend(r['Instances'])
    return instances


def get_instance_name(image):
    return list(filter(lambda t: t['Key'] == 'Name', image['Tags']))[0]['Value']

def filters():
    '''
        e.g.
        [
            {
                'Name': 'tag:<tag_name>',
                'Values': [
                    '<tag_value>',
                    '<tag_value>',
                    '<tag_value>',
                    '<tag_value>'
                ]
            }
        ]
    '''
    return []

def selector(instance):
    '''
        e.g. 'ip': instance['PrivateIpAddress'], 'name': get_instance_name(i), return the name and the private IPs of the instance
    '''

    return {'name': get_instance_name(instance), 'ami': instance['ImageId'], 'instance_type': instance['InstanceType'], 'instance_id': instance['InstanceId']}

client = boto3.client('ec2')

response = client.describe_instances(Filters=filters())
target_instances = extend_instances(response)

mapped_instances = list(map(selector, target_instances))
print(mapped_instances)

# %%
# YAML serializing 
import yaml

mapped_instances.sort(key=lambda e: e['name'])

print(yaml.dump(mapped_instances))

# %%
print(len(mapped_instances))
# %%

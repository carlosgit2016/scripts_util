'''
    Describe instances with the filter that should be defined in filters function and map the result with the selector function.
'''
import os
import boto3

os.environ['AWS_PROFILE'] = '<AWS_PROFILE>'
os.environ['REGION'] = '<region>'


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
                    '<tag_value>'
                ]
            }
        ]
    '''
    return []

def selector(instance):
    '''
        e.g. 'ip': i['PrivateIpAddress'], 'name': get_instance_name(i), return the name and the private IPs of the instance
    '''
    return instance

def run():
    client = boto3.client('ec2')

    response = client.describe_instances(Filters=filters())

    target_instances = extend_instances(response)
    mapped_instances = list(map(selector, target_instances))
    print(mapped_instances)


if __name__ == '__main__':
    run()
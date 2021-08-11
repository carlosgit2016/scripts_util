'''
'''
import os
import boto3

os.environ['AWS_PROFILE'] = 'prod-admin'
os.environ['REGION'] = 'us-east-1'

client = boto3.client('ec2')

def extend_instances(response):
    reservations = response['Reservations'] 
    instances = []
    for r in reservations:
        if 'Instances' in r:
            instances.extend(r['Instances'])    
    return instances

def mapper(i):
    tags = i['Tags']
    tag_name = list(filter(lambda t: t['Key'] == 'Name',tags))[0]['Value']
    return {'instance_name': tag_name, 'ami_id': i['ImageId']}

def source_ami_id_mapper(i):
    source_ami_id_tag = list(filter(lambda t: t['Key'] == 'source-ami-id', i['Tags']))[0]
    return source_ami_id_tag['Value']

def get_ami_name(image):
    return list(filter(lambda t: t['Key'] == 'Name', image['Tags']))[0]['Value']

def get_ami_source_name(image):
    return list(filter(lambda t: t['Key'] == 'source-ami-name', image['Tags']))[0]['Value']

def get_source_images(images):
    return list(map(source_ami_id_mapper, images))

def describe_images(image_ids):
    return client.describe_images(
        ImageIds=image_ids
    )['Images']

def instances_state(instances_ids):
    instances = []
    for instance_id in instances_ids:
        response = client.describe_instances(
            InstanceIds=[instance_id]
        )

        target_instance = extend_instances(response)
        mapped_image_id = list(map(mapper, target_instance))[0]

        try:

            target_image = describe_images([mapped_image_id['ami_id']])
            target_ami_name = get_ami_name(target_image[0])
            source_efs_base_image = get_source_images(target_image)
            efs_base_image = describe_images(source_efs_base_image)
            efs_base_image_name = get_ami_name(efs_base_image[0])
            source_windows_image = get_source_images(efs_base_image)
            windows_base_image = describe_images(source_windows_image)
            windows_image_name = get_ami_name(windows_base_image[0])
            aws_image_name = get_ami_source_name(windows_base_image[0])

            instances.append({
                'instance_name': mapped_image_id['instance_name'],
                'ami_name': target_ami_name,
                'source_efs_base_ami_name': efs_base_image_name,
                'source_efs_windows_ami_name': windows_image_name,
                'aws_image_name': aws_image_name
            })

        except:
            print(f'Image not found for {get_ami_name(target_instance[0])}')
    
    return instances

response = client.describe_instances(
    Filters=[
        {
            'Name': 'tag:product',
            'Values': [
                'ttm:compliance'
            ]
        },
        {
            'Name': 'tag:environment',
            'Values': [
                'prod'
            ]
        }
    ]
)

instances = extend_instances(response)
instances_ids = map(lambda i: i['InstanceId'], instances)
print(instances_state(instances_ids))
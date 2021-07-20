'''
    Update one or more parameters at once
'''
import boto3
import os

path = '/some/path'
value = 'some_value'

# Login in first to load your profile or provide other environment variables
os.environ['AWS_PROFILE'] = "some_profile"
os.environ['AWS_REGION'] = "us-east-1"

client = boto3.client("ssm")

response = client.get_parameters_by_path(
    Path=path,
    Recursive=True,
    WithDecryption=True
)

parameters = response['Parameters']

for p in parameters:
    print(f'Parameter to be updated {p['Name']}')
    response = client.put_parameter(
        Name=p['Name'],
        Value=value,
        Overwrite=True
    )

    print(response)

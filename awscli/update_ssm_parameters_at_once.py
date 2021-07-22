'''
    Update one or more parameters at once
'''
import boto3
import os

PARAMETERS_PATH = '/some/path'
VALUE_TO_UPDATE = 'some_value'

def run():
    # Login in first to load your profile or provide other environment variables
    os.environ['AWS_PROFILE'] = "some_profile"
    os.environ['AWS_REGION'] = "us-east-1"
    
    client = boto3.client("ssm")
    parameters = []
    next_token = None
    
    
    while True:
    
        kwargs = {
            'Path':PARAMETERS_PATH,
            'Recursive':True,
            'WithDecryption':True
        }
    
        if next_token != None:
            kwargs.update({'NextToken': next_token})

        response = client.get_parameters_by_path(**kwargs)
        parameters.extend(response['Parameters'])
        if 'NextToken' not in response:
            break
        
        next_token = response['NextToken']
    
    for p in parameters:
        print(f'Parameter to be updated {p["Name"]}')
        response = client.put_parameter(
            Name=p['Name'],
            Value=VALUE_TO_UPDATE,
            Overwrite=True
        )
    
        print(response)



if __name__ == "__main__":
    run()
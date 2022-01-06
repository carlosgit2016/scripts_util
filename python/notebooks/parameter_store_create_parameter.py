# %%
'''
    Create parameters 
'''
import boto3
import os



def run():
    
    # Login in first to load your profile or provide other environment variables
    os.environ['AWS_PROFILE'] = "some_profile"
    os.environ['AWS_REGION'] = "us-east-1"
    
    client = boto3.client("ssm")

    environments = ['alpha', 'dev', 'qa', 'qa-2']
    parameters = [
        {
            'name': '/<env>/efs/ttc/session/dvir/key_id',
            'description': 'TTC credential key id for dvir api',
            'value': 'key',
            'type': 'SecureString',
            'key_id': ''
        },
        {
            'name': '/<env>/efs/ttc/session/dvir/key_secret',
            'description': 'TTC credential key secret for dvir api',
            'value': 'secret',
            'type': 'SecureString',
            'key_id': ''
        },
        {
            'name': '/<env>/efs/ttc/api_base_url',
            'description': 'TTC base URL',
            'value': '',
            'type': 'String'
        }
    ]

    for e in environments:
        for p in parameters:
            # Need to be adjusted
            parameter = p.replace('<env>', e)
            response = client.put_parameter(
                Name='parameter',
                Description='string',
                Value='string',
                Type='String'|'StringList'|'SecureString',
                KeyId='string',
                Overwrite=True|False,
                AllowedPattern='string',
                Tags=[
                    {
                        'Key': 'string',
                        'Value': 'string'
                    },
                ],
                Tier='Standard'|'Advanced'|'Intelligent-Tiering',
                Policies='string',
                DataType='string'
            )
# %% 
environments = ['alpha', 'dev', 'qa', 'qa-2']
for e in environments:
    print(f'aws ssm put-parameter --name /{e}/efs/ttc/session/dvir/key_id --value "46748174eadB03C05eA6Ee5711e1303" --description "TTC credential key id for dvir api" --type SecureString --key-id <key-id>')
# %%
for e in environments:
    print(f'aws ssm put-parameter --name /{e}/efs/ttc/session/dvir/key_secret --value "e3b61793d5B5915F4418E81A0Ed530e" --overwrite')
# %%
for e in environments:
    print(f'aws ssm put-parameter --name /{e}/efs/ttc/api_base_url --value "https://cloud.dev.api.trimblecloud.com" --description "TTC Base URL" --type String')
# %%


## Some result
'''
# Adding keys

aws ssm put-parameter --name /alpha/efs/ttc/session/dvir/key_id --value "<sensitive_key>" --description "TTC credential key id for dvir api" --type SecureString --key-id c42964a1-ed4e-42ad-bbb4-83c262462539
aws ssm put-parameter --name /dev/efs/ttc/session/dvir/key_id --value "<sensitive_key>" --description "TTC credential key id for dvir api" --type SecureString --key-id 0ffbeaa5-1280-4149-9004-74202e31ee1a
aws ssm put-parameter --name /qa/efs/ttc/session/dvir/key_id --value "<sensitive_key>" --description "TTC credential key id for dvir api" --type SecureString --key-id 31b21206-9023-4ce6-a57d-56cc88701d1c
aws ssm put-parameter --name /qa-2/efs/ttc/session/dvir/key_id --value "<sensitive_key>" --description "TTC credential key id for dvir api" --type SecureString --key-id f555e8a0-c41e-4c6a-82d2-90e82ecaef57

# Adding secrets

aws ssm put-parameter --name /alpha/efs/ttc/session/dvir/key_secret --value "<sensitive_key>" --description "TTC credential key secret for dvir api" --type SecureString --key-id c42964a1-ed4e-42ad-bbb4-83c262462539
aws ssm put-parameter --name /dev/efs/ttc/session/dvir/key_secret --value "<sensitive_key>" --description "TTC credential key secret for dvir api" --type SecureString --key-id 0ffbeaa5-1280-4149-9004-74202e31ee1a
aws ssm put-parameter --name /qa/efs/ttc/session/dvir/key_secret --value "<sensitive_key>" --description "TTC credential key secret for dvir api" --type SecureString --key-id 31b21206-9023-4ce6-a57d-56cc88701d1c
aws ssm put-parameter --name /qa-2/efs/ttc/session/dvir/key_secret --value "<sensitive_key>" --description "TTC credential key secret for dvir api" --type SecureString --key-id f555e8a0-c41e-4c6a-82d2-90e82ecaef57

# Adding base URL
aws ssm put-parameter --name /alpha/efs/ttc/api_base_url --value "https://cloud.dev.api.trimblecloud.com" --description "TTC Base URL" --type String
aws ssm put-parameter --name /dev/efs/ttc/api_base_url --value "https://cloud.dev.api.trimblecloud.com" --description "TTC Base URL" --type String
aws ssm put-parameter --name /qa/efs/ttc/api_base_url --value "https://cloud.dev.api.trimblecloud.com" --description "TTC Base URL" --type String
aws ssm put-parameter --name /qa-2/efs/ttc/api_base_url --value "https://cloud.dev.api.trimblecloud.com" --description "TTC Base URL" --type String
'''
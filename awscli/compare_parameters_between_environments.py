"""
Compare the parameters between two environments, print the result of the diff and create a file for each environment with the parameters diff
`env1`: environment to compare with `env2`
`env2`: environment to compare with `env1`

If any parameters are found `env1` that does not present in `env2`, so it will be considered in the diff. Same for `env2`.

Temp files are genated with the diff if this diff exists

"""

import boto3
import tempfile
import json

def run(env1, env2, dump_to_file=False):
    env1_parameters = pull_all_parameters(env1)
    env2_parameters = pull_all_parameters(env2)

    env1_map_subpath = list(map(remove_environment_prefix, env1_parameters))
    env2_map_subpath = list(map(remove_environment_prefix, env2_parameters))

    print(f'\n\n\n=== Parameters present in {env1} but not in {env2}\n\n')
    present_in_env1_but_not_in_env2 = list(filter(lambda p: p not in env2_map_subpath, env1_map_subpath))
    for p in present_in_env1_but_not_in_env2:
        print(f'Parameter {p} present in {env1} but not in {env2}') 

    print(f'\n\n\n=== Parameters present in {env2} but not in {env1}\n\n')
    present_in_env2_but_not_in_env1 = list(filter(lambda p: p not in env1_map_subpath, env2_map_subpath))
    for p in present_in_env2_but_not_in_env1:
        print(f'Parameter {p} present in {env2} but not in {env1}') 

    if dump_to_file:
        fileenv1 = tempfile.NamedTemporaryFile('wt', delete=False, prefix=f'present_in_{env1}_')
        fileenv2 = tempfile.NamedTemporaryFile('wt', delete=False, prefix=f'present_in_{env2}_')
        json.dump(present_in_env1_but_not_in_env2, fileenv1)
        json.dump(present_in_env2_but_not_in_env1, fileenv2)

        print(f'{env1} x {env2} output: {fileenv1.name}')
        print(f'{env2} x {env1} output: {fileenv2.name}')

def remove_environment_prefix(path):
    splitted_path = path.split('/')

    return "/".join(splitted_path[2:len(splitted_path)])

def pull_all_parameters(env):
    client = boto3.client('ssm')
    parameters = []
    parameters_name = []

    next_token = None
    
    
    while True:
    
        kwargs = {
            'Path': f'/{env}',
            'Recursive': True,
            'WithDecryption': True
        }
    
        if next_token != None:
            kwargs.update({'NextToken': next_token})

        response = client.get_parameters_by_path(**kwargs)
        parameters.extend(response['Parameters'])
        if 'NextToken' not in response:
            break
        
        next_token = response['NextToken']

    parameters_name = list(map(lambda p: p['Name'], parameters))
    return parameters_name

if __name__ == "__main__":
    from sys import argv
    environment_1 = argv[1]
    environment_2 = argv[2]

    import os
    os.environ['AWS_PROFILE'] = "isefs-prod"
    os.environ['AWS_REGION'] = "us-east-1"

    dump_to_file = None
    if len(argv) > 3:
        dump_to_file = str(argv[3]).lower() == 'true'

    run(argv[1], argv[2], dump_to_file)

def test_remove_environment_prefix():
    
    paths = [
        "/fieldtest/efs/smm/connstr/failover",
        "/fieldtest/efs/urlrewrite/url",
        "/fieldtest/efs/urlrewrite/type",
        "/fieldtest/efs/webapi/EnableAPIForFSM",
        "/fieldtest/efs/webapi/EnableAPIForPNet",
        "/fieldtest/efs/website/CertificationNotRequiredForExemptDrivers",
        "/fieldtest/efs/website/alk_maps_api_key",
        "/fieldtest/efs/windows/administrator_password",
        "/prod/sauron/graylog/admin_password",
        "/prod/sauron/graylog/server_secret",
        "/prod/sauron/telegraf/mssql_connection_string",
        "/prod/sauron/userify/api_id",
        "/prod/sauron/userify/api_key"
    ]

    single_path_expected = 'efs/smm/connstr/failover'

    result = []

    for p in paths:
        result.append(remove_environment_prefix(p))

    assert result[0] == single_path_expected

    for r in result:
        assert 'fieldtest' not in r
        assert 'prod' not in r
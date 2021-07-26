from datetime import datetime
import boto3
import os
import base64
from uuid import uuid4
import re
import json

from botocore.retries import base
# Certificates from paramter store

def set_aws_env(profile, region):
    os.environ['AWS_PROFILE'] = profile
    os.environ['AWS_REGION'] = region

def run():
    set_aws_env('main-admin', 'us-east-1')

    diff = compare_parameters(
        [
            {
                'source_value': 'some_source_value',
                'parameter_store_value': 'some_parameter_store_value',
                'type': 'path'
            },
            {
                'source_value': 'some_source_value',
                'parameter_store_value': 'some_parameter_store_value',
                'type': 'path'
            }
        ]
    )

    print(diff)


def compare_parameters(m):
    result = []
    for e in m:
        parameter_store_value = pull_parameter_store(e['parameter_store_value'])

        if e['type'] == 'path':
            tmp_file = f'/tmp/tmp.{uuid4()}'
            base64.encode(open(e['source_value'], 'rb'), output=open(tmp_file, 'wb'))
            p = re.compile('\\n')
            source_value = p.sub('', open(tmp_file, 'r').read())
        elif e['type'] == 'text':
            source_value = e['source_value']

        res = {
            'source': source_value,
            'parameter_store_value' : parameter_store_value,
            'diff': diff_value(source_value, parameter_store_value)
        }

        result.append(res)

    result_file = f'result-{uuid4()}.json'
    json.dump(result, open(result_file, 'wt'))
    return result_file
    

def diff_value(source, value):
    return source != value


def pull_parameter_store(name):
    client = boto3.client('ssm')

    response = client.get_parameter(
        Name=name,
        WithDecryption=True
    )

    return response['Parameter']['Value']

if __name__ == '__main__':
    run()
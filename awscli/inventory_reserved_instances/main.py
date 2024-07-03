import click
import boto3
import os
from datetime import datetime
from datetime import timedelta
from datetime import timezone

def set_profile(p):
    os.environ["AWS_PROFILE"] = p

def common_headers() -> list:
    return [
        'aws_account',
        'region',
        'reservation_type'
    ]

def rds_headers():
    return [
        'reservation_id',
        'lease_id',
        'engine',
        'class',
        'offering_type',
        'multi_az',
        'start_date',
        'remaining_days',
        'quantity'
    ]

def opensearch_headers():
    return [
        'reservation_id',
        'lease_id',
        'engine',
        'class',
        'offering_type',
        'multi_az',
        'start_date',
        'remaining_days',
        'quantity'
    ]

def elasticache_headers():
    return [
        'reservation_id',
        'lease_id',
        'engine',
        'class',
        'offering_type',
        'multi_az',
        'start_date',
        'remaining_days',
        'quantity'
    ]

def headers(reservation_type):
    if reservation_type == 'rds':
        headers_to_append = rds_headers()
    elif reservation_type == 'opensearch':
        headers_to_append = rds_headers()
    elif reservation_type == 'elasticache':
        headers_to_append = rds_headers()

    ch = common_headers()
    ch.extend(headers_to_append)
    return ch

def describe(f, nested_property, response={}):
    # base case
    if ('Marker' not in response and 'NextToken' not in response) and response != {}:
        return response
    # Recursion
    
    res = {}
    if 'Marker' in response:
        res=f(Marker=response['Marker'])    
    elif 'NextToken' in response:
        res=f(NextToken=response['NextToken'])
    else:
        res=f()
    
    if response != {}:
        res[nested_property].extend(response[nested_property])
        
    return describe(f, nested_property, res)

# function to calc the remaining days of a reservation
def remaining_days(start_date, duration):
    now = datetime.now(timezone.utc)
    delta = start_date + timedelta(days=duration) - now
    return delta.days

def map_properties(ri, service, profile, region):
    if service == 'rds':
        return [
            profile,
            region,
            'rds',
            ri['ReservedDBInstanceId'],
            ri['LeaseId'],
            ri['ProductDescription'],
            ri['DBInstanceClass'] if 'DBInstanceClass' in ri else ri['InstanceType'],
            ri['OfferingType'],
            str(ri['MultiAZ']),
            datetime.strftime(ri['StartTime'], "%m/%d/%Y"),
            str(remaining_days(ri['StartTime'], ((ri['Duration']/60)/60)/24)),
            str(ri['DBInstanceCount']) if 'DBInstanceCount' in ri else str(ri['InstanceCount'])
        ]
    elif service == 'opensearch':
        return [
            profile,
            region,
            'opensearch',
            ri['ReservedInstanceId'],
            'N/A',
            ri['ReservationName'],
            ri['InstanceType'],
            ri['PaymentOption'],
            'N/A',
            datetime.strftime(ri['StartTime'], "%m/%d/%Y"),
            str(remaining_days(ri['StartTime'], ((ri['Duration']/60)/60)/24)),
            str(ri['InstanceCount'])
        ]
    elif service == 'elasticache':
        return [
            profile,
            region,
            'elasticache',
            ri['ReservedCacheNodeId'],
            'N/A',
            ri['ProductDescription'],
            ri['CacheNodeType'],
            ri['OfferingType'],
            'N/A',
            datetime.strftime(ri['StartTime'], "%m/%d/%Y"),
            str(remaining_days(ri['StartTime'], ((ri['Duration']/60)/60)/24)),
            str(ri['CacheNodeCount'])
        ]

def create_service_list(profile, region, data, service, nested_property):
    reserved_instances = list(filter(lambda ri: ri['State']=='active', data[nested_property]))

    mapped_reserved_instances = list(map(lambda ri: map_properties(ri, service, profile, region), reserved_instances))
    
    return mapped_reserved_instances

def create_list(profile, region, service):
    session = boto3.Session(region_name=region, profile_name=profile)
    if service == 'rds':
        client = session.client('rds')
        response = describe(client.describe_reserved_db_instances, 'ReservedDBInstances')
        return create_service_list(profile, region, response, service, 'ReservedDBInstances')
    elif service == 'opensearch':
        client = session.client('opensearch')
        response = describe(client.describe_reserved_instances, 'ReservedInstances')
        return create_service_list(profile, region, response, service, 'ReservedInstances')
    elif service == 'elasticache':
        client = session.client('elasticache')
        response = describe(client.describe_reserved_cache_nodes, 'ReservedCacheNodes')
        return create_service_list(profile, region, response, service, 'ReservedCacheNodes')

@click.command()
@click.option('--output-path', required=False, default='reserved_instances.csv', help='AWS profile')
def run(output_path):
    profiles = [
        'main-admin',
        'prod-admin'
    ]
    
    regions = [
        'us-east-1',
        'us-east-2'
    ]
    
    # Append headers
    csv=[]
    csv.append(headers('rds'))
    
    for profile in profiles:
        for region in regions:
            rds_list = create_list(profile, region, 'rds')
            opensearch_list = create_list(profile, region, 'opensearch')
            elasticache_list = create_list(profile, region, 'elasticache')
            
            csv.extend(rds_list)
            csv.extend(opensearch_list)
            csv.extend(elasticache_list)
    
    with open(output_path, 'w') as f:
        for line in csv:
            f.write(','.join(line))
            f.write('\n')

if __name__ == '__main__':
    run()
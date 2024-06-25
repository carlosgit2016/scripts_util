import click
import boto3
import os

def set_profile(p):
    os.environ["AWS_PROFILE"] = p
    
def recursive_describe_reserved_db_instances_offerings(Marker="", reserved_db_instances_offerings=[], client=None):
    
    if Marker == None:
        return reserved_db_instances_offerings
    
    if client is None:
        client = boto3.client('rds')

    response = client.describe_reserved_db_instances_offerings(
        Duration="31536000",
        OfferingType="All Upfront",
        Marker=Marker
    )
    
    if len(response["ReservedDBInstancesOfferings"]) > 0:
        reserved_db_instances_offerings.extend(response["ReservedDBInstancesOfferings"])
        
    if 'Marker' not in response:
        response["Marker"]=None
    
    return recursive_describe_reserved_db_instances_offerings(response["Marker"], reserved_db_instances_offerings, client)

# function to filter the offering id from the reserved_db_instances_offering using db engine, deployment option and instance type
# The input will be an list with reserved_db_instances_offering and the db engine, deployment option and instance type

def filter_offering(instance_type, db_engine: str, deployment_option, reserved_db_instances_offerings):
    offering_instance_type = instance_type
    offering_db_engine = db_engine.lower()
    offering_multi_az = deployment_option == 'Multi-AZ'
    
    offering_id = list(filter(lambda x: x['MultiAZ'] == offering_multi_az and x['DBInstanceClass'] == offering_instance_type and x['ProductDescription'].lower() == offering_db_engine, reserved_db_instances_offerings))
    return offering_id[0]['ReservedDBInstancesOfferingId']

@click.command()
@click.option('--dry-run', is_flag=True, default=False, help='Dry run')
@click.option('--profile', default='main-admin', help='AWS profile')
def run(dry_run, profile):
    set_profile(profile)
    client = boto3.client('rds')
    with open('file.csv', 'r') as f:
        data = f.readlines()
        data.pop(0)
        reserved_db_instances_offerings = recursive_describe_reserved_db_instances_offerings()

        for line in data:
            line = line.strip()
            line = line.split(',')
            db_instance_class = line[1]
            product_description = line[3]
            multi_az = line[4]
            quantity = line[5]
            
            offering_id = filter_offering(db_instance_class, product_description, multi_az, reserved_db_instances_offerings)
            
            if dry_run:
                print(f'aws rds purchase-reserved-db-instances-offering --reserved-db-instances-offering-id {offering_id} --db-instance-count {quantity}')
            else:
                response = client.purchase_reserved_db_instances_offering(
                    ReservedDBInstancesOfferingId=offering_id,
                    DBInstanceCount=int(quantity)
                )
                print(response)


if __name__ == '__main__':
    run()
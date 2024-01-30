import boto3
import csv
import os
import click
import logging

CLIENTS = {}
CACHE = {}

def header():
    return [
        "Name",
        "Instance ID",
        "Account ID",
        "Product",
        "Primary contact",
        "Primary contact email",
        "VPC ID",
        "Has VPC Peering",
        "Is internet facing",
        "Has sensitive data",
        "Notes"
    ]


def set_profile(p):
    os.environ["AWS_PROFILE"] = p


def get_boto3_client(client_name: str, region: str) -> boto3.Session:
    global CLIENTS
    if client_name not in CLIENTS.keys():
        CLIENTS[client_name] = boto3.client(client_name, region_name=region)
    return CLIENTS.get(client_name)


def extend_instances(response):
    reservations = response['Reservations']
    instances = []
    for r in reservations:
        if 'Instances' in r:
            instances.extend(r['Instances'])
    return instances


def is_sg_open(sg_ids: list, region: str) -> bool:
    ec2_client = get_boto3_client('ec2', region)

    security_groups = ec2_client.describe_security_groups(GroupIds=sg_ids)['SecurityGroups']
    # Checking if the security group has a 0.0.0.0/0 inbound rule to any port
    for sg in security_groups:
        for ipp in sg["IpPermissions"]:
            for ipr in ipp["IpRanges"]:
                if ipr["CidrIp"] == "0.0.0.0/0":
                    return True
    
    return False


def is_public_facing(instance: object, region: str) -> bool:
    elbv2_client = get_boto3_client('elbv2', region)
    elb_client = get_boto3_client('elb', region)
    instance_id = instance['InstanceId']
    
    sg_ids = list(map(lambda sg: sg["GroupId"], instance["SecurityGroups"]))
    if is_sg_open(sg_ids, region):
        logging.info(f'{instance_id} public facing because of the instance security_group')
        return True

    if 'elbv2' not in CACHE.keys():
        CACHE['elbv2'] = elbv2_client.describe_load_balancers()['LoadBalancers']
    if 'elb' not in CACHE.keys():
        CACHE['elb'] = elb_client.describe_load_balancers()['LoadBalancerDescriptions']

    # Checking the instance in classic load balancers
    for clb in CACHE.get('elb'):
        if clb['Scheme'] == 'internet-facing':
            for instance in clb['Instances']:
                if instance['InstanceId'] == instance_id:
                    if is_sg_open(clb['SecurityGroups'], region):
                        logging.info(f'{instance_id} public facing because of the load_balancer')
                        return True

    if 'target_groups' not in CACHE.keys():
        CACHE['target_groups'] = elbv2_client.describe_target_groups()['TargetGroups']
    # Checking the instance in NLB/ALB
    for lbv2 in CACHE.get('elbv2'):
        if lbv2['Scheme'] == 'internet-facing':
            target_groups = list(filter(lambda tg: lbv2['LoadBalancerArn'] in tg['LoadBalancerArns'], CACHE.get('target_groups')))
            for tg in target_groups:
                target_health_descriptions = elbv2_client.describe_target_health(TargetGroupArn=tg['TargetGroupArn'])['TargetHealthDescriptions']
                for thd in target_health_descriptions:
                    if thd['Target']['Id'] == instance_id:
                        logging.info(f'{instance_id} public facing because of the V2 load_balancer')
                        return True                        

    return False


def get_instance_tag(instance: object, tag_key: str):
    try:
        instance_tag_value = list(filter(lambda t: t['Key'] == tag_key, instance['Tags']))[
            0]['Value']
        return instance_tag_value
    except Exception as e:
        logging.info(f'Not possible to get instance {instance["InstanceId"]} tag_key {tag_key} {e}')


@click.command()
@click.option('--profile', help="AWS profile")
@click.option('--region', help="AWS region")
@click.option('--output-file', type=str, default="instances.csv", help="CSV output file")
def run(profile, region, output_file):
    set_profile(profile)

    client = get_boto3_client('ec2', region)
    response = client.describe_instances(MaxResults=1000)
    instances = extend_instances(response)
    owner_id = response["Reservations"][0]["OwnerId"]

    with open(output_file, 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)

        spamwriter.writerow(header())

        # Map instances to csv
        for i in instances:
            instance_id = i["InstanceId"]
            name = get_instance_tag(i, 'Name')
            try:
                spamwriter.writerow([
                    name,
                    i["InstanceId"],
                    owner_id,
                    get_instance_tag(i, 'product'),
                    get_instance_tag(i, 'primary-contact-name'),
                    get_instance_tag(i, 'primary-contact-email'),
                    i["VpcId"],
                    "", # Manual inserted
                    is_public_facing(i, region),
                    "", # Manual inserted
                    "" # Manual inserted
                ])
            except Exception as e:
                logging.error(
                    f'error writing instance {name} - {instance_id} \n{e}')
            else:
                logging.info(f'instance {name} - {instance_id} writed to csv')


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run()

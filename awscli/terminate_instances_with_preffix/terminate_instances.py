import boto3
import click


def get_instance_name(instance):
    return list(filter(lambda t: t['Key'] == 'Name', instance['Tags']))[0]['Value']


def contains_preffix(instance, prefix):
    tags = instance.get('Tags', [])
    name_tag = get_instance_name(instance)
    return prefix in name_tag


def extend_instances(response):
    reservations = response['Reservations']
    instances = []
    for r in reservations:
        if 'Instances' in r:
            instances.extend(r['Instances'])
    return instances


@click.command()
@click.option('--prefix', '-p', required=True, help='Instance name prefix')
@click.option('--dry-run', '-d', is_flag=True, help='Dry run mode')
def terminate_instances(prefix, dry_run):
    ec2 = boto3.client('ec2')

    instances = extend_instances(ec2.describe_instances())
    instances_to_be_terminated = []

    for instance in instances:
        # print(instance)
        if contains_preffix(instance, prefix):
            instances_to_be_terminated.append({
                "instance_name": get_instance_name(instance),
                "instance_id": instance['InstanceId'],
                "launch_time": instance['LaunchTime'].strftime("%m/%d/%y %H:%M")
            })

    if not instances_to_be_terminated:
        click.echo("No instances found with prefix {}".format(prefix))
        return

    if dry_run:
        click.echo("Dry run mode: the following instances would be terminated:")
        for instance_id in instances_to_be_terminated:
            click.echo("- {}".format(instance_id))
        return

    ec2.terminate_instances(InstanceIds=list(map(
        lambda i: i["instance_id"], instances_to_be_terminated)))
    click.echo("Successfully terminated instances with prefix {}".format(prefix))


if __name__ == "__main__":
    terminate_instances()

import click
import csv
import boto3
import botocore.exceptions


@click.command()
@click.argument('csv_file', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), help='Output file path')
@click.option('--environment', '-e', type=click.Path(), help='Environment tag value to be checked')
def tag_checker(csv_file, output, environment):
    """Reads a CSV file containing instance information and checks if each instance
    has a tag named "Environment"."""
    
    # Create a Boto3 EC2 client
    ec2_client = boto3.client('ec2')
    
    # Open the CSV file
    with open(csv_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        
        # Iterate over each row in the CSV file
        for row in reader:
            instance_id = row['INSTANCE ID']
            instance_name = row['HOST NAME']
            instance_product = row['PRODUCT']
            instance_owner = row['OWNER']
            instance_environment = row.get('tag:Environment')
            
            if not instance_id:
                continue

            # Use Boto3 to describe the instance and get its tags
            response = {}
            try:
                response = ec2_client.describe_instances(InstanceIds=[instance_id])
            except botocore.exceptions.ClientError as error:
                if error.response['Error']['Code'] == 'InvalidInstanceID.NotFound':
                    click.echo(click.style(f'[{instance_name} {instance_id}] instance NOT FOUND', fg='yellow'))
                    continue
                else:
                    raise error
            try:
                tags = response['Reservations'][0]['Instances'][0]['Tags']
            except IndexError as error:
                click.echo(click.style(f'[{instance_name} {instance_id}] tags NOT FOUND', fg='yellow'))
                continue
            
            # Check if the instance has a tag named "Environment" with the specified value
            environment_tag = next((tag for tag in tags if tag['Key'] == 'Environment'), None)
            output_string = ""
            if environment_tag and environment_tag['Value'] == environment:
                # If the instance has the correct tag, print its information to stdout (and optionally to a file)
                output_string = f'[{instance_name} {instance_id}] environment tag EXISTS'
                click.echo(click.style(output_string, fg='green'))
            elif environment_tag and environment_tag['Value'] != environment:
                output_string = f'[{instance_name} {instance_id}] environment tag FOUND, but with a different value |{environment_tag["Value"]}|'
                click.echo(click.style(output_string, fg='red'))
            else:
                output_string = f'[{instance_name} {instance_id}] environment tag NOT FOUND'
                click.echo(click.style(output_string, fg='red'))
            if output:
                with open(output, 'a') as outfile:
                    outfile.write(output_string + '\n')



if __name__ == '__main__':
    tag_checker()

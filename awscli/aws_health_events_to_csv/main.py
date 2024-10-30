'''
This script is inteded to get event notification from AWS and generate a CSV
'''
import boto3
import click
import os
import csv
from datetime import datetime

BOTO_CLIENT = None
AWS_ACCOUNT = None


def header():
    return [
        "Deadline",
        "Source",
        "Account",
        "Region",
        "Service",
        "EventType",
        "Affected Resources",
        "Status",
        "Description",
        "JIRA issue"
    ]


def set_profile(p):
    os.environ["AWS_PROFILE"] = p


def set_aws_account():
    global AWS_ACCOUNT
    AWS_ACCOUNT = boto3.client('sts').get_caller_identity()['Account']

# Singleton implementation


def get_boto_client() -> boto3.Session:
    global BOTO_CLIENT
    if BOTO_CLIENT == None:
        BOTO_CLIENT = boto3.client('health')
        return BOTO_CLIENT
    else:
        return BOTO_CLIENT


def setup_csv(f, data):
    with open(f, 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter='|',
                                quotechar='"', quoting=csv.QUOTE_ALL)
        spamwriter.writerow(header())
        for d in data:
            spamwriter.writerow(d)


def transform_string(s):
    parts = s.split('_')
    transformed_parts = [parts[0]] + [word.capitalize() for word in parts[1:]]
    return ' '.join(transformed_parts)


def filter_event(e) -> bool:
    event_type_code = e['eventTypeCode']
    if event_type_code == "AWS_VPN_REDUNDANCY_LOSS":
        return False
    elif event_type_code == "AWS_CLOUDSHELL_OPERATIONAL_NOTIFICATION":
        return False
    elif event_type_code == "AWS_SAGEMAKER_SECURITY_NOTIFICATION":
        return False
    elif event_type_code == "AWS_SHIELD_ADVANCED_SUBSCRIPTION_RENEWED":
        return False
        
    return True

def populate_and_format(event):
    if not filter_event(event):
        return

    client = get_boto_client()
    event_arn = event['arn']
    event_details = client.describe_event_details(
        eventArns=[
            event_arn
        ]
    )

    affected_entities = client.describe_affected_entities(
        filter={
            'eventArns': [
                event_arn
            ]
        },
        maxResults=100
    )

    row = [
        event['startTime'].strftime('%m/%d/%Y'),
        "AWS",
        AWS_ACCOUNT,
        event['region'],
        event['service'],
        transform_string(event['eventTypeCode']),
        ";".join(list(map(
            lambda affected_entity: affected_entity['entityValue'], affected_entities['entities']))),
        event['statusCode'],
        event_details['successfulSet'][0]['eventDescription']['latestDescription'], # TODO: How to include description that has multiple lines in a csv
    ]

    return row

@click.command()
@click.option("--output-file", default="output.csv", help="Output file")
@click.option("--profile", help="AWS Profile")
@click.option("--initial-date", help="The initial date to gather the events (format %m/%d/%Y %H:%M). e.g. 09/21/2023 00:00")
def run(output_file, profile, initial_date):
    # Set AWS profile
    set_profile(profile)
    set_aws_account()
    client = get_boto_client()

    dt = datetime.strptime(initial_date, "%m/%d/%Y %H:%M")

    events = client.describe_events(filter={
        'startTimes': [
            {
                'from': dt
            }
        ],
        'eventTypeCategories': [
            'accountNotification',
            'scheduledChange'
        ],
        'eventStatusCodes': [
            'open',
            'upcoming'
        ]
    }, maxResults=100)['events']

    events.sort(key=lambda e: e['startTime'])
    mapped_events = list(filter(lambda event: event != None, map(populate_and_format, events)))
    setup_csv(output_file, mapped_events)


if __name__ == "__main__":
    run()

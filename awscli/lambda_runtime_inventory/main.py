import boto3
import click
import os
import sys
import csv


BOTO_CLIENT = None


def header():
    return [
        "Name",
        "ARN",
        "Runtime",
        "PrimaryContact",
        "Description",
        "Tags",
    ]


def set_profile(p):
    os.environ["AWS_PROFILE"] = p

# data: [["row1"], ["row2"]]


def get_boto_client() -> boto3.Session:
    global BOTO_CLIENT
    if BOTO_CLIENT == None:
        BOTO_CLIENT = boto3.client('lambda')
        return BOTO_CLIENT
    else:
        return BOTO_CLIENT


def setup_csv(f, data):
    with open(f, 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(header())
        for d in data:
            spamwriter.writerow(d)


def populate_and_format(function):
    function_name = function["FunctionName"]
    client = get_boto_client()

    full_function = client.get_function(
        FunctionName=function_name
    )
    primary_contact_email = None
    formatted_tags = None
    if 'Tags' in full_function:
        tags = full_function["Tags"]
        if 'primary-contact-email' in tags:
            primary_contact_email = tags['primary-contact-email']
        formatted_tags = ";".join(f"{key}:{value}" for key, value in tags.items())

    row = [
        function_name,
        function["FunctionArn"],
        function["Runtime"],
        primary_contact_email,
        function["Description"],
        formatted_tags
    ]

    print(row)

    return row


@click.command()
@click.option('--profile', help="AWS profile")
@click.option('--lambda-runtime', multiple=True, help="One or more AWS Lambda runtime to filter")
@click.option('--region', help="AWS region")
@click.option('--output-file', type=str, default="lambdas.csv", help="CSV output file")
def run(profile, lambda_runtime, region, output_file):
    set_profile(profile)

    client = get_boto_client()
    functions = []
    NextMarker = ""

    try:
        response = client.list_functions(
            # MasterRegion=region,
            FunctionVersion='ALL',
            MaxItems=50
        )
    except Exception as e:
        print(e)
        sys.exit(1)

    # Iterate through the rest of function if any
    while True:
        if 'Functions' in response:
            functions.extend(response['Functions'])

        if 'NextMarker' not in response:
            break
        else:
            NextMarker = response['NextMarker']

        try:
            response = client.list_functions(
                # MasterRegion=region,
                FunctionVersion='ALL',
                Marker=NextMarker,
                MaxItems=50
            )
        except Exception as e:
            print(e)
            sys.exit(1)

    # Filter functions based on the runtime
    functions_filtered = list(
        filter(lambda f: f["Runtime"] in lambda_runtime, functions))

    mapped_functions = list(map(populate_and_format, functions_filtered))
    # Write to csv file
    setup_csv(output_file, mapped_functions)


if __name__ == "__main__":
    run()

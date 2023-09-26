import boto3
import click
import csv
import re
import base64
import cv2
import numpy as np
import pytesseract
from io import BytesIO
from PIL import Image, ImageFilter, ImageOps, ImageStat


@click.command()
@click.option('--aws-profile', required=True, help='AWS Profile name')
@click.option('--output-file', required=True, type=click.File('w'), help='Output file path')
def get_instance_details(aws_profile, output_file):
    session = boto3.Session(profile_name=aws_profile)
    ec2_client = session.client('ec2')

    # Retrieve all running EC2 instances
    response = ec2_client.describe_instances(
        Filters=[
            {'Name': f'tag:Name', 'Values': ['{name}']}
        ]
    )



    csv_writer = csv.writer(output_file)
    csv_writer.writerow(["Instance ID", "Screenshot path"])

    # Get console screenshot
    screenshot_response = ec2_client.get_console_screenshot(
        InstanceId=instance_id)
    image_data = screenshot_response['ImageData']
    img = Image.open(BytesIO(base64.b64decode(image_data)))
    img.save(f"{instance_id}-screenshot.png")

    # Write to the CSV file
    csv_writer.writerow([instance_id, f"{instance_id}-screenshot.png"])


if __name__ == '__main__':
    get_instance_details()

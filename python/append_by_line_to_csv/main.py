import os
import boto3
import click
import csv

def get_instance_details(session, instance_id):
    ec2 = session.client('ec2')
    try:
        response = ec2.describe_instances(InstanceIds=[instance_id])
        return response
    except Exception as e:
        print(f"Error fetching details for instance {instance_id}. Error: {e}")
        return None

def get_image_details(session, image_id):
    ec2 = session.client('ec2')
    try:
        response = ec2.describe_images(ImageIds=[image_id])
        if "Images" in response and len(response["Images"]) > 0:
            return response["Images"][0]
        else:
            return None
    except Exception as e:
        print(f"Error fetching image details for image id {image_id}. Error: {e}")
        return None

def extract_tag_value(tags, key):
    tag_item = list(filter(lambda t: t["Key"] == key, tags))
    return tag_item[0]["Value"] if tag_item else ""

def format_line(line, instance, instance_data, tags=[], additional=[]):
    line_data = line.strip().split(',')
    for id in instance_data:
        if id in instance:
            line_data.append(str(instance[id]))
        else:
            line_data.append("")
    for tag_key in tags:
        line_data.append(extract_tag_value(instance.get("Tags", []), tag_key))
    line_data.extend(additional)
    return ','.join(line_data) + '\n'

def get_profile(account_id):
    profile = ""
    if account_id == "000000000000":
        profile = "default"
    elif account_id == "000000000000":
        profile = "default"
    else:
        return ""

    return profile

@click.command()
@click.option('--output-file', default='output.csv', help='Output file')
@click.option('--input-file', default='patching.csv', help='Input csv file to be parsed')
def main(output_file, input_file):
    output_filename = output_file
    input_filename = input_file
    
   
    header = ("Sector,"
             "Division,"
             "AccountName,"
             "AccountId,"
             "InstanceId,"
             "Status,"
             "AssetName,"
             "ResourceId,"
             "HighPriorityCount,"
             "TotalCount,"
             "Platform,"
             "LaunchTime,"
             "Primary Contact Email,"
             "Team Contact Email,"
             "AutoscalingGroup,"
             "Environment,"
             "Product Tag,"
             "Patch Group,"
             "CloudFormationStack,"
             "ImageId,"
             "Image Exists?,"
             "Image Name,"
             "Image Creation Date\n") 

    with open(input_filename, mode="r") as f, open(output_filename, "w") as out_file:


        out_file.write(header)

        spamreader = csv.reader(f, delimiter=',')
        for row in spamreader:
            _, _, _, account_id, instance_id, *_ = row
            # Workaround lines with ','
            for i in range(len(row)):
                c = row[i]
                row[i] = c.replace(",", "")
            line = ",".join(row)

            session_profile = get_profile(account_id)
            if session_profile == "":
                continue

            session = boto3.Session(profile_name=session_profile)
            
            instance_data = get_instance_details(session, instance_id)
            if not instance_data or len(instance_data["Reservations"]) == 0:
                continue

            instance = instance_data["Reservations"][0]["Instances"][0]
            image = get_image_details(session, instance["ImageId"])
            if not image:
                image_id, image_exists, image_name, image_creation_date = "", "False", "", ""
            else:
                image_id, image_exists, image_name, image_creation_date = image["ImageId"], "True", image["Name"], image["CreationDate"]

            tags_to_extract = ["primary-contact-email", "team-contact-email", "aws:autoscaling:groupName", "environment", "product", "Patch Group", "aws:cloudformation:stack-name"]
            additional_data = [image_id, image_exists, image_name, image_creation_date]
            instance_data   = ["Platform", "LaunchTime"]
            
            formatted_line = format_line(line, instance, instance_data, tags_to_extract, additional_data)
            print(formatted_line)
            out_file.write(formatted_line)    

if __name__ == "__main__":
    main()


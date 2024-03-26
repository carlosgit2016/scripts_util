import click
import re
import boto3
import subprocess

DRY_RUN=False

@click.command()
@click.option('--users', type=str)
@click.option('--output', type=str, default="keys.csv")
@click.option('--dry-run', is_flag=True, default=False)
def run(users, output, dry_run):
    global DRY_RUN
    DRY_RUN=dry_run

    users = re.split('\s+', users)
    iam_client = boto3.client('iam')
    keys = []

    for u in users:
        response = {}
        try:
            if DRY_RUN:
                print("Would create a key access for {u}")
                continue
            response = iam_client.create_access_key(
                    UserName=u                    
            )
            print(f'Created key {response["AccessKey"]["AccessKeyId"]} for {u}')
        except Exception as e:
            print(f'Failed to create a new key for {u}\n{e}')
            continue

        keys.append(response["AccessKey"])
    if not DRY_RUN:
        save_keys(keys, output)
    create_secure_note_lt(keys)

def save_keys(keys, output_file):
    headers = [
        'UserName'
        'AccessKeyId'
        'Status'
        'SecretAccessKey'
        'CreateDate'
    ]

    with open(output_file, 'w') as file:
        for k in keys:
            key_attr = list(map(lambda k_attr: str(k_attr), k.values()))            
            file.write(f'{",".join(key_attr)}\n')

def create_secure_note_lt(keys):
    for k in keys:
        line = "\n".join([
                f'ACCESS_KEY_ID {k["AccessKeyId"]}',
                f'SECRET_ACCESS_KEY {k["SecretAccessKey"]}',
                f'CREATE_DATE {k["CreateDate"]}',
        ])
        lt(k['UserName'], line)

def lt(name, data):
    cmd = ["./lt.sh", name, data]
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=True)
    except subprocess.SubprocessError as e:
        print(f"Failed to create secure note in LT for {name}\ncommand: {e.cmd} \n{e.stdout}")

if __name__ == "__main__":
    run()

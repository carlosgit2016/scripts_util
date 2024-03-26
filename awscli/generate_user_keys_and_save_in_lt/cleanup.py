import boto3

client = boto3.client("iam")

with open("keys.csv", "r") as f:
    data = f.read()
    lines = data.split("\n")
    for l in lines:
        args = l.split(",")
        username=args[0]
        access_key=args[1]
        client.delete_access_key(UserName=username, AccessKeyId=access_key)
        print(f'Deleted key {access_key} for {username}')

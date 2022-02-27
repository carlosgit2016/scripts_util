'''
    Script to retrieve an entire cloudwatch log event from a specific stream
'''
import boto3
import tempfile

def run(log_group, stream, dump_for_file=False):
    client = boto3.client('logs')
    next_token = None
    events = []

    while True:
        
        kwargs = {
            'logGroupName': log_group,
            'logStreamName': stream,
            'startFromHead': True
        }
    
        if next_token != None:
            kwargs.update({'nextToken': next_token})

        response = client.get_log_events(**kwargs)
        events.extend(map(lambda e: str(e['message']), response['events']))

        if 'nextToken' not in response:
            break
        
        next_token = response['nextToken']

    
    text_events = "\n".join(events)
    print(text_events)

    if dump_for_file:
        temp_file = tempfile.NamedTemporaryFile('wt', delete=False)
        temp_file.write(text_events)
        temp_file.close()

        print(f'\n\n Also present in: {temp_file.name}')

if __name__ == "__main__":
    from sys import argv
    log_group = argv[1]
    stream = argv[2]

    import os
    os.environ['AWS_PROFILE'] = "isefs-prod"
    os.environ['AWS_REGION'] = "us-east-1"

    dump_to_file = None
    if len(argv) > 3:
        dump_to_file = str(argv[3]).lower() == 'true'

    run(argv[1], argv[2], dump_to_file)
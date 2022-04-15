'''
    Script to retrieve an entire cloudwatch log event from a specific stream
'''
import boto3
import tempfile
import argparse

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
    parser = argparse.ArgumentParser(description='Retrieve entire logs from a desired stream')

    parser.add_argument('--log-group', required=True, metavar='log_group', nargs=1, help='The name of the cloudwatch log group')
    parser.add_argument('--log-stream', required=True, metavar='log_stream', nargs=1, help='The name of the cloudwatch log stream')
    parser.add_argument('--dump-to-file', action='store_true', help='Dump the logs for a temporary file')

    args = parser.parse_args()
    print(args.log_group)
    run(args.log_group, args.log_stream, args.dump_to_file)

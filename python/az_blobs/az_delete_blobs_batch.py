#!/home/cflor/.asdf/shims/python
import json
import subprocess
import tempfile
from dateutil.parser import *

from multiprocessing import Pool

def run(account_name, container_name):

    print('Searching for blobs to delete')
    blobs = subprocess.run(['az', 'storage', 'blob', 'list', '-c', container_name, '--account-name', account_name, '--only-show-errors', '--num-results', '*'], capture_output=True)

    if blobs.stderr:
        print(blobs.stderr)
        exit(1)

    blobs_json = json.loads(blobs.stdout)
    filtered_blobs = list(filter(greater_than_eight_days, blobs_json))

    print(f'Found {len(blobs_json)} in total')
    tmpfile = tempfile.NamedTemporaryFile('wt', delete=False)
    tmpfile_to_exec = tempfile.NamedTemporaryFile('wt', delete=False, prefix='blobs_to_delete_')

    print(f'Writing all blobs to {tmpfile.name}')
    json.dump(filtered_blobs, tmpfile, indent=4)

    print('Total of MB to exclude ', end='')
    total_content_length = 0
    for b in filtered_blobs:
        total_content_length += (b["properties"]["contentLength"] / 1024 ** 2)
    print(total_content_length)
    print(f'Total of GB to exclude {round(total_content_length / 1024, 2)}')
    print(f'Total of {len(filtered_blobs)} to be deleted')

    print('Continue...')
    input()
    date_out = subprocess.run(f'date -d "15 days ago" \'+%Y-%m-%dT00:00Z\'', shell=True, capture_output=True)
    print(f'Batch deleting older than {date_out.stdout} ')
    batch_delete_out = subprocess.run(f'az storage blob delete-batch -s {container_name} --account-name {account_name} --if-unmodified-since {date_out.stdout} -o json', shell=True, capture_output=True)
    print(batch_delete_out.stdout)

    
def lease_and_delete_blob(blob_name, container_name, account_name):
    lease_out = subprocess.run(f'az storage blob lease break -b {blob_name} -c {container_name} --account-name {account_name} 2> /dev/null', shell=True, capture_output=True)
    delete_out = subprocess.run(f'az storage blob delete -n {blob_name} -c {container_name} --account-name {account_name} 2> /dev/null', shell=True, capture_output=True)
    print(lease_out, delete_out)

def greater_than_eight_days(b):
    eight_days_ago = parse('2022-07-05 00:00:00 UTC').timestamp()
    creation_time = parse(b["properties"]["lastModified"]).timestamp() 
    return creation_time < eight_days_ago

if __name__ == "__main__":
    import sys

    run(sys.argv[1], sys.argv[2])
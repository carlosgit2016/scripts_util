# %%
import json
import subprocess

blobs = subprocess.run(['az', 'storage', 'blob', 'list', '-c', 'sqlserverbackups', '--account-name', 'sqlserverstgeastus2st', '--only-show-errors', '--num-results', '*'], capture_output=True)
blobs_json = json.loads(blobs.stdout)
blobs_filtered = map(lambda b: { "name": b["name"], "immutabilityPolicy": b["immutabilityPolicy"], "creationTime": b["properties"]["creationTime"], "lastModified": b["properties"]["lastModified"], "remainingRetentionDays": b["properties"]["remainingRetentionDays"] }, blobs_json)
blobs_list = list(blobs_filtered)
blobs_list_temp = blobs_list

# %%
how_many_page_blobs = len(list(filter(lambda b:  b["properties"]["blobType"] == "PageBlob" if "properties" in b else False, blobs_json)))
print(how_many_page_blobs)

# %%
json.dump(blobs_list, open('/tmp/tmp.GSqB4XofWl', 'w'))

# %%
from dateutil.parser import *

eight_days_ago = parse('2022-06-30 00:00:00 UTC').timestamp()

def greater_than_eight_days(b):
    creation_time = parse(b["lastModified"]).timestamp() 
    return creation_time < eight_days_ago

should_be_deleted = list(filter(greater_than_eight_days, blobs_list))

# %%
json.dump(should_be_deleted, open('/tmp/tmp.PwFKvPVVdx', 'w'))

# %% 
with open('/tmp/tmp.PwFKvPVVdx', 'w') as f:
    f.write("\n".join(list(map(lambda b: b["name"], should_be_deleted))))
    f.close()
# %%
print("properties" in {"properties": {}})
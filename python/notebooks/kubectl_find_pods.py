# %%
import subprocess
import json

kubectl_pods_res = subprocess.run(['kubectl', 'get', 'pods', '-n', 'dev', '-o', 'json'], stdout=subprocess.PIPE)

# %%
pods = json.loads(kubectl_pods_res.stdout)
# %%
tag = 'tags.datadoghq.com/service'

pods_labels = []

for p in pods['items']:
    pods_labels.append(p['metadata']['labels'])



# %%
pods_jobs = list(filter(lambda p: 'job-name' in p, pods_labels))
pods_dd_jobs = list(filter(lambda p: 'tags.datadoghq.com/env' in p, pods_jobs))
print(json.dumps(pods_dd_jobs))
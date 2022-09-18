# %%
from git import Repo

r: Repo = Repo('/home/cflor/git/DSP.d/gcp-pubsub-connector-fork')
references = r.remote().refs

branches_to_remove = [
    'origin/renovate/org.mockito-mockito-core-4.x',
    'origin/renovate/com.google.cloud-google-cloud-pubsublite-1.x',
    'origin/renovate/org.apache.kafka-kafka-clients-3.x',
    'origin/renovate/com.google.cloud-google-cloud-pubsublite-0.x'
]

references = list(filter(lambda r: r.name not in branches_to_remove, references))

commits_to_cherry_pick = list(filter(lambda c: c != None, map(lambda r: r.commit.hexsha if 'origin/renovate/' in r.name  else None, references)))

print(commits_to_cherry_pick)
print(len(commits_to_cherry_pick))

print(f'git cherry-pick {" ".join(commits_to_cherry_pick)}')

# %%

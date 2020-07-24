$Token = "<personal_token>"
$BitbucketRepos = iwr "https://<bitbucket_url>/rest/api/1.0/projects/EFS/repos/" -Method GET -Headers @{Authorization=("Bearer {0}" -f $Token)} | ConvertFrom-Json 
$BitbucketRepos.values.ForEach({
   git clone $_.links.clone.href[1];
})

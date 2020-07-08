#Reference: https://docs.newrelic.com/docs/apm/new-relic-apm/maintenance/record-monitor-deployments

$Headers = @{ 
    "X-Api-Key" = "<API_KEY>"; 
}

$Body = 

'{
  "deployment": {
    "revision": "REVISION",
    "changelog": "Added: /v2/deployments.rb, Removed: None",
    "description": "Added a deployments resource to the v2 API",
    "user": "datanerd@example.com",
    "timestamp": "2019-10-08T00:15:36Z"
  }
}';


iwr "https://api.newrelic.com/v2/applications/<APP_ID>/deployments.json" -Method Post -Headers $Headers -Body $Body -ContentType "application/json" 

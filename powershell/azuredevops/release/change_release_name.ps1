# Change the arguments to continue:
$Organization = "<organization>"
$Project = "<project_name>";
$ReleaseId = <release_id> # You can get on release url
$Token = "<PAT>"
$ReleaseName = "<new_release_name>"

# Alter Release name azure devops
$url = "https://vsrm.dev.azure.com/$($Organization)/$($Project)/_apis/release/releases/$($ReleaseId)?api-version=5.1"
#Encode token to Base64
$EncodedTokenBase64 = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes(("{0}:{1}" -f '', $Token)))
$Headers = @{"Authorization" = "Basic $($EncodedTokenBase64)" }
$pipeline = Invoke-RestMethod -Uri $url -Headers $Headers
Write-Host "Pipeline = $($pipeline | ConvertTo-Json -Depth 99)"
# Edit variable pipeline name
$pipeline.name = $ReleaseName
####****************** update the modified object **************************
$json = @($pipeline) | ConvertTo-Json -Depth 99
Invoke-RestMethod -Uri $url -Method Put -Body $json -Headers $Headers -ContentType "application/json;charset=utf-8"

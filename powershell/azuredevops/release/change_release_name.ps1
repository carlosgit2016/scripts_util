# Alter Release name azure devops
$url = "https://vsrm.dev.azure.com/{organization}/{project}/_apis/release/releases/{release_id}?api-version=5.1"
$Token = $personalToken
#Encode token to Base64
$EncodedTokenBase64 = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes(("{0}:{1}" -f '', $Token)))

$Headers = @{"Content-Type" = "application/json"; "Authorization" = "Basic $($EncodedTokenBase64)" }

$pipeline = Invoke-RestMethod -Uri $url -Headers $Headers

Write-Host "Pipeline = $($pipeline | ConvertTo-Json -Depth 100)"

# Edit variable pipeline name
$pipeline.name = "new_release_name"

####****************** update the modified object **************************
$json = @($pipeline) | ConvertTo-Json -Depth 99

Invoke-RestMethod -Uri $url -Method Put -Body $json -Headers $Headers
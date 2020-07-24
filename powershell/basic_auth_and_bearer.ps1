# Basic Authentication to request token or make a direct request 
$username = "<user>";
$password = "<pass>";
$base64AuthInfo = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes(("{0}:{1}" -f $username,$password)))
iwr "<url_to_make_request>" -Method POST -Body $Body -Headers @{Authorization=("Basic {0}" -f $base64AuthInfo)} | ConvertFrom-Json 

# OAuth Bearer
iwr "<url_to_make_request>" -Method POST -Body $Body -Headers @{Authorization=("Bearer {0}" -f $base64AuthInfo)} | ConvertFrom-Json 

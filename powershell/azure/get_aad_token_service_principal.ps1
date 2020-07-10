# GET AAD Token with Service Principal

$AppID = "<app_id>";
$TenanID = "<tenant_id>";
$ClientSecret = "<client_secret>";
$Resource = "<resource_id>"

$Body = @{
    grant_type="client_credentials";
    client_id=$AppID;
    client_secret=$ClientSecret;
    resource=$Resource;
}

$Response = iwr "https://login.microsoftonline.com/$TenanID/oauth2/v2.0/token" -Headers $Headers -ContentType "application/x-www-form-urlencoded" -Body $Body

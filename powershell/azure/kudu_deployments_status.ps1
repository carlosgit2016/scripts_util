# Last Deployments

function GetLastDeployments {
    param (
        [String]$SiteName,
        [String]$User,
        [String]$Password
    )

    $Response = curl -u "$($User):$Password" "https://$SiteName.scm.azurewebsites.net/api/deployments" | convertfrom-json;
    Write-Output $Response
    
}

# GetLastDeployments <site-name> <user> <password>

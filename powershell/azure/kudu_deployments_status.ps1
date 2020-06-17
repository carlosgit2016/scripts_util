# Last Deployments

function GetLastDeployments {
    param (
        [String]$SiteName,
        [String]$User,
        [String]$Password
    )

    $Response = curl -u "$($User):$Password" $SiteName | convertfrom-json;
    Write-Output $Response
    
}

# GetLastDeployments <site-name> <user> <password>
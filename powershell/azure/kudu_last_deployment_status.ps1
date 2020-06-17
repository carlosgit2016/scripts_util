# Azure Webapp deployment status

function GetLastDeployment {
    param (
        [String]$SiteName,
        [String]$User,
        [String]$Password
    )

    $Response = curl -s -u "$($User):$Password" $SiteName | convertfrom-json;
    $LastDeploy = curl -s -u "$($User):$Password" $Response[0].log_url | convertfrom-json;
    foreach ($info in $LastDeploy){
        Write-Output "================================================== $($info.log_time) ================================================"
        Write-Output ($info | ConvertTo-Json)
        if($null -ne $info.details_url) {
            $Details = curl -s -u "$($User):$Password" $info.details_url | convertfrom-json;
            Write-Output "More details:" $Details;
            $Details = $null;
        }
        
    }    
}

GetLastDeployment <site-name> <user> <password>
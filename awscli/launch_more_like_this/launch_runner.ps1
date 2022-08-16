[CmdletBinding()]
param (
    [Parameter()]
    [String]
    $AMI_ID,
    [Parameter()]
    [String]
    $SourceInstanceName,
    [Parameter()]
    [String]
    $QueueName,
    [Parameter()]
    [String]
    $NewInstanceName
)

function RunAndConvertToJson {
    param (
        [String]
        $Command
    )

    $Result = pwsh -nologo -command $Command
    $Result = $Result -join '' | ConvertFrom-Json -Depth 99
    return $Result
}

function RetrieveInstanceConfigs {
    param (
        [String]$SourceInstanceName
    )

    $SourceInstanceConfigs = RunAndConvertToJson "aws ec2 describe-instances --filters 'Name=tag:Name,Values=$SourceInstanceName'"
    return $SourceInstanceConfigs.Reservations[0].Instances[0]
}

function ChangeQueueUserData {
    param (
        [String]$QueueName,
        [Object]$InstanceConfigs
    )

    $InstanceId = $InstanceConfigs.InstanceId
    $UserData = RunAndConvertToJson "aws ec2 describe-instance-attribute --instance-id $InstanceId --attribute userData"
    $UserDataDecoded = [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($UserData.UserData.Value)) -replace 'queue=efs-windows', "queue=$QueueName"
    $UserDataFile = New-item -ItemType File -Path $([IO.Path]::GetTempPath()) -Name "$($InstanceConfigs.InstanceId)_user_data" -Value $UserDataDecoded -Force
    return $UserDataFile
}

function RetrieveTags {
    param (
        [String]$NewInstanceName,
        [Object]$InstanceConfigs
    )

    $InstanceConfigs.Tags.ForEach( 
        { 
            if ($_.Key -eq "Name") { 
                $_.Value=$NewInstanceName 
            } 
        } 
    )

    $TagSpecifiations = [System.Collections.ArrayList]@()
    foreach ($Tag in $InstanceConfigs.Tags) {
        if ($Tag.Key.Contains("aws:")){
            continue
        }
        $Null = $TagSpecifiations.Add("{Key=`"$($Tag.Key)`",Value=`"$($Tag.Value)`"}")
    }
    return "ResourceType=instance,Tags=[$($TagSpecifiations | Join-String -Separator ',')]"
}

Write-Host "Retrieving configs from $SourceInstanceName"
$InstanceConfigs = RetrieveInstanceConfigs $SourceInstanceName
Write-Host "Retrieving User Data from $SourceInstanceName"
$UserDataFile = ChangeQueueUserData $QueueName $InstanceConfigs
Write-Host "Retrieving Tags from $SourceInstanceName"
$StringTags = RetrieveTags $NewInstanceName $InstanceConfigs

Write-Host "Running instance $NewInstanceName $AMI_ID"
$Command = ("aws ec2 run-instances `
--image-id $AMI_ID `
--instance-type $($InstanceConfigs.InstanceType) `
--security-group-ids $($InstanceConfigs.SecurityGroups.GroupId | ForEach-Object { "'$_'" } | Join-String -Separator ' ') `
--count 1 --subnet-id $($InstanceConfigs.SubnetId) `
--key-name $($InstanceConfigs.KeyName) `
--user-data file://$($UserDataFile.FullName) `
--tag-specifications '$StringTags'").Split("`n") | % { $_ } | Join-String -Separator ' '

pwsh -nologo -command $Command

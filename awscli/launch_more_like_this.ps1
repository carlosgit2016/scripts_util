function LaunchMoreLikeThis ([String]$SourceInstanceName, [String]$CloneInstanceName, [String]$AMI_ID, [String]$InstanceType, [Int64]$Count = 1) {
    $SourceInstance = aws ec2 describe-instances --filters "Name=tag:Name,Values=$SourceInstanceName"
    $SourceInstance = $SourceInstance -join '' | ConvertFrom-Json -Depth 99

    $SourceInstanceAttr = $SourceInstance.Reservations.Instances[0];
    $InstanceId = $SourceInstanceAttr.InstanceId
    $SGs = $SourceInstanceAttr.SecurityGroups.GroupId | ForEach-Object { "`"$_`"" } | Join-String -Separator ' '  ;
    $PrivateKey = $SourceInstanceAttr.KeyName
    $SubnetId = $SourceInstanceAttr.SubnetId
    $UserData = pwsh -nologo -command "aws ec2 describe-instance-attribute --instance-id $InstanceId --attribute userData"
    $UserData = $UserData -join '' | ConvertFrom-Json -Depth 99
    $UserDataDecoded = [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($UserData.UserData.Value))
    $UserDataFile = New-item -ItemType File -Path $([IO.Path]::GetTempPath()) -Name "user_data" -Value $UserDataDecoded -Force #You can change this to use a different user_data
    $Tags = "ResourceType=instance,Tags=[{Key=Name,Value=$CloneInstanceName}]"
    pwsh -nologo -command "aws ec2 run-instances --image-id $AMI_ID --instance-type $InstanceType --security-group-ids $SGs --count 1 --subnet-id $SubnetId --key-name $PrivateKey --user-data file://$($UserDataFile.FullName) --tag-specifications `'$Tags`'"

}


LaunchMoreLikeThis -SourceInstanceName "dev_compliance_ad_web" -CloneInstanceName "dev_compliance_ad_web_carlos" -AMI_ID "ami-058f41137c9192e08" -InstanceType "t3.medium"

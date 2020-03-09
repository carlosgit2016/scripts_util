function ConnectRemoteComputerInlinePassword {
    param (
        
        [Parameter(Mandatory)]
        [String]
        $ComputerName,
        [Parameter(Mandatory)]
        [String]
        $UserName,
        [Parameter(Mandatory)]
        [securestring]
        $Password
    )

    # Convert To Secure String
    # ConvertTo-SecureString "password" -AsPlainText -Force
    $Credential = New-Object System.Management.Automation.PSCredential ($UserName, $Password )

    # New session on remote computer
    $SessionRemoteComputer = New-PSSession -ComputerName $ComputerName -Credential $Credential


    #Enter on new session created below
    Enter-PSSession $SessionRemoteComputer    
}



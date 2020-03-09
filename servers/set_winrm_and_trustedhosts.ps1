function ConfigureWinRMAndTrustedHosts {

    try {
    
        winrm.cmd quickconfig

        # Get Trusteds hosts
        
        $trustedHosts = "WSMan:\localhost\Client\TrustedHosts"
        
        Set-Item WSMan:\localhost\Client\TrustedHosts *       
        
        Get-Item $trustedHosts 

        Write-Host "Success configured"
    }
    catch {
        Write-Error "Error: $_.ErrorMessage"
    }

}

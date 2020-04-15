# Get Properties of a Powershell Object

function GetObjProperties {
    param (
        $ObjectToPrintProperties
    )

    $properties = ($ObjectToPrintProperties).psobject.properties;
    return $properties.ForEach{ Write-Host $_.Name };
}

# Example to use
$props = GetObjProperties -ObjectToPrintProperties (Get-Service) # Get all properties of the object returned by Get-Service cmdlet 
Write-Host $props

function CreateHeadersToRequestAzureDevops ([string]$TokenToMakeRequest) {
    $EncodedTokenBase64 = ConvertEncoded64 -StringToConvert $TokenToMakeRequest;
    return @{"Content-Type" = "application/json"; "Authorization" = "Basic $($EncodedTokenBase64)" };
}

function ConvertEncoded64 ([Parameter(Mandatory)][string]$StringToConvert) {
    return [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes(("{0}:{1}" -f '', $StringToConvert)))
}

function MakeRequest ([Parameter(Mandatory)]$Body, [Parameter(Mandatory)]$Method, [Parameter(Mandatory)][string]$TokenToMakeRequest, [Parameter(Mandatory)]$Url) {
    $Headers = CreateHeadersToRequestAzureDevops -$TokenToMakeRequest;
    $Response = Invoke-WebRequest -Uri $Url -Headers $Headers -Method $Method -Body $Body;
    return $Response;
}


## Example Put a new information in a release pipeline

$url = "https://vsrm.dev.azure.com/{organization}/{project}/_apis/release/definitions/6?api-version=5.1"
$token = "my_pat"
$body = '{ "my": "body pipeline" }'

$response = MakeRequest -Body $body -Method Put -TokenToMakeRequest $token -Url $url;

write-host $response;

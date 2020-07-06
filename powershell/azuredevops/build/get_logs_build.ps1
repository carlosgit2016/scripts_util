function ConvertEncoded64 ([Parameter(Mandatory)][string]$StringToConvert) {
    return [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes(("{0}:{1}" -f '', $StringToConvert)))
}

function CreateHeadersToRequestAzureDevops ([string]$TokenToMakeRequest) {
    $EncodedTokenBase64 = ConvertEncoded64 -StringToConvert $TokenToMakeRequest;
    return @{"Content-Type" = "application/json"; "Authorization" = "Basic $($EncodedTokenBase64)" };
}

$token = "<token>";

$Headers = CreateHeadersToRequestAzureDevops $token;


$Response = iwr "https://dev.azure.com/<organization>/<project>/_apis/build/builds/<buildId>/logs?api-version=5.1" -Headers $Headers


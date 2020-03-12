## Convert String to Encoded64

function ConvertEncoded64 ([Parameter(Mandatory)][string]$StringToConvert) {
    return [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes(("{0}:{1}" -f '', $StringToConvert)))
}

## Example to use

ConvertEncoded64 -StringToConvert "string_test_to_convert"

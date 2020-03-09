
function CopyFileToSession {
    param (
        [Parameter(Mandatory)][String]$SourcePath,
        [Parameter(Mandatory)][String]$Destination,
        [Parameter(Mandatory)][System.Management.Automation.Runspaces.PSSession]$Session
    )

    # Copy a file or folder to another computer remote using a custom session
    # if you need the reverse option change the "TosSession" to "FromSession"

    Copy-Item -Recurse -Path ("C:\instantclient_19_3") -Destination C:\ -ToSession $Session

}

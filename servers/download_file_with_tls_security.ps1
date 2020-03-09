New-Item -name "common.jar" -Path "C:\Temp\"
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
Invoke-WebRequest -Uri "https://repo1.maven.org/maven2/com/csicit/ace/common/1.0.21/common-1.0.21.jar" -Method Get -OutFile "C:\Temp\common.jar"

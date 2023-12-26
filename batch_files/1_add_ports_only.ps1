# Récupérer les arguments à passer au script ps1

param(
    [string[]]$printerPorts
)

$portMonitor = "strsmon"

#Chemin dans le registre du  moniteur streamserve
$printersRoot = "HKLM:\SYSTEM\CurrentControlSet\Control\Print\Monitors"
$streamServePortsPath = Join-Path -Path $printersRoot -ChildPath "StreamServe\Ports"

foreach ($port in $printerPorts) {
    $portRegistryPath = Join-Path -Path $streamServePortsPath -ChildPath $port

    if (!(Test-Path $portRegistryPath)) {
        # Create the registry key for the printer port
        New-Item -Path $portRegistryPath -Force | Out-Null
    }

    # Set properties for the printer port
    Set-ItemProperty -Path $portRegistryPath -Name "OutputType" -Value 0
    $portFilesPath = "E:\STR_SERVICES\editique_$port\input"
    Set-ItemProperty -Path $portRegistryPath -Name "Path" -Value $portFilesPath
    Set-ItemProperty -Path $portRegistryPath -Name "Description" -Value "StreamServe Port"
    Set-ItemProperty -Path $portRegistryPath -Name "PortMonitor" -Value $portMonitor

    Write-Host "Printer port '$port' configuration has been updated."
}

Write-Host "Printer port configurations updated successfully."

# Restart the Print Spooler service
Restart-Service -Name Spooler -Force
Write-Host "Print Spooler service restarted."

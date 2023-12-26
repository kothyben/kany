$portsToRemove = Get-PrinterPort | Where-Object { $_.Description -eq "StreamServe Port" -and $_.PortMonitor -eq "strsmon" }
$registryPath = "HKLM:\SYSTEM\CurrentControlSet\Control\Print\Monitors\StreamServe\Ports"

foreach ($portToRemove in $portsToRemove) {
    # Check if the registry entry exists before deleting
    if (Test-Path "$registryPath\$($portToRemove.Name)") {
        Remove-Item -Path "$registryPath\$($portToRemove.Name)" -Force
        Write-Host "Registry entry for port '$($portToRemove.Name)' has been deleted."
    } else {
        Write-Host "Registry entry for port '$($portToRemove.Name)' does not exist."
    }

    Remove-Printer -Name "OutQueue_$($portToRemove.Name)" -ErrorAction SilentlyContinue
    Remove-PrinterPort -Name $portToRemove.Name -ErrorAction SilentlyContinue
}

Restart-Service Spooler

# Get a list of printers with names starting with "OutQueue_"
$printers = Get-Printer -Name "OutQueue_*"

$registryPath = "HKLM:\SYSTEM\CurrentControlSet\Control\Print\Monitors\StreamServe\Ports"

foreach ($printer in $printers) {
    # Check if the registry entry exists before deleting
    $portNameWithoutPrefix = $printer.Name -replace '^OutQueue_', ''

    if (Test-Path "$registryPath\$portNameWithoutPrefix") {
        Remove-Item -Path "$registryPath\$portNameWithoutPrefix" -Force
        Write-Host "Registry entry for port '$portNameWithoutPrefix' has been deleted."
    } else {
        Write-Host "Registry entry for port '$portNameWithoutPrefix' does not exist."
    }

    Remove-Printer -Name $printer.Name -ErrorAction SilentlyContinue
    Remove-PrinterPort -Name $portNameWithoutPrefix -ErrorAction SilentlyContinue
}

# Restart the Print Spooler service
Restart-Service -Name Spooler

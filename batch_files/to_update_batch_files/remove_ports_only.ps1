$portsToRemove = Get-PrinterPort | Where-Object { $_.Description -eq "Standard TCP/IP Port" -and $_.PortMonitor -eq "TCPMON.DLL" }

foreach ($port in $portsToRemove) {
    $associatedPrinters = Get-WmiObject -Class Win32_Printer -Filter "PortName='$($port.Name)'"

    if ($associatedPrinters) {
        Write-Host "The port $($port.Name) is in use by one or more printers. Skipping removal."
    } else {
        Remove-PrinterPort -Name $port.Name
        Write-Host "Printer port $($port.Name) removed successfully."
    }
}

$Printers = Get-Printer -Name "OutQu*"

foreach ($Printer in $Printers) {
    $PortInfo = Get-WmiObject -Query "SELECT * FROM Win32_TCPIPPrinterPort WHERE Name = '$($Printer.PortName)'"
    
    Write-Host "Printer Name: $($Printer.Name)"
    Write-Host "Port Name: $($Printer.PortName)"
    if ($PortInfo) {
        Write-Host "Port Description: $($PortInfo.Description)"
        Write-Host "Port Host Address: $($PortInfo.HostAddress)"
        Write-Host "Port Port Number: $($PortInfo.PortNumber)"
        Write-Host "Port Printer Path: $($PortInfo.PrinterHostAddress)"
        Write-Host "--------------------------------------------------------"
    } else {
        Write-Host "No additional information available for this port."
        Write-Host "--------------------------------------------------------"
    }
}

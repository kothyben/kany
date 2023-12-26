$printerPorts = "AEES_TST", "AURU_TST", "MANUAL_TST", "KIKO_TST", "BOIT_TST"

foreach ($port in $printerPorts) {
    $printerName = "OutQueue_$port"  # Construct printer name based on the port
    $printer = Get-WmiObject -Class Win32_Printer -Filter "Name='$printerName'"
    if ($printer) {
        $associatedPorts = $printer | Select-Object -ExpandProperty PortName

        Write-Host "Printer Name: $($printer.Name)"
        Write-Host "Number of Printer Ports: $($associatedPorts.Count)"
        Write-Host "Associated Ports: $($associatedPorts -join ', ')"

        foreach ($portName in $associatedPorts) {
            $portInfo = Get-WmiObject -Query "SELECT * FROM Win32_TCPIPPrinterPort WHERE Name='$portName'"
            if ($portInfo) {
                Write-Host "Port Name: $($portInfo.Name) | Port Monitor: $($portInfo.HostAddress) | Description: $($portInfo.Description)"
            } else {
                Write-Host "Port information not found for $portName."
            }
        }
    } else {
        Write-Host "Printer '$printerName' not found."
    }
}

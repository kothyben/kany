# Récupérer les arguments à passer au script ps1

param(
    [string[]]$printerPorts
)

# Boucle pour chaque port
foreach ($printerPort in $printerPorts) {

    # existing port
    $port = Get-PrinterPort | Where-Object { $_.Description -eq "StreamServe Port" -and $_.PortMonitor -eq "strsmon" -and $_.Name -eq $printerPort }

    if ($port) {
        # Créer une nouvelle imprimante si le port existe
        $printerName = "OutQueue_$($port.Name)"
        $shareName = $port.Name
        $printerModel = "Generic / Text Only"
        $portName = $port.Name
        $location = ""
        $comment = ""
        Add-Printer -Name $printerName -ShareName $shareName -DriverName $printerModel -PortName $portName -Location $location -Comment $comment -ComputerName $env:COMPUTERNAME
    } else {
        Write-Host "Le port  $printerPorts n'existe pas ou ne correspond pas aux critères spécifiés."
    }

    
    
}

Write-Host "Done!"

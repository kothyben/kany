$printerInfo = Get-Content -Raw "printers_infos.json" | ConvertFrom-Json
foreach ($printer in $printerInfo) {
  $driverName = $printer.DriverName
  $portName = $printer.PortName
  $printerName = $printer.Name
  $portAddress = ""

  # Vérifier si l'adresse IP est fournie dans le format "IP_x.y.z.t"
  if ($portName -match '^IP_(\d+\.\d+\.\d+\.\d+)$') {
    $portAddress = $Matches[1]
  }

  # Vérifier si le nom de l'imprimante ne commence pas par "OutQueue"
  if (-not ($printerName -like "OutQueue*")) {
    try {
      # Installer le driver
      Add-PrinterDriver -Name $driverName -ErrorAction Stop

      # Installer le port
      if ($portAddress -ne "") {
        Add-PrinterPort -Name $portName -PrinterHostAddress $portAddress -ErrorAction Stop
      } else {
        Add-PrinterPort -Name $portName -PrinterHostAddress "localhost" -ErrorAction Stop  # Utilisation de l'adresse locale par défaut
      }

      # Ajouter l'imprimante
      Add-Printer -Name $printerName -DriverName $driverName -PortName $portName -ErrorAction Stop
    } catch {
      Write-Host "Erreur lors de la création de l'imprimante $printerName : $_"
    }
  }
}

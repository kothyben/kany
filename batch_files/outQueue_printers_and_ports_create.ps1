# Liste des noms de répertoire à changer
$repertoires = "AEES_TST", "AURU_TST", "MANUAL_TST", "KIKO_TST", "BOIT_TST"

# Chemin des ports
$chemins_ports = "HKLM:\SYSTEM\CurrentControlSet\Control\Print\Monitors\StreamServe\Ports"

# Boucle pour chaque port
foreach ($repertoire in $repertoires) {

    # Vérifier si le port existe déjà
    if (!(Test-Path "$chemins_ports\$repertoire")) {
        # Créer le port s'il n'existe pas
        New-Item -Path "$chemins_ports\$repertoire" -Force | Out-Null
        Set-ItemProperty -Path "$chemins_ports\$repertoire" -Name "OutputType" -Value 0
        $chemin_fichiers = "E:\STR_SERVICES\editique_$repertoire\input"
        Set-ItemProperty -Path "$chemins_ports\$repertoire" -Name "Path" -Value $chemin_fichiers

        # Ajouter les autres valeurs
        Set-ItemProperty -Path "$chemins_ports\$repertoire" -Name "Beg Seq" -Value ""
        Set-ItemProperty -Path "$chemins_ports\$repertoire" -Name "End Seq" -Value ""
        Set-ItemProperty -Path "$chemins_ports\$repertoire" -Name "AddDocname" -Value 0
        Set-ItemProperty -Path "$chemins_ports\$repertoire" -Name "Adduser" -Value 0
        Set-ItemProperty -Path "$chemins_ports\$repertoire" -Name "AddPrinter" -Value 0
        Set-ItemProperty -Path "$chemins_ports\$repertoire" -Name "ReplaceChar" -Value ""
        Set-ItemProperty -Path "$chemins_ports\$repertoire" -Name "DestFtps" -Value 0
        Set-ItemProperty -Path "$chemins_ports\$repertoire" -Name "DestVerifyHost" -Value 0
        Set-ItemProperty -Path "$chemins_ports\$repertoire" -Name "DestUser" -Value ""
        Set-ItemProperty -Path "$chemins_ports\$repertoire" -Name "DestMoveDir" -Value ""
        Set-ItemProperty -Path "$chemins_ports\$repertoire" -Name "UseNamedPipe" -Value ""
    }

    # Créer un nouveau port
    $portName = $repertoire
    $portType = "StreamServe"
    Add-PrinterPort -Name $portName -PrinterHostAddress $portType

    # Créer une nouvelle imprimante
    $printerName = "OutQueue_$repertoire"
    $shareName = $repertoire
    $printerModel = "Generic / Text Only"
    $portName = $repertoire
    $location = ""
    $comment = ""
    Add-Printer -Name $printerName -ShareName $shareName -DriverName $printerModel -PortName $portName -Location $location -Comment $comment

    # Set the registry values for Description and PortMonitor
    $portRegistryPath = Join-Path $chemins_ports $repertoire
    Set-ItemProperty -Path $portRegistryPath -Name "Description" -Value "StreamServe Port"
    Set-ItemProperty -Path $portRegistryPath -Name "PortMonitor" -Value "strsmon"
}

Write-Host "Done!"

$portsToRemove = "AEES_TST", "AURU_TST", "MANUAL_TST", "KIKO_TST", "BOIT_TST"

foreach ($portToRemove in $portsToRemove) {

    Remove-Printer -Name "OutQueue_$portToRemove" -ErrorAction SilentlyContinue
    
}

Restart-Service Spooler

@echo off
setlocal enabledelayedexpansion

rem Liste des noms de répertoire à changer
set "repertoires=AEES_TST AURU_TST MANUAL_TST KIKO_TST BOIT_TST"

rem Chemin des ports
set "chemins_ports=HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Print\Monitors\StreamServe\Ports"

rem Boucle pour chaque port
for %%i in (%repertoires%) do (
    
    rem Vérifier si le port existe déjà
    reg query "%chemins_ports%\%%i" >nul 2>&1
    if errorlevel 1 (
        rem Créer le port s'il n'existe pas
        reg add "%chemins_ports%\%%i" /f /k
        rem Ajouter la valeur "OutputType"
        reg add "%chemins_ports%\%%i" /v "OutputType" /t REG_DWORD /d 0 /f

        rem Générer le chemin en fonction du répertoire
        set "chemin_fichiers=E:\\STR_SERVICES\\editique_%%i\\input"

        rem Ajouter le chemin des fichiers en tant que valeur "Path"
        reg add "%chemins_ports%\%%i" /v "Path" /t REG_SZ /d "!chemin_fichiers!" /f

        rem Ajouter les autres valeurs
        reg add "%chemins_ports%\%%i" /v "Beg Seq" /t REG_SZ /d "" /f
        reg add "%chemins_ports%\%%i" /v "End Seq" /t REG_SZ /d "" /f
        reg add "%chemins_ports%\%%i" /v "AddDocname" /t REG_SZ /d 0 /f
        reg add "%chemins_ports%\%%i" /v "Adduser" /t REG_SZ /d 0 /f
        reg add "%chemins_ports%\%%i" /v "AddPrinter" /t REG_SZ /d 0 /f
        reg add "%chemins_ports%\%%i" /v "ReplaceChar" /t REG_SZ /d "" /f
        reg add "%chemins_ports%\%%i" /v "DestFtps" /t REG_DWORD /d 0 /f
        reg add "%chemins_ports%\%%i" /v "DestVerifyHost" /t REG_DWORD /d 0 /f
        reg add "%chemins_ports%\%%i" /v "DestUser" /t REG_SZ /d "" /f
        reg add "%chemins_ports%\%%i" /v "DestMoveDir" /t REG_SZ /d "" /f
        reg add "%chemins_ports%\%%i" /v "UseNamedPipe" /t REG_SZ /d "" /f
        rem i do not add this : reg add "%chemins_ports%\%%i" /v "DestPwd" /t REG_BINARY 
    )

    rem Créer un nouveau port
    set "portName=%%i"
    set "portType=StreamServe"
    Add-PrinterPort -Name !portName! -PrinterHostAddress !portType!

    rem Créer une nouvelle imprimante
    set "printerName=OutQueue_%%i"
    set "shareName=%%i"
    set "printerModel=Generic / Text Only"
    set "location="
    set "comment="
    Add-Printer -Name !printerName! -ShareName !shareName! -DriverName !printerModel! -PortName !portName! -Location !location! -Comment !comment!
)

echo Done!

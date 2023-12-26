@echo off
setlocal enabledelayedexpansion

rem Liste des noms de répertoire à changer
set "repertoires=AEES_TST AURU_TST MANUAL_TST KIKO_TST BOIT_TST"

rem Chemin des ports
set "chemins_ports=HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Print\Monitors\StreamServe\Ports"

rem Boucle pour chaque port
for %%i in (%repertoires%) do (
    
    rem Créer le port /k est pour eviter une erreur 
    reg add "%chemins_ports%\%%i" /f /k

    rem Générer le chemin en fonction du répertoire
    set "chemin_fichiers=E:\\STR_SERVICES\\editique_%%i\\input"

    rem Ajouter la valeur "OutputType"
    reg add "%chemins_ports%\%%i" /v "OutputType" /t REG_DWORD /d 0 /f

    rem Ajouter le chemin des fichiers en tant que valeur "Path"
    reg add "%chemins_ports%\%%i" /v "Path" /t REG_SZ /d "!chemin_fichiers!" /f

    rem Ajouter les autres valeurs
    reg add "%chemins_ports%\%%i" /v "Beg Seq" /t REG_SZ /d "" /f
    reg add "%chemins_ports%\%%i" /v "End Seq" /t REG_SZ /d "" /f
    reg add "%chemins_ports%\%%i" /v "AddDocname" /t REG_DWORD /d 0 /f
    reg add "%chemins_ports%\%%i" /v "Adduser" /t REG_DWORD /d 0 /f
    reg add "%chemins_ports%\%%i" /v "AddPrinter" /t REG_DWORD /d 0 /f
    reg add "%chemins_ports%\%%i" /v "ReplaceChar" /t REG_SZ /d "" /f
    reg add "%chemins_ports%\%%i" /v "DestFtps" /t REG_DWORD /d 0 /f
    reg add "%chemins_ports%\%%i" /v "DestVerifyHost" /t REG_DWORD /d 0 /f
    reg add "%chemins_ports%\%%i" /v "DestUser" /t REG_SZ /d "" /f
    reg add "%chemins_ports%\%%i" /v "DestMoveDir" /t REG_SZ /d "" /f
    rem reg add "%chemins_ports%\%%i" /v "UseNamedPipe" /t REG_SZ /d "" /f
    rem reg add "%chemins_ports%\%%i" /v "DestPwd" /t REG_BINARY /d 01000000d08c9ddf0115d1118c7a00c04fc297eb010000008e8be1be9b7c0b49b248ab5f11fde382040000003c000000530074007200650061006d00730065007200760065002000660074007000200075007300650072002000700061007300730077006f00720064000000106600000001000020000000a38e3de5aa6f50558178720d53bd1a4bb39aeda09894ec1d3d0fd92b790031c400000000e8000000020000200000a11d4712c2a01be84fdc2a0c0c411ef8fdc0ac07cefff534dafee2f334663a5e10000000f9e294a7905a9923410cfc1e15b3f46640000000f75dd5bc535ace576baf9acf5df1511196f39ac28ee6b48147dcd23ce3440cb84133cfd22fd09302ee5bb5cf48bd697ab88bf15f39042f10ee9e52516938c43

)


@echo off
setlocal enabledelayedexpansion

rem Liste des noms de répertoire à changer
set "repertoires=AEES_TST AURU_TST MANUAL_TST KIKO_TST BOIT_TST"

rem Boucle pour chaque répertoire
for %%i in (%repertoires%) do (
    rem Définir le nom du service
    set "serviceName=StreamServe%%i"

    rem Supprimer les clés de registre associées au service
    reg delete "HKEY_LOCAL_MACHINE\SOFTWARE\Wow6432Node\StreamServe\Server\2.0\service\!serviceName!" /f
    reg delete "HKEY_USERS\S-1-5-21-2810556606-2836570587-2614408249-500\Software\StreamServe\Server\2.0\!serviceName!" /f
    
    rem Supprimer les clés de registre associées à l'événement du service
    reg delete "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\EventLog\Application\!serviceName!" /f
    reg delete "HKEY_LOCAL_MACHINE\SYSTEM\ControlSet001\Services\EventLog\Application\!serviceName!" /f
    reg delete "HKEY_LOCAL_MACHINE\SYSTEM\ControlSet002\Services\EventLog\Application\!serviceName!" /f
    
    rem Supprimer les clés de registre associées à l'affichage du service
    reg delete "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\!serviceName!" /f
    reg delete "HKEY_LOCAL_MACHINE\SYSTEM\ControlSet001\Services\!serviceName!" /f
    reg delete "HKEY_LOCAL_MACHINE\SYSTEM\ControlSet002\Services\!serviceName!" /f

    echo Service !serviceName! supprimé.
)

echo Suppression des services terminée.

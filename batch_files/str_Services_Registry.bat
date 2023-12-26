@echo off
setlocal enabledelayedexpansion

rem Récupérer les arguments passés au script batch
set "repertoires=%~1"


rem Extraire le dernier numéro de service existant
for /f "tokens=*" %%i in ('reg query "HKEY_LOCAL_MACHINE\SOFTWARE\Wow6432Node\StreamServe\Server\2.0\service" /s ^| findstr /i "service\\" ^| findstr /r "[0-9]*$"') do (
	set /a numService=%%i + 1
)

rem Si aucune clé n'est trouvée, utilisez un numéro de service par défaut
if not defined numService set "numService=1"

rem configure streamedit
reg add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\EventLog\Application\streamedit" /v "EventMessageFile" /t REG_EXPAND_SZ /d "C:\\Program Files (x86)\\StreamServe\\4.1.2\\Server\\strsvc.exe" /f

reg add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\EventLog\Application\streamedit" /v "TypesSupported" /t REG_DWORD /d 7 /f


rem Boucle pour chaque répertoire
for %%i in (%repertoires%) do (
    rem Incrémenter le numéro de service
    set /a "numService+=1"

    rem Créer la sous-clé !numService!
    reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Wow6432Node\StreamServe\Server\2.0\service\!numService!" /v "MaxJobsInMemory" /t REG_DWORD /d 25 /f
	
    rem Ajouter ou mettre à jour les valeurs
    reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Wow6432Node\StreamServe\Server\2.0\service\!numService!" /v "argfile" /t REG_SZ /d "E:\\STR_SERVICES\\\editique_%%i\\export\\generix.arg" /f
    reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Wow6432Node\StreamServe\Server\2.0\service\!numService!" /v "licfile" /t REG_SZ /d "E:\\STR_SERVICES\\editique_Template\\strs.lic" /f
    reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Wow6432Node\StreamServe\Server\2.0\service\!numService!" /v "tmpdir" /t REG_SZ /d "E:\\STR_SERVICES\\editique_%%i\\tmp" /f
    reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Wow6432Node\StreamServe\Server\2.0\service\!numService!" /v "workdir" /t REG_SZ /d "E:\\STR_SERVICES\\editique_%%i\\export" /f

    rem configuration du ProjRoot - celui-ci écrase les anciennes valeurs 
    reg add "HKEY_USERS\S-1-5-21-2810556606-2836570587-2614408249-500\Software\StreamServe\Server\2.0" /v "ProjRoot" /t REG_SZ /d "E:\\STR_SERVICES\\editique_%%i" /f
    reg add "HKEY_USERS\S-1-5-21-2810556606-2836570587-2614408249-500\Software\StreamServe\Server\2.0" /v "ArgPath" /t REG_SZ /d "start.arg" /f
    reg add "HKEY_USERS\S-1-5-21-2810556606-2836570587-2614408249-500\Software\StreamServe\Server\2.0" /v "TmpPath" /t REG_SZ /d "tmp" /f
	
	
    rem Define CurrentControlSet base key and newkey streamserve path 
    set "baseKey=HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\EventLog\Application\StreamServe"
    set "newKey=%baseKey%!numService!"
    
    rem Define ControlSet_001 key and newkey streamserve path 
    set "baseKey_001=HKEY_LOCAL_MACHINE\SYSTEM\ControlSet001\Services\EventLog\Application\StreamServe"
    set "ControlSet_001=%baseKey_001%!numService!"
	
    rem Define ControlSet_002 key and newkey streamserve path 
    set "baseKey_002=HKEY_LOCAL_MACHINE\SYSTEM\ControlSet002\Services\EventLog\Application\StreamServe"
    set "ControlSet_002=%baseKey_002%!numService!"
	
    rem Define eventMessageFile and typesSupported values
    set "eventMessageFile=C:\\Program Files (x86)\\StreamServe\\4.1.2\\Server\\strsvc.exe"
    set "typesSupported=7"
    
    rem Add values to the registry for eventmessagefile
    reg add "%newKey%" /v "EventMessageFile" /t REG_SZ /d "%eventMessageFile%" /f
    reg add "%newKey%" /v "TypesSupported" /t REG_DWORD /d %typesSupported% /f
	
    reg add "%ControlSet_001%" /v "EventMessageFile" /t REG_SZ /d "%eventMessageFile%" /f
    reg add "%ControlSet_001%" /v "TypesSupported" /t REG_DWORD /d %typesSupported% /f
	
    reg add "%ControlSet_002%" /v "EventMessageFile" /t REG_SZ /d "%eventMessageFile%" /f
    reg add "%ControlSet_002%" /v "TypesSupported" /t REG_DWORD /d %typesSupported% /f
	
	
    rem Define displaynamekey paths
    set "displaynamekey=HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\StreamServe"
    set "displaykey=%displaynamekey%!numService!"
	
    set "displaynamekey_001=HKEY_LOCAL_MACHINE\SYSTEM\ControlSet001\Services\StreamServe"
    set "displaykey_001=%displaynamekey_001%!numService!"
	
    set "displaynamekey_002=HKEY_LOCAL_MACHINE\SYSTEM\ControlSet002\Services\StreamServe"
    set "displaykey_002=%displaynamekey_002%!numService!"
	
    set "imagepath=C:\\Program Files (x86)\\StreamServe\\4.1.2\\Server\\strsvc.exe"
	
    rem add displayname relative to internal name Streamserve
    reg add %displaykey% /v "DisplayName" /d "StreamServe %%i" /t REG_SZ /f
    reg add %displaykey% /v "ObjectName" /d "LocalSystem" /t REG_SZ /f
    reg add %displaykey% /v "Type" /t REG_DWORD /d 272 /f
    reg add %displaykey% /v "Start" /t REG_DWORD /d 3 /f
    reg add %displaykey% /v "ErrorControl" /t REG_DWORD /d 1 /f
    reg add %displaykey% /v "ImagePath" /t REG_EXPAND_SZ /d "%imagepath%" /f
    reg add %displaykey% /v "WOW64" /t REG_DWORD /d 332 /f
	
    reg add %displaykey_001% /v "DisplayName" /d "StreamServe %%i" /t REG_SZ /f
    reg add %displaykey_001% /v "ObjectName" /d "LocalSystem" /t REG_SZ /f
    reg add %displaykey_001% /v "Type" /t REG_DWORD /d 272 /f
    reg add %displaykey_001% /v "Start" /t REG_DWORD /d 3 /f
    reg add %displaykey_001% /v "ErrorControl" /t REG_DWORD /d 1 /f
    reg add %displaykey_001% /v "ImagePath" /t REG_EXPAND_SZ /d "%imagepath%" /f
    reg add %displaykey_001% /v "WOW64" /t REG_DWORD /d 332 /f
	
    reg add %displaykey_002% /v "DisplayName" /d "StreamServe %%i" /t REG_SZ /f
    reg add %displaykey_002% /v "ObjectName" /d "LocalSystem" /t REG_SZ /f
    reg add %displaykey_002% /v "Type" /t REG_DWORD /d 272 /f
    reg add %displaykey_002% /v "Start" /t REG_DWORD /d 3 /f
    reg add %displaykey_002% /v "ErrorControl" /t REG_DWORD /d 1 /f
    reg add %displaykey_002% /v "ImagePath" /t REG_EXPAND_SZ /d "%imagepath%" /f
    reg add %displaykey_002% /v "WOW64" /t REG_DWORD /d 332 /f
	
	

)
rem run control center 
rem start "" "C:\Program Files (x86)\StreamServe\4.1.2\Common\controlcenter.exe"

rem Wait for Control Center to start
rem timeout /t 5


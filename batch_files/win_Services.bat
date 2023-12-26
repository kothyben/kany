@echo off
setlocal enabledelayedexpansion

rem Récupérer les arguments passés au script batch - Le nom des repertoires editiques
set "repertoires=%~1"

rem Exécutable 
set "Executable=C:\\Program Files (x86)\\StreamServe\\4.1.2\\Server\\strsvc.exe"

rem Compteur pour les services
set "count=1"

rem Boucle pour chaque répertoire
for %%i in (%repertoires%) do (
    set "directoryName=%%i"

    REM Step 1: Create the service
    sc create "StreamServe!count!" binPath= "%Executable%" DisplayName= "StreamServe!count!"

    REM Step 2: Configure the service to start automatically
    sc config "StreamServe!count!" start= auto
	
	REM Configure the DislayName 
    sc config "StreamServe!count!" DisplayName= "StreamServe StreamServe !directoryName!"

    REM Step 4: Stop the service
    sc stop "StreamServe!count!"

    REM Increment the counter
    set /a "count+=1"
)

REM Step 3: Start the services
for /l %%i in (1,1,%count%) do (
    sc start "StreamServe%%i"
    echo Service StreamServe%%i is started.
)


rem Attempt to stop Control Center
taskkill /f /im controlcenter.exe 2>nul

rem Check the errorlevel to see if a process was terminated
if errorlevel 1 (
    echo Control Center was not running.
) else (
    echo Control Center terminated successfully.
)

rem Command to start Control Center
rem start "" "C:\Program Files (x86)\StreamServe\4.1.2\Common\controlcenter.exe"

rem Wait for Control Center to start
rem timeout /t 5




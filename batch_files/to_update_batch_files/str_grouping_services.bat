@echo off

REM key of groups 
set "repo_groups=HKEY_LOCAL_MACHINE\SOFTWARE\Wow6432Node\StreamServe\ProcessManager\Groups"

REM group I am looking for  
set "check_group=TestGroup"

REM Enable delayed expansion
setlocal enabledelayedexpansion

REM Services and their DisplayNames
set "services=AEES_TST AURU_TST MANUAL_TST BOIT_TST KIKO_TST"

REM Create group if not exists
if not exist "%repo_groups%\%check_group%" (
    REM Create the new group if it doesn't exist
    reg add "%repo_groups%\%check_group%" /v %check_group% /t REG_SZ /f
    echo Group %check_group% is created.
	
	REM Add services to this group
	for %%i in (%services%) do (
		sc query state= all | findstr /i /c:"%%i" >nul 2>&1
		if !errorlevel! equ 0 (
			REM Service exists, add it to the group // add string value 
			reg add "%repo_groups%\%check_group%" /v "StreamServe %%i" /t REG_SZ /d "" /f
			echo Added %%i to %check_group%
		) else (
			echo Error: %%i does not exist or could not be queried. Please create it first.
		)
	)	
else (
		echo Group %check_group% already exists.
		for %%i in (%services%) do (
		sc query state= all | findstr /i /c:"%%i" >nul 2>&1
		if !errorlevel! equ 0 (
			REM Service exists, add it to the group // add string value 
			reg add "%repo_groups%\%check_group%" /v "StreamServe %%i" /t REG_SZ /d "" /f
			echo Added %%i to %check_group%
		) else (
			echo Error: %%i does not exist or could not be queried. Please create it first.
		)
	)	
		
	)
)

REM Disable delayed expansion
endlocal

echo Done.

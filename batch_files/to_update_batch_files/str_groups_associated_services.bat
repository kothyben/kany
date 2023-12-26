@echo off
setlocal enabledelayedexpansion

Rem key of groups
set repo_groups="HKEY_LOCAL_MACHINE\SOFTWARE\Wow6432Node\StreamServe\ProcessManager\Groups"

Rem Extract JSON data passed from Ansible
set "ansible_data=%*"

Rem Parse JSON data to retrieve groups and associated services
for /f "tokens=1,* delims=:" %%a in ("%ansible_data%") do (
    Rem Extract the group name
    set "group_name=%%a"

    Rem Extract services for the current group
    set "services=%%b"
    
    Rem Create the group if it doesn't exist
    reg query %repo_groups%\!group_name! >nul 2>&1
    if errorlevel 1 (
        reg add %repo_groups%\!group_name! /t REG_SZ /f >nul 2>&1
        echo Created group !group_name!
    )
    
    Rem Loop through services and add them to the group
    for %%S in (!services!) do (
        Rem Check if service exists and add it to the group
        sc query state= all | findstr /i /c:"%%S" >nul 2>&1
        if !errorlevel! equ 0 (
            REM Service exists, add it to the group // add string value
            reg add "%repo_groups%\!group_name!" /v "%%S" /t REG_SZ /d "" /f >nul 2>&1
            echo Added %%S to !group_name!
        ) else (
            echo Error: %%S does not exist or could not be queried. Please create it first.
        )
    )
)

echo Done.

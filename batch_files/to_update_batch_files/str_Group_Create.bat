@echo off
setlocal enabledelayedexpansion

Rem key of groups
set repo_groups="HKEY_LOCAL_MACHINE\SOFTWARE\Wow6432Node\StreamServe\ProcessManager\Groups"

Rem Groups to be created are added as arguments to this script
set "groups_services=%*"

Rem Check for each groups_services if the group exists
for %%G in (%groups_services%) do (
    rem Strip quotes around group names
    set "group_name=%%~G"
    reg query %repo_groups%\!group_name! >nul 2>&1
    if errorlevel 1 (
        REM Create the new group if it doesn't exist
        rem Traiter les groupes avec deux mots ici
        if not "%%~G" == "" (
            reg add %repo_groups%\!group_name! /t REG_SZ /f
        )
    )
)
echo Done.

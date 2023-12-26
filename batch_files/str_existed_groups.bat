@echo off
setlocal EnableDelayedExpansion

REM Define the registry key path
set "repo_groups=HKEY_LOCAL_MACHINE\SOFTWARE\Wow6432Node\StreamServe\ProcessManager\Groups"

REM Initialize a counter for dictionary keys
set count=0

REM Create an empty dictionary
set "dictionary="

REM Query the registry for the list of groups and extract the group name
for /f "tokens=*" %%G in ('reg query "%repo_groups%"') do (
    set "registry_path=%%G"
    REM Extract the last part of the registry path (group name)
    for %%I in ("!registry_path!") do set "group_name=%%~nxI"

    REM Add the group name to the dictionary
    set /a count+=1
    set "dictionary[!count!]=!group_name!"

    REM Query and display values for each group
    reg query "!registry_path!" /s
    echo.
)

endlocal

@echo off
setlocal EnableDelayedExpansion

REM Define the registry key path
set "repo_groups=HKEY_LOCAL_MACHINE\SOFTWARE\Wow6432Node\StreamServe\ProcessManager\Groups"

Rem Initialize a counter for dictionary keys
set count=0

Rem Create an empty dictionary
set "dictionary="

Rem Query the registry for the list of groups and extract the group name
for /f "tokens=*" %%G in ('reg query "%repo_groups%"') do (
    set "registry_path=%%G"
   
     Rem Extract the last part of the registry path (group name)
    for %%I in ("!registry_path!") do set "group_name=%%~nxI"
   
    Rem Add the group name to the dictionary
    set /a count+=1
    set "dictionary[!count!]=!group_name!"
)

Rem Display the dictionary
for /l %%N in (1,1,!count!) do (
    echo Group %%N: !dictionary[%%N]!
)

endlocal


   



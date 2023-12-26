@echo off
set "regKey=HKEY_LOCAL_MACHINE\SOFTWARE\Wow6432Node\StreamServe\ProcessManager\Groups"

echo Suppression des SOUS-CLES de %regKey% ...

for /f "tokens=*" %%a in ('reg query "%regKey%" /s /f "*" ^| findstr /i "HKEY_LOCAL_MACHINE"') do (
    reg delete "%%a" /f
)

echo TOUTES LES SOUS-CLES  %regKey% ONT ETE SUPPRIMEES AVEC SUCCES


param(
    [string]$ansibleData
)

# Convertir le contenu du fichier JSON directement en objet PowerShell
$jsonData = Get-Content -Path $ansibleData | ConvertFrom-Json

# Clé des groupes
$repoGroups = "HKLM:\SOFTWARE\Wow6432Node\StreamServe\ProcessManager\Groups"

foreach ($groupData in $jsonData) {
    $groupName = $groupData.group
    $services = $groupData.services

    # Créer le groupe s'il n'existe pas
    if (-not (Test-Path "$repoGroups\$groupName")) {
        New-Item -Path "$repoGroups\$groupName" -ItemType "String" -Force | Out-Null
        Write-Output "Created group $groupName"
    }

    # Ajouter les services au groupe
    foreach ($service in $services) {
        $serviceName = $service.Trim('" ')
        if ($serviceName -ne "") {
            New-ItemProperty -Path "$repoGroups\$groupName" -Name $serviceName -Value "" -PropertyType String -Force | Out-Null
            Write-Output "Added $serviceName to $groupName"
        }
    }
}

Write-Output "Done."

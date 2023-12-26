for ($i = 0; $i -lt 10; $i++) {
    $serviceName = "StreamServe$i"

    # Vérifier si le service existe
    $service = Get-Service -Name $serviceName -ErrorAction SilentlyContinue

    if ($null -ne $service) {
        # Le service existe, essayez de l'arrêter
        Stop-Service -Name $serviceName -ErrorAction SilentlyContinue
        Write-Host "Service $serviceName arrêté."

        # Attendez que le service soit complètement arrêté (ajustez si nécessaire)
        while ((Get-Service -Name $serviceName).Status -ne 'Stopped') {
            Start-Sleep -Seconds 1
        }

        # Supprimez le service en utilisant sc.exe
        sc.exe delete $serviceName
        Write-Host "Service $serviceName supprimé."
    } else {
        # Le service n'existe pas, passez à l'itération suivante
        Write-Host "Le service $serviceName n'existe pas"
    }
}

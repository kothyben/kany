import subprocess

def synchronize_files(source_path, destination_path, username, password):
    try:
        # Ajout des informations d'authentification au gestionnaire de mots de passe
        cmdkey_cmd = f'cmdkey /add:{destination_path} /user:{username} /pass:{password}'
        subprocess.run(cmdkey_cmd, shell=True, check=True)

        # Exécution de la commande robocopy avec les informations d'authentification
        robocopy_cmd = f'robocopy "{source_path}" "{destination_path}" /E /MIR /R:3 /W:1 /NFL /NDL /NJH /NJS'
        subprocess.run(robocopy_cmd, shell=True, check=True)

        print("Synchronisation réussie !")
    except subprocess.CalledProcessError as e:
        print("Erreur lors de la synchronisation :", e)

if __name__ == "__main__":
    # Spécifiez le chemin du répertoire source, le chemin du répertoire de destination, et les informations d'authentification
    source_path = r"C:\Chemin_vers_le_repertoire_source"
    destination_path = r"\\NOM_DU_SERVEUR\Chemin_vers_le_repertoire_destination"
    username = "votre_nom_d_utilisateur"
    password = "votre_mot_de_passe"

    synchronize_files(source_path, destination_path, username, password)


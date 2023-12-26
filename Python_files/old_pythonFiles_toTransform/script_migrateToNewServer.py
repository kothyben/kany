"""
    Ce script copie les dossiers directement d'un serveur windows vers un autre serveur windows 
    il crée un dossier dans la machine de destination  dans lequel  il copie les fichies
    il crée aussi une sauvegarde automatique backup 
    Il se lance depuis la machine source
"""

import os
import shutil

def migrate_to_new_servers(source_dir, destination_server, username, password):
    try:
        # Vérifie si le répertoire de destination existe sur le serveur de destination, sinon le crée
        if not os.path.exists(destination_server):
            os.makedirs(destination_server)

        # Exemple : Utilisation de shutil.copytree pour copier les fichiers sauvegardés vers le serveur de destination
        shutil.copytree(source_dir, destination_server)

        print("Migration réussie vers les nouveaux serveurs !")
    except Exception as e:
        print("Erreur lors de la migration :", e)

# Backup
def backup_files(source_dir, backup_dir):
    try:
        # Vérifie si le répertoire de sauvegarde existe, sinon le crée
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)

        # Copie récursive des fichiers et répertoires du répertoire source vers le répertoire de sauvegarde
        shutil.copytree(source_dir, os.path.join(backup_dir, os.path.basename(source_dir)))

        print("Sauvegarde réussie !")
    except Exception as e:
        print("Erreur lors de la sauvegarde :", e)


if __name__ == "__main__":
    # Spécifiez le répertoire que vous souhaitez sauvegarder et le répertoire de sauvegarde
    source_directory = "Chemin_vers_le_répertoire_à_sauvegarder"
    backup_directory = "Chemin_vers_le_répertoire_de_sauvegarde"

    # Spécifiez les informations pour les nouveaux serveurs de destination
    destination_server = "\\\\LWX-CZ3BZ33\\Users\adl_akoki\Desktop\\LocalFolders"  # UNC path
    username = "adl_akoki"
    password = "votre_mot_de_passe"

    # Étape 1 : Sauvegarde des fichiers importants avant la migration
    backup_files(source_directory, backup_directory)

    # Étape 2 : Migration vers les nouveaux serveurs en utilisant les partages réseau
    migrate_to_new_servers(backup_directory, destination_server, username, password)


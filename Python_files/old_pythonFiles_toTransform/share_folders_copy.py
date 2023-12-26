"""
    Ce script permet de partager un dossier avec tous les privilèges
    Le dossier est accessible à tout le monde (rwx)
"""

import subprocess
import pandas as pd
import os
import logging
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="Partager un dossier avec tous les privilèges.")
    parser.add_argument("--name_backup_temp_folder", type=str, help="Nom du dossier à partager")
    return parser.parse_args()


def share_folder(share_name):
    # Obtenez dynamiquement le nom d'utilisateur de la machine
    username = os.getlogin()
    folder_path = os.path.join(r"C:\Users", username, f"Desktop\\{share_name}")

    # Créez le dossier de sauvegarde s'il n'existe pas
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    try:
        create_share_cmd = f'net share {share_name}="{folder_path}" /GRANT:Everyone,FULL'
        subprocess.run(create_share_cmd, shell=True, check=True)
        print(f"Le dossier '{folder_path}' a été partagé sous le nom '{share_name}' avec un accès complet pour tout le monde.")

        # Exporter un résultat de réussite 
        data = {"Sharing": "OK"}
        df = pd.DataFrame(data)
        df.to_csv('OK_shared.csv', index=False)

    except subprocess.CalledProcessError as e:
        error_message = f"Erreur lors du partage du dossier: {str(e)}"
        print(error_message)
        logging.error(error_message)

        # Exporter un résultat signalant une erreur
        data2 = {"Sharing": "KO",  "Error" : error_message}
        df = pd.DataFrame(data2)
        df.to_csv('KO_share.csv', index=False)


if __name__ == "__main__":
    args = parse_args()
    share_name = args.name_backup_temp_folder
    share_folder(share_name)

"""
    Ce script permet de partager un dossier avec tous les privilèges
    Le dossier est accessible  tout le monde (rwx)

"""

import subprocess
import pandas as pd
import os
import logging
import argparse

def share_folder(share_name):
    # Obtenez dynamiquement le nom d'utilisateur de la machine
    username = os.getlogin()
    folder_path = os.path.join(r"C:\Users", username, "Desktop\\temp_folder")

    if not os.path.exists(folder_path):
        print(f"Le dossier '{folder_path}' n'existe pas.")
        return

    try:
        create_share_cmd = f'net share {share_name}="{folder_path}" /GRANT:Everyone,FULL'
        subprocess.run(create_share_cmd, shell=True, check=True)
        print(f"Le dossier '{folder_path}' partageé sous le nom '{share_name}' avec tous les droits  pour tout le monde.")

        # Exporter un résultat de reussite 
        data = {"Sharing": "OK"}
        df = pd.DataFrame(data)
        df.to_csv('OK_shared.csv', index=False)

    except subprocess.CalledProcessError as e:
        error_message = f"Erreur lors du partage du dossier: {str(e)}"
        print(error_message)
        logging.error(error_message)

        # Exporter un résultat signalant error
        data2 = {"Sharing": "KO",  "Error" : error_message}
        df = pd.DataFrame(data2)
        df.to_csv('KO_share.csv', index=False)

if __name__ == "__main__":
    share_name = "SharingTempFolder"
    share_folder(share_name)


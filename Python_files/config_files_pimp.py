"""
Ce script copie tous les fichiers et dossiers importants que nous avons choisis
puis retranscrit ses informations dans un fichier csv copy_Log.csv.

Tous ses fichiers et dossiers sont copiés dans le dossier backup qui est le dossier partagé temp_folder

Si le script rencontre une erreur lors de la copie il passe sur la copie suivante du fichier ou du dossier
Dans le fichier copy_log il inscrit tous les dossiers et fichiers copiés et non copié

A la fin il doit classer tous ses sous dossiers et fichiers dans un dossier 
nommé comme le dossier parent correspondant.

NB: CE SCRIPT TIENT AUSSI COMPTE D'UNE CONDITION IMPORTANTE CELLE DE LA TAILLE RESTANTE DU DISK AVANT ET PENDANT LA COPIE 
"""

import os
import shutil
import pandas as pd
import psutil
import platform
import argparse

def get_rest_disk():
    partitions = psutil.disk_partitions()
    disk_partitions = []
    total_disks = []
    used_disks = []
    percentages = []

    for partition in partitions:
        if platform.system() == "Windows" and "fixed" in partition.opts:
            disk_usage = psutil.disk_usage(partition.mountpoint)
            total_disk = round(disk_usage.total / (1024 ** 3), 2)  # Conversion en Go
            used_disk = round(disk_usage.used / (1024 ** 3), 2)    # Conversion en Go
            pourcentage = round(disk_usage.percent, 2)             # Pourcentage d'utilisation du disque
            rest_disk = round((total_disk - used_disk), 2)
            
            disk_partitions.append(partition.device)
            total_disks.append(total_disk)
            used_disks.append(used_disk)
            percentages.append(pourcentage)

    return rest_disk

def detect_system_config_files():
    config_folders = [
        "E:\\STR_SERVICES\\"
    ]
    important_config_folders = []

    for folder_path in config_folders:
        if os.path.exists(folder_path):
            important_config_folders.append(folder_path)

    return important_config_folders

def copy_folders_and_files_with_space_check(source, destination, remaining_space_limit):
    for item in os.listdir(source):
        source_item = os.path.join(source, item)
        destination_item = os.path.join(destination, item)
        
        rest_disk = get_rest_disk()
        if rest_disk <= remaining_space_limit:
            print(f"Arrêt de la copie car l'espace disque restant est inférieur à {remaining_space_limit} Go.")
            return
        
        try:
            if os.path.isdir(source_item):
                shutil.copytree(source_item, destination_item)
            else:
                shutil.copy2(source_item, destination_item)  # Utilise copy2 pour conserver les métadonnées
            print(f"Copy of {item} successful!")
            
            data = {"Copy": "OK", "Name_Folder_or_File": os.path.basename(source_item)}
            df = pd.DataFrame(data, index=[0])
            df.to_csv('Copy_Log.csv', mode='a', header=not os.path.exists('Copy_Log.csv'), index=False)
        except Exception as e:
            print(f"Error during copy of {item}:", e)

if __name__ == "__main__":
    default_folders = ["E:\\STR_SERVICES\\"]

    parser = argparse.ArgumentParser(description='Copier des dossiers.')
    parser.add_argument('dossiers', nargs='*', default=default_folders, help='Liste des dossiers à copier.')
    args = parser.parse_args()

    important_config_folders = args.dossiers

    if important_config_folders:
        print("Detected important system and configuration folders:")
        for folder_path in important_config_folders:
            print(folder_path)
            username = os.getenv('USERNAME')
            destination_folder = f"C:\\Users\\{username}\\Desktop\\temp_folder\\"
            parent_folder_name = os.path.basename(folder_path)
            new_destination = os.path.join(destination_folder, parent_folder_name)
            copy_folders_and_files_with_space_check(folder_path, new_destination, remaining_space_limit=1)  # Modifier la limite d'espace restant selon vos besoins
    else:
        print("No important system and configuration folders detected.")


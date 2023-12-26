"""
    Ce script copie tous les fichiers et dossiers  importants que nous avons choisis
    puis retranscrit ses informations dans un fichier csv copy_Log.csv.

    Tous ses fichiers et dossiers sont copiés dans le dossier backup qui est le dossier partagé temp_folder

    Si le script rencontre une erreur lors de la copie il passe sur la copie suivante du fichier ou du dossier
    Dans le fichier copy_log il inscrit tous les dossiers et fichiers copiés et non copié

    A la fin il  doit classer tous ses sous dossiers et fichiers dans un dossier 
    nommé comme le dossier parent correspondant.

"""
import os
import shutil
import pandas as pd

def detect_system_config_files():
    config_folders = [
            "E:\\STR_SERVICES\\"
    ]
    important_config_folders = []

    for folder_path in config_folders:
        if os.path.exists(folder_path):
            important_config_folders.append(folder_path)

    return important_config_folders

def copy_folders_and_files(source, destination):
    # Pour chaque élément dans le dossier source
    for item in os.listdir(source):
        source_item = os.path.join(source, item)
        destination_item = os.path.join(destination, item)
        
        # Copier le contenu dans la destination
        try:
            if os.path.isdir(source_item):
                shutil.copytree(source_item, destination_item)
            else:
                shutil.copy2(source_item, destination_item)  # Utilise copy2 pour conserver les métadonnées
            print(f"Copy of {item} successful!")
            
            # Enregistrement du statut de la copie dans le fichier CSV
            data = {"Copy": "OK", "Name_Folder_or_File": os.path.basename(source_item)}
            df = pd.DataFrame(data, index=[0])
            df.to_csv('Copy_Log.csv', mode='a', header=not os.path.exists('Copy_Log.csv'), index=False)
        except Exception as e:
            print(f"Error during copy of {item}:", e)

if __name__ == "__main__":
    important_config_folders = detect_system_config_files()
    if important_config_folders:
        print("Detected important system and configuration folders:")
        for folder_path in important_config_folders:
            print(folder_path)
            destination_folder = "C:\\Users\\Administrator\\Desktop\\temp_folder\\"
            parent_folder_name = os.path.basename(folder_path)
            new_destination = os.path.join(destination_folder, parent_folder_name)
            copy_folders_and_files(folder_path, new_destination)
    else:
        print("No important system and configuration folders detected.")

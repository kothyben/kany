"""
    Ce script copie tous les fichiers et dossiers  editiques  que nous avons choisis
    puis retranscrit ses informations dans un fichier csv copy_Log.csv.

    il ignore le dossier editique_RXIT_TST
    Tous ses fichiers et dossiers sont copiés dans le dossier backup qui est le dossier partagé temp_folder

    Si le script rencontre une erreur lors de la copie il passe sur la copie suivante du fichier ou du dossier
    Dans le fichier copy_log il inscrit tous les dossiers et fichiers copiés et non copié

    A la fin il  doit classer tous ses sous dossiers et fichiers dans un dossier 
    nommé comme le dossier parent correspondant.

"""
import os
import shutil
import pandas as pd

def detect_system_config_folders():
    config_folders = [
        "E:\\STR_SERVICES\\"
    ]
    important_config_folders = []

    for folder_path in config_folders:
        if os.path.exists(folder_path):
            important_config_folders.append(folder_path)

    return important_config_folders

def initialize_log_file():
    header = ["Copy", "Name_Folder_or_File"]
    df = pd.DataFrame(columns=header)
    df.to_csv('Copy_eqitique_Log.csv', mode='w', header=True, index=False)

def copy_folders_and_files(source, destination):
    initialize_log_file()  # Initialize log file once
    # For each element in the source folder
    for item in os.listdir(source):
        source_item = os.path.join(source, item)
        destination_item = os.path.join(destination, item)

        try:
            if os.path.isdir(source_item):
                # Check if the folder name is NOT "editique_RXIT_TST"
                if os.path.basename(source_item) != "editique_RXIT_TST":
                    shutil.copytree(source_item, destination_item)
            else:
                shutil.copy2(source_item, destination_item)  # Use copy2 to preserve metadata
            print(f"Copy of {item} successful!")

            # Log the status of the copy operation in the CSV file
            data = {"Copy": "OK", "Name_Folder_or_File": os.path.basename(source_item)}
            df = pd.DataFrame(data, index=[0])
            df.to_csv('Copy_eqitique_Log.csv', mode='a', header=False, index=False)
        except Exception as e:
            print(f"Error during copy of {item}: {e}")
            # Log the error in the CSV file
            data = {"Copy": "Error", "Name_Folder_or_File": os.path.basename(source_item)}
            df = pd.DataFrame(data, index=[0])
            df.to_csv('Copy_eqitique_Log.csv', mode='a', header=False, index=False)

if __name__ == "__main__":
    important_config_folders = detect_system_config_folders()
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

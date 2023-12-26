""" 
    Ce script synchronise 2 dossiers dans 2 machines distinctes windows 
    qui comminiquement  ensemble. 
    Il est préférable de lancer depuis la machine source 
    mais nous lanàns depuis la machine de destination puisque nous ne convertissons pa le fichier en .exe
    
"""
import subprocess
import pandas as pd
import os
import threading

# Définissez une variable globale pour le verrouillage
synchronization_lock = threading.Lock()

def synchronize_files(source_path, destination_path, source_username, source_password):
    try:
        drive_letter = 'Z:'  # Vous pouvez choisir une lettre de lecteur disponible

        # Vérifiez si le lecteur Z: est déjà mappé en utilisant la commande "net use"
        check_command = f"net use {drive_letter}"
        check_output = subprocess.run(check_command, shell=True, stderr=subprocess.PIPE, text=True)

        # Si le lecteur Z: est déjà mappé, déconnectez-le
        if check_output.returncode == 0:
            unmap_command = f"net use {drive_letter} /delete"
            subprocess.run(unmap_command, shell=True, check=True)
        else:
            print(f"Le lecteur {drive_letter} n'est pas mappé.")

        # Mappez le lecteur réseau distant sur votre machine
        map_command = f"net use {drive_letter} {source_path} /user:{source_username} {source_password}"
        subprocess.run(map_command, shell=True, check=True)

        # Exécution de la commande robocopy en utilisant le lecteur mappé
        mapped_source_path = os.path.join(drive_letter, '')  # Ajoutez '\' à la fin pour le chemin mappé
        robocopy_command = (
            f"robocopy \"{mapped_source_path}\" \"{destination_path}\" /E /MIR /R:3 /W:1 /NFL /NDL /NJH /NJS"
        )
        
        # Avant de commencer la synchronisation, obtenez le verrou
        with synchronization_lock:
            subprocess.run(robocopy_command, shell=True, check=True)

        # Déconnectez le lecteur réseau après la synchronisation
        unmap_command = f"net use {drive_letter} /delete"
        subprocess.run(unmap_command, shell=True, check=True)

        print("Synchronisation réussie !")
        data = {"Synchro": ["OK"]}
        df = pd.DataFrame(data)
        df.to_csv('OK_synchro.csv', index=False)

    except subprocess.CalledProcessError as e:
        print("Erreur lors de la synchronisation :", e)
        data = {"Synchro": ["KO"], "Error": [str(e)]}
        df = pd.DataFrame(data)
        df.to_csv('KO_Synchro.csv', index=False)

        # Déconnectez le lecteur réseau après la synchronisation
        unmap_command = f"net use {drive_letter} /delete"
        subprocess.run(unmap_command, shell=True, check=True)

if __name__ == "__main__":
    # Spécifiez le chemin du répertoire source, le chemin du répertoire de destination,
    # le nom d'utilisateur et le mot de passe
    source_path = r"\\STR-MUT-TEST2\Users\Administrator\Desktop\temp_folder"
    destination_path = r"C:\Users\admin\Desktop\temp_folder"
    source_username = "Administrator"  # Remplacez par le nom d'utilisateur
    source_password = "*********************"  # Remplacez par le mot de passe

    # Déconnectez le lecteur réseau après la synchronisation
    drive_letter = 'Z:'  # Vous pouvez choisir une lettre de lecteur disponible
    unmap_command = f"net use {drive_letter} /delete"
    subprocess.run(unmap_command, shell=True, check=True)

    synchronize_files(source_path, destination_path, source_username, source_password)

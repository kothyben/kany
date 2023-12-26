import os
import sys

def main(chemin):
    if not os.path.isdir(chemin):
        print(f"Le chemin spécifié ({chemin}) n'est pas un répertoire valide.")
        return

    for root, dirs, files in os.walk(chemin):
        for printer_path in dirs:
            ps1_files = [
                file for file in os.listdir(os.path.join(root, printer_path))
                if file.endswith(".ps1") and os.path.isfile(os.path.join(root, printer_path, file))
            ]

            if ps1_files:
                for ps1_file in ps1_files:
                    print(f"Execution du fichier {os.path.join(root, printer_path, ps1_file)}")
                    os.system(f"powershell.exe -File {os.path.join(root, printer_path, ps1_file)}")
            else:
                print(f"Aucun fichier .ps1 trouvé dans {os.path.join(root, printer_path)}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py str_drivers_paths")
    else:
        chemin = sys.argv[1]

        main(chemin)

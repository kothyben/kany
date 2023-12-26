import os
import sys

def main(fileRepository_Pilotes):
    if not os.path.isdir(fileRepository_Pilotes):
        print(f"Le fileRepository_Pilotes spécifié ({fileRepository_Pilotes}) n'est pas un répertoire valide.")
        return

    for root, dirs, files in os.walk(fileRepository_Pilotes):
        for pilotes_dir in dirs:
            Inf_files = [
                file for file in os.listdir(os.path.join(root, pilotes_dir))
                if file.endswith(".inf") and os.path.isfile(os.path.join(root, pilotes_dir, file))
            ]

            if Inf_files:
                for inf_file in Inf_files:
                    print(f"Execution du fichier {os.path.join(root, pilotes_dir, inf_file)}")
                    os.system(f" pnputil.exe -i -a  {os.path.join(root, pilotes_dir, inf_file)}")
            else:
                print(f"Aucun fichier .inf trouvé dans {os.path.join(root, pilotes_dir)}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py pilotes_dir")
    else:
        fileRepository_Pilotes = sys.argv[1]

        main(fileRepository_Pilotes)


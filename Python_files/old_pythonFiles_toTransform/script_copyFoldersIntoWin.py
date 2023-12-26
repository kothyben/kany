""" 
    This script takes directories, subdirectories and files into selected directories
    It does not take files in the directory where i only selected some subdirectories
    if i select one directory it takes all contents of this directory
    
"""

import os
import shutil

def explore_and_copy(source_dir, selected_folders):
    base_name = os.path.basename(source_dir)
    #target_dir = os.path.join(os.path.dirname(source_dir), base_name + "_copie")
    #target_dir = r"C:\Users\Administrator\Desktop\temp_folder"
    target_dir = r'\\192.168.29.1\Global_Share\STR\TESTK'

    # Create the base target directory if it doesn't exist
    os.makedirs(target_dir, exist_ok=True)

    for root, dirs, files in os.walk(source_dir):
        # Get the relative path from the source directory
        relative_path = os.path.relpath(root, source_dir)

        # Check if the current directory is one of the selected subfolders
        if any(selected_folder in relative_path for selected_folder in selected_folders):
            target_path = os.path.join(target_dir, relative_path)
            os.makedirs(target_path, exist_ok=True)

            # Copy files in the current directory to the target directory
            for file in files:
                source_file = os.path.join(root, file)
                target_file = os.path.join(target_path, file)
                shutil.copy2(source_file, target_file)

if __name__ == "__main__":

    # Replace these variables with your desired paths and folder names
    source_directory = "E:\STR_SERVICES"
    selected_subfolders = ["editique_VEFR_TST",  "drivers", "exported_configurations"]

    explore_and_copy(source_directory, selected_subfolders)


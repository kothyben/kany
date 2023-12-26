"""
  
    This script to traverse the given directory tree 
    and copy only the files (not the directories) to a new target directory


"""

import os
import shutil

def explore_and_copy_files(source_dir, target_dir):
    # Create the target directory if it doesn't exist
    os.makedirs(target_dir, exist_ok=True)

    for root, dirs, files in os.walk(source_dir):
        for file in files:
            source_file = os.path.join(root, file)
            shutil.copy2(source_file, target_dir)

if __name__ == "__main__":
    # Replace these variables with your desired paths
    source_directory = "folders"
    target_directory = "{}_copie_files".format(source_directory)

    explore_and_copy_files(source_directory, target_directory)

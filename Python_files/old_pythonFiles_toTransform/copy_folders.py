import shutil, os

# ---------directories'
source_directory = r'E:\Testdrivers'
destination_directory = r'C:\Users\Administrator\Desktop\temp_folder'
#destination_directory = r'\\192.168.29.1\Global_Share\STR\TESTK'

# --------------Create directory where i copy first
dstDir = destination_directory
def createDir(dstDir):
    # Check if dst path exists
    if os.path.isdir(dstDir) == False:
        # Create all the dierctories in the given path
        os.makedirs(dstDir); 
    return None
    
createDir(dstDir)


# ---------------Function copy folders from one to another 
def copy_folders(src_dir, dest_dir):
    try:
        # Remove the destination directory if it exists
        shutil.rmtree(dest_dir, ignore_errors=True)

        # Copy the entire directory from source to destination
        shutil.copytree(src_dir, dest_dir)

        print("Folder migration successful!")
    except Exception as e:
        print("An error occurred during folder migration:", str(e))

copy_folders(source_directory, destination_directory)

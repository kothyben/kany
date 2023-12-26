#-------------------------------------------------- VARIABLES GLOBALES REMOTE ----------------------------------
# librairies 
import os
import random
import pandas as pd

# List of packages to check
required_packages = ['win32print', 'shutil', 'glob', 'wmi']

missing_packages = []
for package in required_packages:
    try:
        exec(f'import {package}')
    except ImportError:
        missing_packages.append(package)

if missing_packages:
    # Handle the case when packages are missing
    print("The following packages are missing or not available:", missing_packages)
    # Install alternative packages or perform alternative actions for each missing package


# Get Server Name
try:
    import wmi
    c = wmi.WMI()
    serverName = c.Win32_OperatingSystem()[0].CSName
    print("ServerName: ", serverName, "\n")
except Exception as e:
    # Handle the exception when the operation fails
    print("Failed to get server name:", str(e))
    # Perform alternative actions or raise the exception again if needed

#---------------------------------------------------------------------------------------------------------------

# Variables and paths
global_path = r'E:\STR_SERVICES'
same_path = 'export\exported_configurations'
les_repertoires = []
save_path = r'./'

# Check if the global_path directory exists, otherwise handle the exception
if not os.path.isdir(global_path):
    print("The global path directory does not exist.")
    # Handle the case when the global path directory is missing
else:
    les_repertoires = os.listdir(global_path)

# Check if the same_path directory exists within global_path, otherwise handle the exception
same_path_full = os.path.join(global_path, same_path)
if not os.path.isdir(same_path_full):
    print("The same path directory does not exist.")
    # Handle the case when the same path directory is missing

# Continue with the code if directories exist
# Variables and paths
DirName = serverName
srcDir = r'\\192.168.29.1\Global_Share\STR'
sourcePath = srcDir
dstDir = os.path.join(srcDir, DirName)

if not os.path.isdir(srcDir):
    print("The source directory does not exist.")
    # Handle the case when the source directory is missing

if not os.path.isdir(dstDir):
    print("The destination directory does not exist.")
    # Handle the case when the destination directory is missing


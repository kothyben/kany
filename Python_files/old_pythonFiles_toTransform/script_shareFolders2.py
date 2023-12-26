"""
    Ce script permet de partager un dossier avec tous les privilèges 
    Le dossier est accessible à tout le monde en RWX
    il utilise les modules win32

"""

import win32netcon
import win32net
import win32wnet
import os

def share_folder_with_everyone(folder_path, share_name):
    share_info = {
        'netname': share_name,
        'path': folder_path,
        'remark': 'Shared Folder',
        'max_uses': -1,
        'passwd': '',
        'permissions': (
            win32netcon.PERMISSION_ALL,
            win32netcon.PERMISSION_ALL,
        ),
    }

    try:
        win32net.NetShareAdd(None, 2, share_info)
        print(f"Folder '{folder_path}' shared as '{share_name}' with full access to Everyone.")
    except win32net.error as e:
        print(f"Error sharing folder: {e}")

if __name__ == "__main__":
    # Specify the folder path and the share name
    folder_to_share = r"C:\Chemin\vers\le\dossier"
    share_name = "NomDuPartage"

    share_folder_with_everyone(folder_to_share, share_name)


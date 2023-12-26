# Approche multiplatforme 
import  platform, os, time
from datetime import datetime

def creation_date(path_to_file):

    """
    Try to get the date that a file was created, falling back to when it was
    last modified if that isn't possible.
    """
    if platform.system() == 'Windows':
        return os.path.getmtime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        try:
            return stat.st_birthtime
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            return stat.st_mtime

# convertir timestamp
def conv_timestamp(path_to_file) :
    date = str(creation_date(path_to_file)).split('.')[0]
    date = datetime.fromtimestamp(int(date))
    print( date)
    return date


conv_timestamp('GetPrinterServerName.py')
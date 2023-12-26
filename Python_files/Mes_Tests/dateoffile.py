
import os, os.path, time, platform
from datetime import datetime

def get_creation_date(file):
    stat = os.stat(file)
    try:
        return stat.st_birthtime
    except AttributeError:
        # Nous sommes probablement sous Linux. 
        # Pas de moyen pour obtenir la date de création, que la dernière date de modification.
        return stat.st_mtime


# Using os.path
print(os.path.getatime('global.py'))  # the last access time of a file, reported by os.stat()
print(os.path.getmtime('global.py'))  #the last modification time of a file, reported by os.stat()
print(os.path.getctime('global.py'))   # the metadata change time of a file, reported by os.stat()

# Using os.stat()
def getmtime(filename):
    """Return the last modification time of a file, reported by os.stat()."""
    return os.stat(filename).st_mtime


def getatime(filename):
    """Return the last access time of a file, reported by os.stat()."""
    return os.stat(filename).st_atime


def getctime(filename):
    """Return the metadata change time of a file, reported by os.stat()."""
    return os.stat(filename).st_ctime


# Convertir Timestamp en datetime
creation_date = datetime.fromtimestamp(get_creation_date('global.py'))
print("Date de création: %s" % creation_date)

print('\n')
print("Dernière modification: %s" % time.ctime(os.path.getmtime("global.py")))

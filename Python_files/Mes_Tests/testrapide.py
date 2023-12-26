
import pandas as pd 
import os


Dux_List_Modify = pd.read_excel(r'C:\Users\akiko.ext\OneDrive - GENERIX\Documents\testdatemodif.xls')

## ------------------------------- Listing Dux to treat date modification
#Dux_List_Modify = duxFrame.loc[:, ["Groups_Printers", "Name_Dux_Files"]]


# Multiplatform approach for taking of modify date
import  platform
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

# Convert values of  columns into datetime_modification


print(Dux_List_Modify.head())
print('\n')
print(Dux_List_Modify.columns)
print((Dux_List_Modify.shape))


dates = []
for i in Dux_List_Modify['Date_Last_modificaton'] :
    date = conv_timestamp(i)
    dates.append(date)

Dux_List_Modify.rename(columns={"Date_Last_modificaton" : "Dux_Paths"}, inplace=True)
Dux_List_Modify["date_mod"] = dates
print(Dux_List_Modify)
#    ------------------------------------------
# ----------
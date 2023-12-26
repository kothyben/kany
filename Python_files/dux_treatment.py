"""
    Ce Script python permet de répérer tous les fichiers dux de chque service et identifier les dates des 
    dernières moditifications de ces fichiers

"""
#-------------------------------------------------- LIBRAIRIES AND  GLOBAL REMOTE VARIABLES----------------------------------
# librairies 
import os
import random
import pandas as pd

#Server name
def get_server_name():
    return os.environ['COMPUTERNAME']

server_name = get_server_name()
serverName = server_name

# Variables and paths
str_services_path = r'E:\STR_SERVICES'
same_path = 'export\exported_configurations'
les_repertoires = []
save_path = r'./'


DirName = serverName
srcDir = r'\\192.168.29.1\Global_Share\STR'
dstDir = os.path.join(srcDir, DirName)
sourcePath = srcDir
#---------------------------------------------------------------------------------------------------------------

#----------------------------------------   - RECUPERER  LES DOSSIERS EDITIQUES  ------------------------------------------------
# lister tous les sous répertoires du repertoire de base
def list_rep(dir) :
    rep=[]
    for x in os.listdir(dir) :
        rep.append(x)
    return rep
 
# Create  paths : Avoir le chemin complet des dossiers editiques
def createpath():
    paths = []
    les_repertoires = list_rep(str_services_path)
    for dir in les_repertoires :
        if dir.startswith("editique") :
            path = os.path.join(str_services_path, str(dir))
            if os.path.isdir(path) == False :
                None
            else : 
                paths.append(path)
        else :
            None
    # garder les chemins uniques er reconvertir l'ensemble en une liste
    paths = set(paths); paths = list(paths)
    return paths

print([print(i) for i in createpath()])
print('\n')

#---------------------------------    LES DUX DANS LES DOSSIERS EDITIQUES CORRESPONDANTS ------------------------------------------------------------

# Chemins des dossiers editiques
paths = createpath()

# Trouver les DUX
def trouve_dux() :
    Names = []
    services = []
    for i in  range(len(paths)):
        new_path = os.path.join(paths[i], "{}".format(same_path))
        if os.path.isdir(new_path) == False :
            pass
        else :
            for name in os.listdir(new_path) :
                printer = new_path
                services.append(printer)
                Names.append(name)
                
    dux = list(zip(services, Names))
   
    return dux

# Save data into frame 
duxFrame = pd.DataFrame(trouve_dux(), columns = ['Groups_Printers', 'Name_Dux_Files'])


# ---------------------------------------------- TREATMENT OF DATE MODIFICATION DUX ----------------------------------------------------------

Dux_List_Modify = duxFrame.loc[:, ["Groups_Printers", "Name_Dux_Files"]]

# Add column of date  modify file dux 
try :

    date_paths = list()

    for i,j in list(zip(Dux_List_Modify["Groups_Printers"], Dux_List_Modify["Name_Dux_Files"])) :
        pat= os.path.join(i,j)
        date_paths.append(pat)

    Dux_List_Modify["Date_modification"] = date_paths

    print(Dux_List_Modify.head())
except :
    pd.DataFrame({'Erreur' : "PathsFichiersDux"}).to_csv('{}{}_ErrorPathsFichiersDux.csv'.format(save_path, serverName))
    

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
try :

    dates = []
    for i in Dux_List_Modify["Date_modification"] :
         date = conv_timestamp(i)
         dates.append(date)

    Dux_List_Modify.rename(columns={"Date_modification" : "Dux_Paths"}, inplace=True)
    Dux_List_Modify["date_mod"] = dates   
    print(Dux_List_Modify.head())
except :
    pd.DataFrame({'Erreur' : "ConvertTimestamp"}).to_csv('{}{}_ErrorConvertTimestamp.csv'.format(save_path, serverName))
 

## ------------------------------------------------------------------------------------------------

#Transform columns 
valeurs =  []
for val in duxFrame["Groups_Printers"] :
    val = val.split('\\')
    valeurs.append(val[2][9:])
duxFrame["SERVICES"] = valeurs
duxFrame = duxFrame.loc[:, ["SERVICES", "Name_Dux_Files"]]

# Groupby SERVICES column and count drux
duxFrame = duxFrame.assign(Nbr_DuxFiles=1).groupby(["SERVICES"]).agg({
                                'Nbr_DuxFiles' : sum , 
                                "Name_Dux_Files" : lambda x : ','.join(set(x))
}).reset_index()



# Export dataframe to csv file
duxFrame.to_csv('{}{}_Dux_GroupServices.csv'.format(save_path, serverName))  

Dux_List_Modify.to_csv('{}{}_Dux_Modify.csv'.format(save_path, serverName))  

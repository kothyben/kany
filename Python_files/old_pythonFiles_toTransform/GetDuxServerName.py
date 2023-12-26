
#-------------------------------------------------- VARIABLES GLOBALES REMOTE ----------------------------------
from varsRemote import *
#---------------------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------

"""
- RECUP DUX   -- RECUP DUX 
"""
#----------------------------------------------------------------------------------------

# lister tous les sous répertoires du repertoire de base
def list_rep(dir) :
    rep=[]
    for x in os.listdir(dir) :
        rep.append(x)
    return rep
 
print('\n')
# Create  paths 
def createpath():
    paths = []
    les_repertoires = list_rep(global_path)
    for dir in les_repertoires :
        if dir.startswith("editique") :
            path = os.path.join(global_path, str(dir))
            if os.path.isdir(path) == False :
                None
            else : 
                paths.append(path)
        else :
            None
        
    paths = set(paths); paths = list(paths)
    return paths

print([print(i) for i in createpath()])
print('\n')


# Trouver les DUX
paths = createpath()

def trouve_dux() :
    Names = []
    printers = []
    for i in  range(len(paths)):
        new_path = os.path.join(paths[i], "{}".format(same_path))
        if os.path.isdir(new_path) == False :
            pass
        else :
            for name in os.listdir(new_path) :
                printer = new_path
                printers.append(printer)
                Names.append(name)
                
    dux = list(zip(printers, Names))
   
    return dux

# Save data into frame 
duxFrame = pd.DataFrame(trouve_dux(), columns = ['Groups_Printers', 'Name_Dux_Files'])

## ---------------------------------------------- Listing Dux to treat date modification

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
duxFrame["Entrepots"] = valeurs
duxFrame = duxFrame.loc[:, ["Entrepots", "Name_Dux_Files"]]

# Groupby entrepots column and count drux
duxFrame = duxFrame.assign(Nbr_DuxFiles=1).groupby(["Entrepots"]).agg({
                                'Nbr_DuxFiles' : sum , 
                                "Name_Dux_Files" : lambda x : ','.join(set(x))
}).reset_index()



# Export dataframe to csv file
duxFrame.to_csv('{}{}_Dux_GroupPrinters.csv'.format(save_path, serverName))  

Dux_List_Modify.to_csv('{}{}_Dux_Modify.csv'.format(save_path, serverName))  
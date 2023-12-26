#from varsRemote import *
#-------------------------------------------------- VARIABLES GLOBALES REMOTE ----------------------------------
    # librairies 
import os 
import random
import pandas as pd
import win32print, pywintypes, win32con, win32api
import wmi 
import shutil, os, glob

# Get Server Name 
c = wmi.WMI()
serverName = c.Win32_OperatingSystem()[0].CSName
print("ServerName : ....", serverName, "\n")

# Variables and paths 
global_path = r'E:\STR_SERVICES'
same_path = 'export\exported_configurations'
les_repertoires = os.listdir(global_path)
save_path = r'./'

# paths and directories
DirName = serverName
sourcePath = r'\\192.168.29.1\Global_Share\STR'
srcDir = r'\\192.168.29.1\Global_Share\STR'
dstDir = r'\\192.168.29.1\Global_Share\STR\{}'.format(DirName)
#---------------------------------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------
""" 
SAVE PRINTERS IN DATAFRAME    SAVE PRINTERS IN DATAFRAME  
"""
#------------------------------------------------------------------------------------

def cut_generic_drivers() :

  # Sauvegarder les imprimantes dont les drivers sont Generic /*
  df = pd.read_csv("{}{}_allprinters.csv".format(save_path, serverName))

  D = []; P = []; C = []
  for p,d, c in zip(df.Name_Printers, df.DriversNames, df.DriversDirectory) :
      if d.startswith("Generic") :
          D.append(d)
          P.append(p)
          C.append(c)
      else :
        None
  data_generix = pd.DataFrame(list(zip(P, D, C)), 
                      columns=["Name_Printers", "DriversNames", "DriversDirectory"])

  return data_generix


# Spliter les colonnes pour ressortir les imprimantes et les entrepots
df = pd.read_csv("{}{}_allprinters.csv".format(save_path, serverName))

# Enlever ses imprimantes du fichier initial 
df = df.loc[df["DriversNames"] != "Generic / Text Only", 
                        ["Name_Printers","DriversNames", 'DriversDirectory']]

Entrepot = []
printera = []
for col in df["Name_Printers"] :
    if col.split('-') :
        col = col.strip()
        col = col.split('-')
        Entrepot.append(col[0])
        #printera.append(col[1])
    else:
        col = col.strip()
        col = "grpcreate-".join(col)
        col = col.split('-')
        Entrepot.append(col[0])
        #printera.append(col[1])


df["Entrepots"]= Entrepot
#df["Only_printers_Names"] = printera
df = df.loc[:, ["Entrepots", "Name_Printers","DriversNames",
                                    'DriversDirectory']]

print("\nFichier imprimantes et entrepots\n".upper(), df)
print("\nImprimantes avec drivers generic\n".upper(),cut_generic_drivers())    
print(df)
print(df.columns)



# Export data to csv 
try :
  df.to_csv("{}{}_printersInfos.csv".format(save_path, serverName))
except :
  pd.DataFrame([i for i in range(4)]).to_csv("{}pbprintersinfos.csv".format(save_path))


try :
  cut_generic_drivers().to_csv( "{}{}_Generic2_drivers.csv".format(save_path, serverName))
except:
  pd.DataFrame({"A": ['a','b'],"B" : [1,2]}).to_csv("{}PbAvecGenericDrivers.csv".format(save_path))

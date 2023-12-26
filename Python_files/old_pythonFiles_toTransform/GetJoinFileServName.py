# -----------------------------  VARIABLES GLOBALES  -----------------------------------------------
from varsRemote import *
#-------------------------------------------------- VARIABLES GLOBALES REMOTE ----------------------------------

#---------------------------------------------------------------------------------------------------------------

"""
- JOIN DATA  INFOS    -- JOIN DATA INFOS  
"""
#----------------------------------------------------------------------------------------
#Dux files
dux = pd.read_csv('{}{}_Dux_GroupPrinters.csv'.format(save_path, serverName))

#Printers and drivers files
printer_drivers = pd.read_csv("{}{}_printersInfos.csv".format(save_path, serverName))

# For Local test
#printer_drivers = pd.read_csv(r"C:\Users\akiko.ext\OneDrive - GENERIX\Documents\STR-FM-VAL3_printersInfos.csv")
#dux = pd.read_csv(r'C:\Users\akiko.ext\OneDrive - GENERIX\Documents\STR-FM-VAL3_Dux_GroupPrinters.csv')

# inner join  merge files
df_inner = pd.merge(dux, printer_drivers, on='Entrepots').drop_duplicates()
# Delete not using columns
df_inner.drop(['Unnamed: 0_x', 'Unnamed: 0_y'], axis=1, inplace=True)

# full outer join
df_outer = pd.merge(dux, printer_drivers, on='Entrepots', how='outer', indicator=True).drop_duplicates()
# Delete not using columns
df_outer.drop(['Unnamed: 0_x', 'Unnamed: 0_y'], axis=1, inplace=True)


print("\nNombre de lignes Inner----------- {}\nNombre de colonnes Inner------------{}".
                format(df_inner.shape[0], df_inner.shape[1]) )


print("\nNombre de lignes outer----------- {}\nNombre de colonnes outer------------{}".
                format(df_outer.shape[0], df_outer.shape[1]) )

print(df_outer.columns)

# Export data to csv into current directory where  file.exe is 
df_inner.to_csv('{}{}_GloballnnerInfos.csv'.format(save_path, serverName))
df_outer.to_csv('{}{}_GlobalOuterInfos.csv'.format(save_path, serverName))


# Group informations do not use -------------------- !!!!!!!! DO NOT USE !!!!!!----------------
# Group informations do not use -------------------- !!!!!!!! DO NOT USE !!!!!!----------------
def groupall() :
  try :

      GroupInner = df_inner.groupby(['Entrepots']).agg({
        
          'Name_Printers':lambda x : ','.join(set(x)),
          'Name_Dux_Files':lambda x : ','.join(set(x)),
          'DriversNames':lambda x : ','.join(set(x)),
          'DriversDirectory':lambda x : ','.join(set(x))
          }).reset_index().drop_duplicates()

  except:
      None

  try :
      GroupOuter = df_outer.groupby(['Entrepots']).agg({
        
          'Name_Printers':lambda x : ','.join(set(x)),
          'Name_Dux_Files':lambda x : ','.join(set(x)),
          'DriversNames':lambda x : ','.join(set(x)),
          'DriversDirectory':lambda x : ','.join(set(x))
          }).reset_index().drop_duplicates()
  except :
      None

  try :
    GroupInner.to_csv('{}GroupInner.csv'.format(save_path))
  except:
    None 

  try :
    GroupOuter.to_csv('{}GroupOuter.csv'.format(save_path))
  except:
    None 
  
  return None

# Group informations do not use -------------------- !!!!!!!! DO NOT USE !!!!!!----------------
# Group informations do not use -------------------- !!!!!!!! DO NOT USE !!!!!!----------------







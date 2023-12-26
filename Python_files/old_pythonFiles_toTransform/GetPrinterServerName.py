#-------------------------------------------------- VARIABLES GLOBALES REMOTE ----------------------------------

from varsRemote import  *

#---------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------

"""
 RECUP PRINTERS INFOS RECUP PRINTERS INFO

"""
# -----------------------------------------------------------------------------


# show all printers on machine
printers = win32print.EnumPrinters(2)

Imprintes = []
Drivers = []
Dir_drivers = []
Portnames = []

for i in printers:
    print("Nom_imprimante : ", i[2])
    Imprintes.append(i[2])

    #Drivers name
    p = win32print.OpenPrinter(i[2])
    object = win32print.GetPrinter(p, 2)
    driver = object['pDriverName']
    Drivers.append(driver)


    #Drivers directories
    p = win32print.OpenPrinter(i[2])
    drdir = win32print.GetPrinterDriverDirectory()
    Dir_drivers.append(drdir)


# save data into dataframe
data = list(zip(Imprintes, Drivers, Dir_drivers))
df = pd.DataFrame(data, columns = ["Name_Printers", "DriversNames", "DriversDirectory"])
print('\n', df)

df.to_csv("{}{}_allprinters.csv".format(save_path, serverName))

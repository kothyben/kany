import os
import random
import pandas as pd
import win32print 
import wmi

# Get Server Name
try:
    c = wmi.WMI()
    serverName = c.Win32_OperatingSystem()[0].CSName
    print("ServerName: ", serverName, "\n")
except Exception as e:
    # Handle the exception when the operation fails
    print("Failed to get server name:", str(e))
    # Perform alternative actions or raise the exception again if needed

# -------------- RECUP PRINTERS INFOS RECUP PRINTERS INFO

# show all printers on machine
printers = win32print.EnumPrinters(2)

Imprintes = []
Drivers = []
Dir_drivers = []
Paths_drivers = []
Portnames = []

for i in printers:
    print("Nom_imprimante : ", i[2])
    Imprintes.append(i[2])

    #Drivers name
    p = win32print.OpenPrinter(i[2])
    object = win32print.GetPrinter(p, 2)
    driver = object['pDriverName']
    Drivers.append(driver)


    #Drivers Path
    try:
        dvp = c.Win32_PrinterDriver()
        Paths_drivers.append(dvp[0].DriverPath)
        print("driverPath : ......", dvp[0].DriverPath)
    except:
        #Drivers directories
        p = win32print.OpenPrinter(i[2])
        drdir = win32print.GetPrinterDriverDirectory()
        Paths_drivers.append(drdir)


if __name__ == "__main__":
    # Créer le DataFrame à partir des listes Imprintes, Drivers et Dir_drivers
    df_printers_info = pd.DataFrame({
        "Nom_imprimante": Imprintes,
        "Driver Name": Drivers,
        "Driver Path": Paths_drivers
    })

    # Exporter le DataFrame dans un fichier CSV
    df_printers_info.to_csv("printers_info.csv", index=False)

    # Afficher le DataFrame
    print("\nInformations sur les imprimantes:")
    print(df_printers_info)

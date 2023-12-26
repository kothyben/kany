"""
    Ce script recapitules les informations sur  la machine oèu il est lancé dans un fichier csv
    informations_globales.csv

        - les applicationsinstallés sur les machine 
        - Les imprimantes 
        - les drivers installés
        - les ports utilisés (et les services les utilisant) et non utilisés 
        - Les informations de base d'une machine : nom_machine, ram, cpu, disque_dur  
"""

import os
import psutil
import pandas as pd
import winreg
import platform
import wmi


#----------  INSTALLED SOFWARE INTO THE MACHINE 
# *************************************************************************************************

def get_installed_software():
    software_list = []
    try:
        # Access the registry key containing information about installed software
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                            r"Software\Microsoft\Windows\CurrentVersion\Uninstall") as key:

            # Iterate through the subkeys to get the names of installed software
            for i in range(winreg.QueryInfoKey(key)[0]):
                subkey_name = winreg.EnumKey(key, i)
                with winreg.OpenKey(key, subkey_name) as subkey:
                    try:
                        software_name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                        software_list.append(software_name)
                    except Exception:
                        pass

    except Exception as e:
        print("Error while retrieving information about installed software:", e)

    return software_list


#  --------------  FUNCTION TO RETRIEVE APP PRINTS INSTALLED 
#****************************************************************************************************

def get_installed_print_applications():
    c = wmi.WMI()
    print_apps = c.Win32_PrinterConfiguration()
    installed_print_apps = [app.Name for app in print_apps]
    return installed_print_apps


# ------- FUNCTION TO  RETRIEVE DRIVERS INSTALLED 
# *************************************************************************************************

def get_installed_drivers():
    c = wmi.WMI()
    drivers = c.Win32_SystemDriver()
    installed_drivers = {driver.Name: driver.PathName for driver in drivers}
    return installed_drivers


#------ INFORMATIONS ABOUT PORTS AND SERVICES USING THEM ******************************
# *************************************************************************************************

def get_all_open_ports():
    open_ports = set()
    try:
        # Obtient toutes les connexions réseau
        connections = psutil.net_connections(kind='inet')

        # Parcourt chaque connexion et récupère les ports ouverts
        for conn in connections:
            if conn.status == psutil.CONN_LISTEN:
                open_ports.add(conn.laddr.port)

    except Exception as e:
        print("Erreur lors de la récupération des ports ouverts :", e)

    return open_ports

# version 1 : ---------------Fonction pour récupérer les services et les ports qu'elles utilisent
def get_services_using_ports():
    services_using_ports = {}
    try:
        # Exécute la commande netstat avec l'option -anb pour obtenir les informations sur les services ou applications utilisant les ports ouverts
        output = os.popen("netstat -anb").read()

        # Analyse la sortie pour obtenir les informations sur les services ou applications associées aux ports ouverts
        lines = output.splitlines()
        for i, line in enumerate(lines):
            if "LISTENING" in line:
                port = lines[i].split()[-1].split(":")[-1]
                service_info = lines[i + 1].strip()
                services_using_ports[port] = service_info

    except Exception as e:
        print("Erreur lors de l'exécution de la commande netstat :", e)

    return services_using_ports

# version 2 : ------------------Fonction pour récupérer les services et les ports qu'elles utilisent
def get_applications_and_ports():
    connections = psutil.net_connections()
    app_ports = {}
    for conn in connections:
        if conn.status == psutil.CONN_LISTEN:
            pid = conn.pid
            try:
                p = psutil.Process(pid)
                app_name = p.name()
                local_address = conn.laddr.ip
                local_port = conn.laddr.port
                if app_name in app_ports:
                    app_ports[app_name].append((local_address, local_port))
                else:
                    app_ports[app_name] = [(local_address, local_port)]
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
    return app_ports


#---------- BASIC AND COMMON INFOORMATION ABOUT MACHINE
# *************************************************************************************************

def get_ram_info():
    ram = psutil.virtual_memory()
    total_ram = round(ram.total / (1024 ** 3), 2)  # Conversion en Go
    used_ram = round(ram.used / (1024 ** 3), 2)    # Conversion en Go
    return total_ram, used_ram

def get_cpu_info():
    cpu_usage = psutil.cpu_percent(interval=1)    # Interval spécifié pour une mesure en temps réel
    return f"{cpu_usage}%"

def get_disk_info():
    partitions = psutil.disk_partitions()
    disk_partitions = []
    total_disks = []
    used_disks = []
    percentages = []

    for partition in partitions:
        if platform.system() == "Windows" and "fixed" in partition.opts:
            disk_usage = psutil.disk_usage(partition.mountpoint)
            total_disk = round(disk_usage.total / (1024 ** 3), 2)  # Conversion en Go
            used_disk = round(disk_usage.used / (1024 ** 3), 2)    # Conversion en Go
            pourcentage = round(disk_usage.percent, 2)             # Pourcentage d'utilisation du disque
            
            disk_partitions.append(partition.device)
            total_disks.append(total_disk)
            used_disks.append(used_disk)
            percentages.append(pourcentage)

    return disk_partitions, total_disks, used_disks, percentages


def get_installed_printers_count():
    c = wmi.WMI()
    print_apps = c.Win32_PrinterConfiguration()
    num_installed_print_apps = len(print_apps)
    return num_installed_print_apps

def get_basic_machine_info():

    # Informations sur la machine
    machine_name = platform.node()

    # Informations sur le système d'exploitation
    os_name = platform.system()
    os_version = platform.release()

    # Informations sur le processeur
    num_processors = psutil.cpu_count(logical=False)
    total_cpu = psutil.cpu_count()

    # Informations sur la mémoire RAM
    total_ram, used_ram = get_ram_info()

    # Utilisation du CPU
    cpu_usage = get_cpu_info()

    # Nombre d'imprimantes ou d'applications d'impression
    num_installed_print_apps = get_installed_printers_count()

    # Informations sur le disque dur
    partitions, total_disks, used_disks, percentages = get_disk_info()

    # Create an empty list to hold the single partition info lists
    machine_info = []

    for i in range(len(partitions)):
        # Create a list of tuples for each information
        single_partition = [
            ("Nom de la machine", machine_name, ""),
            ("Système d'exploitation", os_name, ""),
            ("Version du système", os_version, ""),
            ("Nombre de processeurs", num_processors, ""),
            ("CPU total de la machine", total_cpu, ""),
            ("Utilisation CPU", cpu_usage, "%"),
            ("Mémoire RAM totale", total_ram, "Go"),
            ("Mémoire RAM utilisée", used_ram, "Go"),
            ("Partition:", partitions[i]),
            ("Capacité totale du disque dur", total_disks[i], "Go"),
            ("Espace disque utilisé", used_disks[i], "Go"),
            ("Pourcentage d'utilisation du disque", percentages[i], "%"),
            ("Number_installed_Apps_printers", num_installed_print_apps)
        ]
        machine_info.append(single_partition)

    # Create the DataFrame using the collected information
    columns = ["Caractéristique", "Valeur", "Unité"]
    dfs = []

    for single_partition in machine_info:
        df_partition = pd.DataFrame(single_partition, columns=columns)
        dfs.append(df_partition)

    df_machine_info = pd.concat(dfs, ignore_index=True)


    return df_machine_info



#------------------------------ ---- GET ALL DATAFRAME AND EXPORT   ********************************************

# *********     Exécutez les fonctions de chaque script pour obtenir les DataFrames associés     *************
app_ports = get_applications_and_ports()
all_open_ports = get_all_open_ports()
services_using_ports = get_services_using_ports()

installed_software = get_installed_software()
drivers_installed = get_installed_drivers()
machine_info = get_basic_machine_info()
installed_print_apps = get_installed_print_applications()


# Créer une liste pour stocker les informations sur les ports ouverts et non utilisés
ports_info = []
for port in all_open_ports:
    if port in services_using_ports:
        service_info = services_using_ports[port]
    else:
        service_info = "Aucun service ou application utilisant ce port."
    ports_info.append({"Port": port, "Service Info": service_info})

# Créer les DataFrames pour chaque partie d'informations
df_ports_info = pd.DataFrame(ports_info)
df_app_ports = pd.DataFrame([(app, ports) for app, ports in app_ports.items()], columns=["Services_using_ports", "Ports_Used"])
df_installed_software = pd.DataFrame(installed_software, columns=["Installed Software"])
df_machine_info = machine_info
df_installed_drivers = pd.DataFrame(list(drivers_installed.items()), columns=["Driver", "File Path"])
df_installed_print_apps = pd.DataFrame(installed_print_apps, columns=["Installed Print Application"])


# Combinez les DataFrames en un seul DataFrame global en utilisant concat avec ignore_index=True
df_global = pd.concat([df_installed_software, df_installed_print_apps, df_installed_drivers,
                       df_app_ports, df_ports_info, df_machine_info], ignore_index=True)

# Afficher le DataFrame final
print("DataFrame global avec toutes les informations :")
print(df_global)

# Exporter le DataFrame global dans un fichier CSV
df_global.to_csv("informations_globales.csv", index=False)


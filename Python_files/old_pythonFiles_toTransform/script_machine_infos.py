import platform
import psutil
import pandas as pd
import win32print
import wmi

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
    for partition in partitions:
        if platform.system() == "Windows":
            if "Fixed" in partition.opts:
                disk_usage = psutil.disk_usage(partition.mountpoint)
                total_disk = round(disk_usage.total / (1024 ** 3), 2)  # Conversion en Go
                used_disk = round(disk_usage.used / (1024 ** 3), 2)    # Conversion en Go
                return total_disk, used_disk

    return None, None

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

    # Informations sur le disque dur
    total_disk, used_disk = get_disk_info()

    # Nombre d'imprimantes ou d'applications d'impression
    num_installed_print_apps = get_installed_printers_count()

    # Création d'une liste de tuples pour chaque information
    machine_info = [
        ("Nom de la machine", machine_name, ""),
        ("Système d'exploitation", os_name, ""),
        ("Version du système", os_version, ""),
        ("Nombre de processeurs", num_processors, ""),
        ("CPU total de la machine", total_cpu, ""),
        ("Utilisation CPU", cpu_usage, "%"),
        ("Mémoire RAM totale", total_ram, "Go"),
        ("Mémoire RAM utilisée", used_ram, "Go"),
        ("Capacité totale du disque dur", total_disk, "Go"),
        ("Espace disque utilisé", used_disk, "Go"),
        ("Pourcentage d'utilisation du disque", f"{psutil.disk_usage('/').percent}%", ""),
        ("Number_installed_Apps_printers", num_installed_print_apps)
    ]

    # Créer le DataFrame à partir de la liste
    df_machine_info = pd.DataFrame(machine_info, columns=["Caractéristique", "Valeur", "Unité"])

    return df_machine_info

if __name__ == "__main__":
    machine_info = get_basic_machine_info()

    # Afficher le DataFrame
    print("Caractéristiques de la machine :")
    print(machine_info)

    # Exporter le DataFrame dans un fichier CSV
    machine_info.to_csv("machine_info.csv", index=False)

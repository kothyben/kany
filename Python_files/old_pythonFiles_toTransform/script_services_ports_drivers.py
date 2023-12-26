import psutil
import wmi
import pandas as pd

# Fonction pour récupérer les applications et les ports qu'elles utilisent
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

# Fonction pour récupérer la liste des drivers installés
def get_installed_drivers():
    c = wmi.WMI()
    drivers = c.Win32_SystemDriver()
    installed_drivers = {driver.Name: driver.PathName for driver in drivers}
    return installed_drivers

# Fonction pour récupérer la liste des applications d'impression installées
def get_installed_print_applications():
    c = wmi.WMI()
    print_apps = c.Win32_PrinterConfiguration()
    installed_print_apps = [app.Name for app in print_apps]
    return installed_print_apps

if __name__ == "__main__":
    app_ports = get_applications_and_ports()
    installed_drivers = get_installed_drivers()
    installed_print_apps = get_installed_print_applications()

    # Convertir les dictionnaires en DataFrames
    df_app_ports = pd.DataFrame([(app, ports) for app, ports in app_ports.items()], columns=["App_Services", "Ports Used"])
    df_installed_drivers = pd.DataFrame(list(installed_drivers.items()), columns=["Driver", "File Path"])
    df_installed_print_apps = pd.DataFrame(installed_print_apps, columns=["Installed Print Application"])

    # Fusionner les DataFrames dans le sens des lignes avec des lignes vides entre eux
    merged_df = pd.concat([df_app_ports, df_installed_drivers, df_installed_print_apps], ignore_index=True)

    # Afficher le DataFrame
    print("Informations fusionnées:")
    print(merged_df)

    # Exporter le DataFrame dans un seul fichier CSV
    merged_df.to_csv("services_ports_drivers.csv", index=False)

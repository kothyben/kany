import os
import psutil
import pandas as pd

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

if __name__ == "__main__":
    all_open_ports = get_all_open_ports()
    services_using_ports = get_services_using_ports()

    # Créer une liste pour stocker les informations sur les ports ouverts et non utilisés
    ports_info = []
    for port in all_open_ports:
        if port in services_using_ports:
            service_info = services_using_ports[port]
        else:
            service_info = "Aucun service ou application utilisant ce port."
        ports_info.append({"Port": port, "Service Info": service_info})

    # Créer un DataFrame avec les informations sur les ports ouverts
    df_ports_info = pd.DataFrame(ports_info)

    # Exporter le DataFrame dans un fichier CSV
    df_ports_info.to_csv("ports_info.csv", index=False)

    # Afficher le DataFrame
    print("Informations sur les ports et les services associés (y compris les ports non utilisés) :")
    print(df_ports_info)

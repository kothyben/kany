import winreg
import pandas as pd

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

if __name__ == "__main__":
    installed_software = get_installed_software()
    logiciel_install = pd.DataFrame(installed_software, columns=["Installed Software"])
    print(logiciel_install)

    if not installed_software:
        print("No installed software detected.")
    else:
        # Export DataFrame to a CSV file named "installed_software.csv"
        csv_filename = "installed_software.csv"
        logiciel_install.to_csv(csv_filename, index=False)
        print(f"DataFrame exported to '{csv_filename}' successfully.")

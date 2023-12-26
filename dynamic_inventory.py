#!/usr/bin python3
import json
import subprocess

def get_dynamic_inventory():
    # Run the PowerShell script remotely on the Windows machine and get the output
    powershell_command = ['powershell.exe', '-ExecutionPolicy', 'RemoteSigned', './get_ip.ps1']
    process = subprocess.Popen(powershell_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = process.communicate()

    # Use the detected IP address for my_dynamic_host
    my_dynamic_host_ip = stdout.strip()

    # Generate the inventory dictionary
    inventory = {
        "my_group": {
            "hosts": {
                "my_dynamic_host": {
                    "ansible_host": my_dynamic_host_ip,
                }
            },
            "vars": {
                "ansible_user": "my_username",
                "ansible_password": "my_password",
                "ansible_become_pass": "my_sudo_password"
            }
        }
    }

    return inventory

if __name__ == "__main__":
    dynamic_inventory = get_dynamic_inventory()
    print(json.dumps(dynamic_inventory))


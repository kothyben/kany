import win32serviceutil
import win32con

# List of service names to include in the group
service_names = ["Service1", "Service2", "Service3"]

# Name for the service group
group_name = "MyServiceGroup"

# Create the service group
try:
    with win32serviceutil.Svcmgr as scm:
        service_handles = [scm.OpenService(service_name) for service_name in service_names]
        
        group_handle = scm.CreateGroup(group_name, group_name)
        for handle in service_handles:
            scm.AddToGroup(group_handle, win32serviceutil.GetServiceDisplayName(handle))

        print(f"Service group '{group_name}' created successfully.")
except Exception as e:
    print(f"Error: {e}")

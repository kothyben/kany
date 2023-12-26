"""
 Ce scripy permet de traiter le fichier txt afin
 de  récupere les variable groups et services s sous forme de dictionnaire

"""

import pandas as pd

# Replace 'file.txt' with your file path
file_path = 'Existed_groups_services.txt'

# Read the text file using pandas
data = pd.read_csv(file_path, delimiter=',')  # Change delimiter if necessary

# Convert DataFrame columns to a list for easier manipulation
columns_list = data.columns.tolist()

groups_names = []
group_data = []
for item in columns_list:
    item = item.strip().split('.')
    for elt in item:
        if elt.startswith('"HKEY'):
            last_name = elt.split('\\')[-1][:-1]
            if last_name == "u00cdSTICA":
                last_name = 'ANEXA LOGISTICA'
            group_name = last_name
            groups_names.append(group_name)
            group_data.append([])  # Create an empty list for each group

        # Check for StreamServe in the data and associate it with groups
        if 'REG_SZ' in elt:
            group_data[-1].append(elt.strip()[:-11])

# Now group_data contains lists of StreamServe data associated with each group
# make a dictionnary
dict_groups = {group: data for group, data in zip(groups_names, group_data)}

# Printing the dictionary items
for group, data in dict_groups.items():
    print(f"{group} : {data}")
    print('\n')

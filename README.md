# BASCULE STREAMSERVE

# Les prerecquis d'installation (IT et BE_INFRA) :

### Machine source Windows

---

    ==> Prérequis
            - Activation winrm
            - Login Administrator (sinon créer un user avec les droits  admin)
            - Pwd admin
            Ouverture des ports et communication avec machine destination (INFRA)

### Machine Destination Windows

---

    => Prérequis
    * Activation winrm
            * Créer un Login admin
            * Pwd admin
    Ouverture des ports
            et communication avec machine destination (INFRA)

### Autres prérecquis necessaires

---

    ACTIVER  WINRM  (HTTP ET HTTPS) SUR LES MACHINES ET OUVERTURE DES PORTS
        ouverture des ports : 443,4443, 80, 8080,5985,5986
        Machine source <===> la nouvelle machine Windows destination
        la nouvelle machine Windows <===> INF-DEP-TST- 192.168.139.66 (machine linux controler de test) )
        la nouvelle machine Windows <====> 192.168.99.23 (JENKINS )
        la machine Source <====> 192.168.99.23 (JENKINS )

    Dans la nouvelle machine installer le rôle Print Management
        Installer python sur la nouvelle machine  Python 3.11.4
        Installer dans les machines windouws s'il n'existe pas :
            l'outil PrintBrm.exe

    Créer la Partition E:/
        Copier le Dossier "outils" présent dans le E:\ de la machine STR-FM-VAL1 vers la nouvelle machine
        La nouvelle machine doit pouvoir accéder à tout dossier partagé crée et aussi si possible au dossier partagé GLOBALSHARE
        COPIER L'ISO STREAMSERVEV4 et installer       ===> StreamserV4.iso

    Autoriser tout le vlan « 10.231.5.X » sur les ports 9100 & 515 depuis le serveur StreamServe
    IP PROD : 192.168.141.12
    et/ou IP VALIDATION : 192.168.141.17 et/ou
    IP TEST  nouvelle machine Windows (ici 192.168.141.80 ---STR-APP-MUT-TST)

---

# DEMARCHE ET APPROCHE DETAILLEES DU PROJET

NB:  L'ouverture des ports  entre les nouvelles machines, la machine linux controller et les machines sources (celle dans lesquelles se trouve StreamServe)
Le test ici a été fait entre 2 machines windows machine source STR-MUT-TEST2 et la machine destination STR-APP-MUT-TST
et la machine linux controller est INF-DEP-TST

Des scripts python ont été convertis en fichiers executable .exe  afin de palier à la version de powershell diférente d'une machine source à l'autre.
Plusiers playbooks utilisent donc ses fichiers executables convertis en local afin de réaliser des tâches. L'utilisation de ses fichiers est mentionnée  dans le tableau récapitulatif ci-dessous. -S'il faille modifier les fichiers executables il faudrait modifier le fichier python correspondant et reconvertir ce dernier. Les fichiers sont unniquement destinées à des machines windows

Certains scripts .ps1 (robocopy) sont issus des templates j2 se trouvant dans le dossier  "./templates/"

## WORKFLOW DES TÂCHES

---

|                                                                                                                                            *Tâcjhes et Commentaires*                                                                                                                                            |                         *Fichier Python*                         |                                                               *exe / ps1 / bat*                                                               |                             *Playbooks*                             |                                                                                                                                                                               *extra vars - arguments *                                                                                                                                                                               |
| :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: | :----------------------------------------------------------------: | :---------------------------------------------------------------------------------------------------------------------------------------------: | :--------------------------------------------------------------------: | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: |
|                                                                                                                                     **Informations globales  machines**                                                                                                                                     | script_printers_driverPaths.py<br />script_printers_driverPaths.py |                                          script_infosGlobales.exe<br />script_printers_driverPaths.exe                                          | 0_global_infos_servers.yml<br />0_global_infos_destination_servers.yml |                                                                                  En output nous avons 2 fichiers :<br />informations_generales.csv + printers_infos.csv<br />Installed Software,Installed Print Application,<br />Driver,File Path,Services_using_ports,<br />Ports_Used,Port,Service                                                                                  |
|                                                                                                                     **Création et partage du  backup  dans<br />les machines Windows**                                                                                                                     |                                                                    |                                                                                                                                                |                **1_create_share_temp_folder.yml**                |                                                                                                                                                                                  dossier temp_folder                                                                                                                                                                                  |
|                                                                      **Copie et transfert des fichiers de  Editique<br /> (E:\STR_SERVICES\ )**<br /><br />Copie dans src TEMP --> <br />--> vers rep dédié ordinateur de destination                                                                      |                       copy_editique_moins.py                       |                                                             copy_editique_moins.exe                                                             |                **2_editique_copy_moinsLourd.yml**                | <br />La mention moins lourd  parce que un dossier <br />(RXIT) editique trop lourd n'est pas pris  en compte,<br />il est possible de copier ce dossier tout seul par la suite <br />en lancant ce répertoire en argument<br /><br />".\\config_files_pimp.exE {{ le_repertoire_lourd }}"<br />Notons que ceci a été fait à cause de <br />l'espace disque dans la machine source |
|                                                                                **Copie et transfert des dossiers drivers BAT  et FIC_PARAM**<br />NB : Les2 robocopy  copient à partir de temp_folder  de la machine source                                                                                |                        config_files_pimp.py                        |                                                              config_files_pimp.exe                                                              |   **3_1_robocopy_drivers.yml<br />3_2_robocopy_fic_param.yml**   |                                                                                                                                      ".\\config_files_pimp.exE {{ str_drivers_paths }}"<br />".\\config_files_pimp.exE {{ str_path_fic_param }}"                                                                                                                                      |
|                                              Création des différents services streamserve sur Windows directement<br />Ecriture sur registre Windows les services str<br /><br />repertoires = liste des noms des éditiques récupérer  depuis E:\\STR-SERVICES\\                                              |                                                                    |                                                 Str_Services_Registry.bat<br />win_Services.bat                                                 |                      **4_str_services.yml**                      |                                                                                                                                              .\\str_Services_Registry.bat      "{{ repertoires<br />.\\win_Services.bat   "{{ repertoires                                                                                                                                              |
|                                                    **Création des groupes de services  streamserve**<br /><br />Le script python permet de traiter le fichier txt afin  de  récupérer <br />les variable groups et services sous forme de dictionnaire                                                    |                          Filter_group.py                          |                                                     str_groups_and_services_associated.ps1                                                     |               **5_create_groups_and_services.yml**               |                                                                       script lancé :<br />powershell.exe -File .\str_groups_and_services_associated.ps1   -ansibleData  .\ansible_data.json<br /><br />-ansibleData est la variable récupérer from ansibles facts  .\ansible_data.json le fichier json crée                                                                       |
|                                               **Install remote  printers tcp/ip**<br />Ici on utilise l'outil PrintBrm.exe<br /><br />Le playbook met un certain temps Dans la création du fichier <br />ainsi que dans son transfert et son restor printers                                               |                                                                    |                                                                                                                                                |                  **6_migrate_tcp_printers,yml**                  |                                                                                                   Les imprimantes Outqueue_* sont aussi créées   pour installer ces dernières sur le streamserve port<br /> il faudrait donc les supprimer puis les recréer d'où le playbook 7_                                                                                                   |
| **Traitement des outqueue**<br />Il s'agit ici de mettre en place les outqueue sur le port de StreamServe directement<br /><br />**removeBoth_OutQueuePrintersAndPorts.ps1**<br />Permet de supprimer les Outqueue_* créées par l'outil printBrm sur des port standards au lieu du  Streamserve Port |                                                                    | removeBoth_OutQueuePrintersAndPorts.ps1<br />1_add_ports_only.ps1<br /><br /><br />    2_add_printers_only.ps1<br />Used_ports.ps1 (to check) |                **7_OutQueue_printers_create.yml**                |                                                        .\\1_add_ports_only.ps1<br />-printerPorts "{{ printerPorts join('", "') }}"<br /><br /><br />.\\2_add_printers_only.ps1<br />-printerPorts "{{ printerPorts join('", "') }}"<br /><br />Penser à faire tourner le spooler pour visualiser les changements effectifs                                                        |
|                                                                                                              **DUX CHECKING**<br />Vérifier la modification des DUX  relatifs aux imprimantes                                                                                                              |                          dux_treatment.py                          |                                                                                                                                                |                       **8_Dux_Check.yml**                       |                                                                                                                                                                                                                                                                                                                                                                                        |
|                                                                                                                                                                                                                                                                                                                    |                                                                    |                                                                                                                                                |                                                                        |                                                                                                                                                                                                                                                                                                                                                                                        |

## PROCEDURE DETAILLEE

---

### 1. Using ansible, établir la connexion entre ansible Controller et les Windows managed servers

    a. Configuration des machines Windows (winrm voir be_infra)
		b. l'inventaire (fichier hosts)
		==> playbooks/ping_nodes.yml

### 2. Afficher les informations de la machine source:  machines destinations si nécessaire :

    ===> playbooks/ 0_global_infos_servers.yml
        - Imprimantes connectes , drivers, cpu, ports_used

### 3. Créer Un dossier partagé dans les machines windows

    ==> playbooks/1_create_share_temp_folder.yml

### 4. Copie des dossiers importants et de configurations dans le temp_folder et les transférer

    dans les répertoires correspondants des machines    destinations
        - Copie et transfert des fichiers de  Editique  ==> playbooks/2_editique_copy_moinsLourd.yml
         - Copie et transfert des dossiers drivers BAT ===> playbooks/3_1_robocopy_drivers.yml
        - Copie et transfert des dossiers  FIC_PARAM   ===> playbooks/3_2_robocopy_fic_param.yml

### 5. Installation de streamserve dans la nouvelle machine  +  configuration des services + et les Outqueue + Printers remoteTCP

    -

#### 1. Installation STR

    a. Manuelle, à voir avec le service IT pour les GPO , installation avec l'iso  : Server + Tools + Communications Ports

#### 2. Configuration des services et groupes de services

    1. Création Automatique des services ===>  playbooks/4_str_services.yml, Qui comprend les fichiers :
                    ► batch_files/str_Services_Registry.bat
                    ► batch_files/win_Services.bat
            Relancer control center une fois sur le serveur pour observer les changements

    2. Grouper les services: ===>playbooks/5_create_groups_and_services.yml, utilisant les fichiers:
                    ►  str_groups_and_services_associated.ps1
                    ►  Python_files/Filter_group.py
            Relancer control center une fois sur le serveur pour observer les changements

#### 3. Gestion des outqueue (création des OutQueue sur streamserve port  et installation des imprimantes distantes tcp)

    1- Installation des imprimantes  distantes sur TCP Standard Port   ==> playbooks/6_migrate_tcp_printers.yml, utilisant:
                l'outil PrintBrm.exe se trouvant dans C:\WINDOWS\System32\spool\tools\PrintBrm.exe
                ==> l'installer si necessaire

    2- Installation des OutQueue sur le port StreamServe ==> playbooks/7_OutQueue_printers_create.yml
                    ► batch_files/1_add_ports_only.ps1.bat
                    ► batch_files/2_add_printers_only.bat
                    ► batch_files/removeBoth_OutQueuePrintersAndPorts.ps1
                    ► batch_files/Used_ports.ps1
                    ► tcp_printers_robocopy.ps1  venant du template /templates/tcp_printers.j2

### 6. Connexion avec wms et création des imprimantes sur wms

    Cf  équipe wms

### 7. Script de vérification de dernières modifications des fichiers DUX

    DUX CHECKING ===> playbooks/8_Dux_Check.yml
             ► Python_files/dux_treatment.py  ==> script qui donne des output  NomMachine_Dux_GroupServices.csv et  NomMachine_Dux_Modify.csv

---

# DEBUG OPTIMISATIONS ET AMELIORATIONS

---

    ==> L'ouverture des ports entre la machine controller et la machine Global-share\\inf-cifs-pr01.vmwr\Global_Share serait judicieux car faciliterait la copie des dossoers vers cette nouvelle machine: Ce qui n'est pas le cas sur ce test

    ===> Mieux gérer la sécurité du mot de passe machine source dans la créaton des fichier.ps1 issu des  templates j2

    ==> Convertir les fichiers .py en .exe directemen en ligne dans un playbook serait un gros plus ceci permettrait de ne penser qu'à la modification des fichiers python pour les anciennes machines et il n'y aurait plus une étape manuelle de convertion

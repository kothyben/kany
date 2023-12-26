pipeline {
    agent any
    environment {
        DISABLE_AUTH = 'true'
        DB_ENGINE    = 'sqlite'
        ANSIBLE_DEBUG = 'false'
        ANSIBLE_VERBOSITY = '2'
        
        
    
    }

    stages {
        stage('SCM connection') {
            steps {
                git credentialsId: 'jenkins-infra-user', url: 'https://192.168.73.6/akoki.ext/Streamserve_MigrationFolfers.git'
            }
        }
        
        stage('Check last git push ') {
            steps {

                sh '''
                 git log --pretty=format:"%h - %an, %ar : %s" --graph -p -2
                '''
                    }
        }
        
      
        stage('Ping windows Nodes') {
            steps {
               ansiblePlaybook (
                disableHostKeyChecking: true,
                playbook: 'playbooks/ping_nodes.yml',
                inventory: 'hosts' ,
                vaultCredentialsId: 'BE_STR_VAULT'
                )
            }
        }
        
        stage('SEE EXECUTABLE PATHS') {
            steps {
               sh '''
                echo $ANSIBLE_PLAYBOOK_EXECUTABLE 
                cp -r /usr/local/bin/*  /home/jenkins/.local/bin
               '''
            }
        }
        
        
        stage('Create directory work into windows nodes') {
            steps {
                ansiblePlaybook colorized: true, disableHostKeyChecking: true, installation: 'ansible', inventory: 'hosts',
                playbook: 'playbooks/create_dir.yml', vaultCredentialsId: 'BE_STR_VAULT',
                extras:  '-e dir_windows=${DIR_WINDOWS} '    
            }
        }
        
        
        stage('Copy .exe files from local to windows nodes') {
            steps {
                ansiblePlaybook (
                colorized: true,
                disableHostKeyChecking: true,
                playbook: 'playbooks/copy.yml',
                inventory: 'hosts' ,
                vaultCredentialsId: 'BE_STR_VAULT',
                
                extraVars: [
                    copy_files: "${COPY_FILES}",
                    dir_windows: "${DIR_WINDOWS}"
                    ]
                )
        }
        }
        
         stage(' PowerShell script  into windows nodes') {
            steps {
                ansiblePlaybook (
                colorized: true,
                disableHostKeyChecking: true,
                playbook: 'playbooks/powershellscript.yml',
                inventory: 'hosts' ,
                vaultCredentialsId: 'BE_STR_VAULT',
                
               extraVars: [
                    file_to_run: "${FILE_TO_RUN}",
                    copy_files: "${COPY_FILES}",
                    dir_windows: "${DIR_WINDOWS}"
                    ]         
                
                )
        }
        }
      
        
        stage('Runexe file into Windows Nodes') {
            steps {
                ansiblePlaybook (
                colorized: true, 
                disableHostKeyChecking: true, 
                installation: 'ansible', 
                inventory: 'hosts', 
                playbook: 'playbooks/runexe.yml', 
                vaultCredentialsId: 'BE_STR_VAULT', 
                 extraVars: [
                    file_to_run: "${FILE_TO_RUN}",
                    copy_files: "${COPY_FILES}",
                    dir_windows: "${DIR_WINDOWS}"
                    ] 
    
                )
            }
        }
   
    
        
        stage('OutPut of exe files Runned') {
            steps {
                ansiblePlaybook colorized: true, disableHostKeyChecking: true, installation: 'ansible', inventory: 'hosts',
                playbook: 'playbooks/output_exe.yml', vaultCredentialsId: 'BE_STR_VAULT',
                 extraVars: [
                    file_to_run: "${FILE_TO_RUN}",
                    copy_files: "${COPY_FILES}",
                    dir_windows: "${DIR_WINDOWS}"
                    ] 
            }
        }
        
        stage('Migrate FILES FROM WINDOWS TO LINUX') {
        steps {
            ansiblePlaybook (
                disableHostKeyChecking: true,
                colorized: true,
                become: true,
                playbook: 'playbooks/migrate_files.yml',
                inventory: 'hosts' ,
                vaultCredentialsId: 'BE_STR_VAULT',
                extraVars: [
                    file_to_run: "${FILE_TO_RUN}",
                    copy_files: "${COPY_FILES}",
                    dir_windows: "${DIR_WINDOWS}",
                    migrate_files: "${MIGRATE_FILES}"
                    ]
                )
            }
         }
         
         stage('See Dux Date Modificated') {
        steps {
            ansiblePlaybook (
                disableHostKeyChecking: true,
                colorized: true,
                become: true,
                playbook: 'playbooks/dux_modify.yml',
                inventory: 'hosts' ,
                vaultCredentialsId: 'BE_STR_VAULT',
                extraVars: [
                    file_to_run: "${FILE_TO_RUN}",
                    copy_files: "${COPY_FILES}",
                    dir_windows: "${DIR_WINDOWS}",
                    migrate_files: "${MIGRATE_FILES}"
                    ]
                )
            }
         }

    }
}

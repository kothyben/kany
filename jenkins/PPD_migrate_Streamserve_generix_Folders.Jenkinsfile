// Global variables

def main_role_url = "https://192.168.73.6/akoki.ext/Streamserve_MigrationFolfers.git"
def main_role_branch = 'master'

def inventory_git_url = "https://192.168.73.6/Ansible_Cloudops/Inventories/Production.git"
def inventory_branch = "master"
def inventories =  "preproduction"

def git_credentials = "jenkins-infra-user"
def vault_credentials = ['BE_STR_VAULT', 'vault_awx_pass', "ansible"]

def plays_path = "playbooks"
def playbook = "ping_nodes.yml"



pipeline {
    agent any
    
    environment {
    DISABLE_AUTH = 'true'
    DB_ENGINE    = 'sqlite'
    ANSIBLE_DEBUG = 'False'
    ANSIBLE_VERBOSITY = '1'
    
    }
    
    options {
        skipDefaultCheckout()
    }

   

    stages {
        
        stage('CLEAN DIRECTORY') {
            steps {
                deleteDir()
            }
        }

        stage('CLONE MAIN ROLE') {
            steps {
                checkout([$class: 'GitSCM',
                          branches: [[name: "${main_role_branch}"]],
                          doGenerateSubmoduleConfigurations: false,
                          extensions: [],
                          gitTool: 'Default',
                          submoduleCfg: [],
                          userRemoteConfigs: [[credentialsId:  "${git_credentials}", url: "${main_role_url}"]]
                        ])
            }
        }
        
        
        stage('CLONE INVENTORY') {
            steps {
                dir('inventoryDir') {
                    checkout([$class: 'GitSCM',
                        branches: [[name: "${inventory_branch}"]],
                        doGenerateSubmoduleConfigurations: false,
                        extensions: [],
                        gitTool: 'Default',
                        submoduleCfg: [],
                        userRemoteConfigs: [[credentialsId:  "${git_credentials}", url: "${inventory_git_url}"]]
                    ])
                                      
                }
            }
        }

    
        
        
       // stage('Ping windows machines') {
//     steps {
//         echo "inventaire: ${env.WORKSPACE}/inventoryDir/${inventories}"
//         echo "le playbook: ${env.WORKSPACE}/${plays_path}/${playbook}"
//         
//         // Even if it is failed next stage works
//         catchError(buildResult: 'unstable') {
//             ansiblePlaybook(
//                 inventory: "${env.WORKSPACE}/inventoryDir/${inventories}", 
//                 playbook: "${env.WORKSPACE}/${plays_path}/${playbook}", 
//                 credentialsId: "${git_credentials}", 
//                 disableHostKeyChecking: true, 
//                 vaultCredentialsId: "BE_STR_VAULT", 
//                 colorized: true
//             )
//         }
//     }
// }

        
        stage('PING WINDOWS NODES') {
            steps {
               ansiblePlaybook (
               colorized: true,
                disableHostKeyChecking: true,
                playbook: 'playbooks/ping_nodes.yml',
                inventory: 'hosts' ,
                vaultCredentialsId: 'BE_STR_VAULT'
                )
            }
        }
        
        stage('CONFIG CREDSSP INTO WINDOWS') {
              steps {
                ansiblePlaybook(
                  colorized: true,
                  disableHostKeyChecking: true,
                  installation: 'ansible',
                  inventory: 'hosts',
                  playbook: 'playbooks/config_credssp.yml',
                  vaultCredentialsId: 'BE_STR_VAULT'
                )
              }
            }
            
        stage('WORKSPACE PERMISSIONS') {
            steps {
                script {
                    def workspace = "${env.WORKSPACE}"
        
                    ansiblePlaybook(
                        colorized: true,
                        disableHostKeyChecking: true,
                        installation: 'ansible',
                        inventory: 'hosts',
                        playbook: 'playbooks/workspace_permissions.yml',
                        vaultCredentialsId: 'BE_STR_VAULT',
                        extras: "-e workspace=${workspace}"
                    )
                }
            }
        }
        

        
        stage('COPY FOLDERS FROM WIN TO LINUX') {
            steps {
                script {
                    def workspace = "${env.WORKSPACE}"
        
                    ansiblePlaybook(
                        colorized: true,
                        disableHostKeyChecking: true,
                        installation: 'ansible',
                        inventory: 'hosts',
                        playbook: 'playbooks/copy_windows_folders.yml',
                        vaultCredentialsId: 'BE_STR_VAULT',
                        extras: "-e workspace=${workspace}"
                    )
                }
            }
        }


        
            

    }

}

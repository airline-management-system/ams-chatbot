def projectName = 'ams'
def imageName = 'chatbot'
def registryName = 'harbor.turkey-diminished.ts.net'
def gitUrl = 'git@github.com:airline-management-system/ams-chatbot.git'
def gitCredentials = 'brkydnc-ssh'
def gitBranch = 'main'

pipeline {
    agent {
        kubernetes {
            yamlFile 'Agent.yaml'
        }
    }

    options {
        buildDiscarder logRotator(artifactDaysToKeepStr: '', artifactNumToKeepStr: '5', daysToKeepStr: '', numToKeepStr: '5')
    }

    stages {

        stage('Git'){
            steps{
                git branch: "${gitBranch}", credentialsId: "${gitCredentials}", url: "${gitUrl}"
            }
        }

        stage('Docker Build & Push'){
            environment {
                PATH = "/busybox:/kaniko:$PATH"
            }
            steps {
                container(name: 'kaniko', shell: '/busybox/sh') {
                    sh "/kaniko/executor --dockerfile `pwd`/Dockerfile --context `pwd` --destination=${registryName}/${projectName}/${imageName}:latest"
                }
            }
        }
    }
}

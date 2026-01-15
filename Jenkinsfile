pipeline {
    agent any

    environment {
        IMAGE_NAME = "smartfarm-api"
        IMAGE_TAG  = "${BUILD_NUMBER}"
    }

    stages {

        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Read App Version') {
            steps {
                script {
                    env.APP_BASE_VERSION = readFile('VERSION').trim()
                    env.APP_VERSION = "${env.APP_BASE_VERSION}.${env.BUILD_NUMBER}"
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                bat """
                echo Building Docker image %IMAGE_NAME%:%IMAGE_TAG%
                docker build --build-arg APP_VERSION=%APP_VERSION% -t %IMAGE_NAME%:%IMAGE_TAG% backend
                """
            }
        }

        stage('Save Image Tag') {
            steps {
                bat '''
                echo IMAGE_TAG=%IMAGE_TAG% > image.env
                '''
            }
        }
    }

    post {
        success {
            echo "CI build successful. Image tag: ${IMAGE_TAG}"
            archiveArtifacts artifacts: 'image.env', fingerprint: true
        }

        failure {
            echo 'CI build failed'
        }
    }
}

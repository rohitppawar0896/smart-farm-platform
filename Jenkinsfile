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

        stage('Build Docker Image') {
            steps {
                bat """
                echo Building Docker image %IMAGE_NAME%:%IMAGE_TAG%
                docker build -t %IMAGE_NAME%:%IMAGE_TAG% backend
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

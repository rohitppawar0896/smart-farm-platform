pipeline {
    agent any

    stages {

        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t smartfarm-api ./backend'
            }
        }
    }

    post {
        success {
            echo 'CI build successful'
        }
        failure {
            echo 'CI build failed'
        }
    }
}

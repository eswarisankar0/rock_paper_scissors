pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "ahileshroy/simple-app"
        DOCKER_CREDENTIALS_ID ="devops-dockerhub"
    }

    stages {

        stage('Clone') {
            steps {
                checkout scm
            }
        }

        stage('Build') {
            steps {
                echo "Installing dependencies..."
                sh '''
                if [ -f requirements.txt ]; then
                    pip install -r requirements.txt
                fi

                if [ -f package.json ]; then
                    npm install
                fi
                '''
            }
        }

        stage('Docker Build') {
            steps {
                script {
                    docker.build("${DOCKER_IMAGE}:${BUILD_NUMBER}")
                }
            }
        }

        stage('Push to DockerHub') {
            steps {
                script {
                    docker.withRegistry('', DOCKER_CREDENTIALS_ID) {
                        docker.image("${DOCKER_IMAGE}:${BUILD_NUMBER}").push()
                        docker.image("${DOCKER_IMAGE}:${BUILD_NUMBER}").push("latest")
                    }
                }
            }
        }

        stage('Deploy (Optional)') {
            when {
                branch 'main'
            }
            steps {
                echo "Deployment stage can be added here (EC2, etc)"
            }
        }
    }

    post {
        success {
            echo "Build Successful!"
        }
        failure {
            echo "Build Failed!"
        }
    }
}

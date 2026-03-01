pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "ahileshroy/stone-paper-scissors"
        DOCKER_CREDENTIALS_ID = "devops-dockerhub"
        CONTAINER_NAME = "rps-app"
        APP_PORT = "5000"
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
                    pip3 install -r requirements.txt
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

        stage('Deploy') {
            steps {
                script {
                    sh '''
                    echo "Pulling latest image..."
                    docker pull ${DOCKER_IMAGE}:latest

                    echo "Stopping old container if exists..."
                    docker stop ${CONTAINER_NAME} || true
                    docker rm ${CONTAINER_NAME} || true

                    echo "Running new container..."
                    docker run -d -p ${APP_PORT}:${APP_PORT} --name ${CONTAINER_NAME} ${DOCKER_IMAGE}:latest
                    '''
                }
            }
        }
    }

    post {
        success {
            echo "CI/CD Pipeline Executed Successfully!"
        }
        failure {
            echo "Pipeline Failed!"
        }
    }
}
pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'nidhi8901/web-based-password-manager'
        IMAGE_TAG = "${BUILD_NUMBER}"
    }

    stages {

        stage('Checkout') {
            steps {
                echo 'Checking out source code...'
                checkout scm
            }
        }

        stage('Build') {
            steps {
                echo 'Building Password Manager application...'
                sh 'python3 --version'
                sh 'ls -la'
                sh 'python3 -m py_compile app.py web_app.py'
            }
        }

        stage('Test') {
            steps {
                echo 'Installing Python dependencies...'
                sh 'python3 -m pip install --no-cache-dir -r requirements.txt'

                echo 'Running automated tests...'
                sh 'chmod +x test.sh'
                sh './test.sh'
            }
        }

        stage('Package') {
            steps {
                echo 'Building Docker image...'
                sh 'docker build -t ${DOCKER_IMAGE}:${IMAGE_TAG} .'
                sh 'docker tag ${DOCKER_IMAGE}:${IMAGE_TAG} ${DOCKER_IMAGE}:latest'
            }
        }

        stage('Docker Push') {
            steps {
                echo 'Pushing Docker image to Docker Hub...'

                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub_cred',
                        usernameVariable: 'DOCKER_USERNAME',
                        passwordVariable: 'DOCKER_PASSWORD'
                    )
                ]) {
                    sh '''
                        echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
                        docker push ${DOCKER_IMAGE}:${IMAGE_TAG}
                        docker push ${DOCKER_IMAGE}:latest
                        docker logout
                    '''
                }
            }
        }
    }

    post {
        success {
            echo '======================================'
            echo 'CI/CD pipeline completed successfully!'
            echo '======================================'
        }

        failure {
            echo 'Pipeline failed. Check the Jenkins console output.'
        }
    }
}

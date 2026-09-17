pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'nidhi8901/web-based-password-manager'
        IMAGE_TAG = "${BUILD_NUMBER}"
    }

    stages {

        stage('Checkout') {
            steps {
                echo '=== CHECKOUT ==='
                checkout scm
            }
        }

        stage('Build') {
            steps {
                echo '=== BUILD APPLICATION ==='

                sh '''
                    echo "Python syntax check..."
                    docker run --rm \
                        -v "$(pwd)":/app \
                        -w /app \
                        python:3.10-slim \
                        python -m py_compile app.py web_app.py

                    echo "Build preparation completed."
                '''
            }
        }

        stage('Test') {
            steps {
                echo '=== TEST APPLICATION ==='

                sh '''
                    docker build \
                        -t ${DOCKER_IMAGE}:${IMAGE_TAG} \
                        .

                    echo "Testing installed Python packages..."

                    docker run --rm \
                        ${DOCKER_IMAGE}:${IMAGE_TAG} \
                        python -c "import flask, passlib, cryptography, bcrypt; print('All required Python packages are installed')"

                    echo "Testing Python syntax..."

                    docker run --rm \
                        ${DOCKER_IMAGE}:${IMAGE_TAG} \
                        python -m py_compile app.py web_app.py

                    echo "======================================"
                    echo "ALL TESTS PASSED"
                    echo "======================================"
                '''
            }
        }

        stage('Package') {
            steps {
                echo '=== PACKAGE DOCKER IMAGE ==='

                sh '''
                    docker tag \
                        ${DOCKER_IMAGE}:${IMAGE_TAG} \
                        ${DOCKER_IMAGE}:latest

                    echo "Docker images created:"
                    docker images | grep web-based-password-manager
                '''
            }
        }

        stage('Docker Push') {
            steps {
                echo '=== PUSH TO DOCKER HUB ==='

                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub_cred',
                        usernameVariable: 'DOCKER_USERNAME',
                        passwordVariable: 'DOCKER_PASSWORD'
                    )
                ]) {
                    sh '''
                        echo "$DOCKER_PASSWORD" | docker login \
                            -u "$DOCKER_USERNAME" \
                            --password-stdin

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
            echo '''
========================================
CI/CD PIPELINE SUCCESSFUL
========================================
Checkout      : PASSED
Build         : PASSED
Test          : PASSED
Package       : PASSED
Docker Push   : PASSED
========================================
'''
        }

        failure {
            echo 'CI/CD PIPELINE FAILED'
        }
    }
}

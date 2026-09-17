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
                echo '=== BUILD ==='

                sh '''
                    docker run --rm \
                      -v "$PWD":/app \
                      -w /app \
                      python:3.10-slim \
                      python -m py_compile app.py web_app.py
                '''
            }
        }

        stage('Test') {
            steps {
                echo '=== TEST ==='

                sh '''
                    docker run --rm \
                      -v "$PWD":/app \
                      -w /app \
                      python:3.10-slim \
                      sh -c "
                        pip install --no-cache-dir -r requirements.txt &&
                        python -c 'import flask, passlib, cryptography, bcrypt' &&
                        python -m py_compile app.py web_app.py &&
                        test -f app.py &&
                        test -f web_app.py &&
                        test -f requirements.txt &&
                        test -f Dockerfile &&
                        echo '======================================' &&
                        echo 'ALL TESTS PASSED' &&
                        echo '======================================'
                      "
                '''
            }
        }

        stage('Package') {
            steps {
                echo '=== DOCKER BUILD ==='

                sh '''
                    docker build \
                      -t ${DOCKER_IMAGE}:${IMAGE_TAG} \
                      -t ${DOCKER_IMAGE}:latest \
                      .
                '''

                sh 'docker images | grep web-based-password-manager'
            }
        }

        stage('Docker Push') {
            steps {
                echo '=== DOCKER PUSH ==='

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
Docker Build  : PASSED
Docker Push   : PASSED
========================================
'''
        }

        failure {
            echo 'CI/CD PIPELINE FAILED - CHECK THE FAILED STAGE'
        }
    }
}

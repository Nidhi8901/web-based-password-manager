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
                    echo "Checking project files..."
                    test -f app.py
                    test -f web_app.py
                    test -f requirements.txt
                    test -f Dockerfile

                    echo "Building Docker image..."
                    docker build -t ${DOCKER_IMAGE}:${IMAGE_TAG} .
                '''
            }
        }

        stage('Test') {
            steps {
                echo '=== TEST ==='

                sh '''
                    echo "Testing Python packages inside application image..."

                    docker run --rm \
                        ${DOCKER_IMAGE}:${IMAGE_TAG} \
                        python -c "import flask, passlib, cryptography, bcrypt; print('Required packages: PASS')"

                    echo "Testing Python syntax..."

                    docker run --rm \
                        ${DOCKER_IMAGE}:${IMAGE_TAG} \
                        python -m py_compile app.py web_app.py

                    echo "Testing application files..."

                    docker run --rm \
                        ${DOCKER_IMAGE}:${IMAGE_TAG} \
                        sh -c "test -f /app/app.py && test -f /app/web_app.py && test -f /app/requirements.txt"

                    echo "======================================"
                    echo "ALL TESTS PASSED"
                    echo "======================================"
                '''
            }
        }

        stage('Package') {
            steps {
                echo '=== PACKAGE ==='

                sh '''
                    docker tag ${DOCKER_IMAGE}:${IMAGE_TAG} ${DOCKER_IMAGE}:latest

                    echo "Created images:"
                    docker images | grep web-based-password-manager
                '''
            }
        }

        stage('Docker Push') {
            steps {
                echo '=== DOCKER HUB PUSH ==='

                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub_cred',
                        usernameVariable: 'DOCKER_USERNAME',
                        passwordVariable: 'DOCKER_PASSWORD'
                    )
                ]) {
                    sh '''
                        echo "$DOCKER_PASSWORD" | docker login \
                            --username "$DOCKER_USERNAME" \
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
            echo '======================================'
            echo 'WEEK 9 CI/CD PIPELINE SUCCESSFUL'
            echo '======================================'
        }

        failure {
            echo '======================================'
            echo 'PIPELINE FAILED'
            echo '======================================'
        }
    }
}

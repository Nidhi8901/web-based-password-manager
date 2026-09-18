pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'nidhi8901/web-based-password-manager'
        IMAGE_TAG = "${BUILD_NUMBER}"
        KUBECONFIG = '/tmp/kubeconfig'
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
                    docker run --rm \
                        ${DOCKER_IMAGE}:${IMAGE_TAG} \
                        python -c "import flask, passlib, cryptography, bcrypt; print('Required packages: PASS')"

                    docker run --rm \
                        ${DOCKER_IMAGE}:${IMAGE_TAG} \
                        python -m py_compile app.py web_app.py

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

        stage('Deploy') {
            steps {
                echo '=== KUBERNETES DEPLOYMENT ==='

                sh '''
                    echo "Using Kubernetes context:"
                    kubectl config current-context

                    echo "Deploying application..."
                    kubectl apply -f k8s/deployment.yaml
                    kubectl apply -f k8s/service.yaml

                    echo "Updating image to:"
                    echo "${DOCKER_IMAGE}:${IMAGE_TAG}"

                    kubectl set image deployment/password-manager \
                        password-manager=${DOCKER_IMAGE}:${IMAGE_TAG}

                    kubectl rollout status deployment/password-manager \
                        --timeout=180s
                '''
            }
        }

        stage('Verify') {
            steps {
                echo '=== DEPLOYMENT VERIFICATION ==='

                sh '''
                    echo "=== Deployment ==="
                    kubectl get deployment password-manager

                    echo
                    echo "=== Pods ==="
                    kubectl get pods -l app=password-manager -o wide

                    echo
                    echo "=== Service ==="
                    kubectl get service password-manager-service

                    echo
                    echo "=== Rollout Status ==="
                    kubectl rollout status deployment/password-manager

                    echo
                    echo "=== Verification Successful ==="
                '''
            }
        }

        stage('Rollback Test') {
            steps {
                echo '=== ROLLBACK TEST ==='

                sh '''
                    echo "Creating a new rollout revision..."

                    kubectl set image deployment/password-manager \
                        password-manager=${DOCKER_IMAGE}:latest

                    kubectl rollout status deployment/password-manager \
                        --timeout=180s

                    echo
                    echo "Rolling back to previous revision..."

                    kubectl rollout undo deployment/password-manager

                    kubectl rollout status deployment/password-manager \
                        --timeout=180s

                    echo
                    echo "=== ROLLBACK SUCCESSFUL ==="

                    kubectl get pods -l app=password-manager

                    echo
                    echo "=== Rollout History ==="
                    kubectl rollout history deployment/password-manager
                '''
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

# 🔐 Web-Based Password Manager

A secure web-based password manager built with **Python Flask**, **Docker**, **Jenkins**, and **Kubernetes**.

This project was developed and extended as a DevOps project to demonstrate an end-to-end **CI/CD workflow**, including automated testing, Docker image creation, Docker Hub publishing, Kubernetes deployment, rolling updates, deployment verification, and rollback.

---

## 📌 Project Overview

The Web-Based Password Manager allows users to securely manage their passwords through a web application.

The application provides functionality for:

- User registration and login
- Password storage and management
- Password generation
- Password strength checking
- Password updates
- Password listing
- Password expiry handling
- Secure password hashing
- Encryption of stored password data

The application is containerized using Docker and deployed through an automated Jenkins CI/CD pipeline to a Kubernetes cluster.

---

## 🚀 DevOps Workflow

The complete CI/CD workflow used in this project is:

```text
Developer
    │
    ▼
GitHub Repository
    │
    │ GitHub Webhook
    ▼
Jenkins
    │
    ├── Checkout
    ├── Build
    ├── Test
    ├── Package
    ├── Docker Push
    ├── Deploy
    ├── Verify
    └── Rollback Test
    │
    ▼
Docker Hub
    │
    ▼
Kubernetes Cluster
    │
    ├── Rolling Deployment
    ├── Health Verification
    └── Rollback
    │
    ▼
Password Manager Application
🛠️ Technologies Used
Technology	Purpose
Python	Application development
Flask	Web application framework
Passlib	Password hashing
Cryptography / Fernet	Data encryption
Git	Version control
GitHub	Source code repository
Jenkins	CI/CD automation
Docker	Application containerization
Docker Hub	Container image registry
Kubernetes	Container orchestration
Kind	Local Kubernetes cluster
Bash	Automated testing and scripting
ngrok	GitHub webhook connectivity for local Jenkins
✨ Application Features
User registration
User authentication
Password management
Password generation
Password strength checking
Password expiry support
Password update functionality
Password listing
Encrypted password data
Hashed user passwords
Web-based interface
Dockerized application
Kubernetes deployment
Automated CI/CD pipeline
📁 Project Structure
web-based-password-manager/
│
├── app.py
├── web_app.py
├── key.py
├── requirements.txt
├── Dockerfile
├── Jenkinsfile
├── test.sh
├── .gitignore
├── .env.example
├── README.md
│
├── k8s/
│   ├── deployment.yaml
│   └── service.yaml
│
└── project screenshots.pdf
Important files
File	Description
app.py	Core password manager functionality
web_app.py	Flask web application
key.py	Key-related application utility
requirements.txt	Python dependencies
Dockerfile	Docker image configuration
Jenkinsfile	Jenkins CI/CD pipeline
test.sh	Automated project validation script
.env.example	Example environment configuration
.gitignore	Prevents secrets and local files from being committed
k8s/deployment.yaml	Kubernetes Deployment configuration
k8s/service.yaml	Kubernetes Service configuration
🔐 Security and Secrets

The application uses an environment variable for the encryption key.

The actual encryption key is not stored in the GitHub repository.

Example:

ENCRYPTION_KEY=your-fernet-encryption-key-here

The repository contains only:

.env.example

The actual .env file is excluded using .gitignore.

The project also ignores local database files, password data files, Python cache files, and Kubernetes secret configuration.

.gitignore includes
.env
.env.*
!.env.example

*.db
*.sqlite
*.sqlite3

passwords.json

__pycache__/
*.py[cod]

k8s/secret.yaml

For Kubernetes, the encryption key is supplied through a Kubernetes Secret rather than being hard-coded in the Deployment configuration.

💻 Run the Application Locally
1. Clone the repository
git clone <repository-url>
cd web-based-password-manager
2. Create a Python virtual environment
python3 -m venv venv

Activate it:

Linux / WSL / Git Bash
source venv/bin/activate
Windows
venv\Scripts\activate
3. Install dependencies
pip install -r requirements.txt
4. Configure the encryption key

Create a local .env file based on .env.example.

Set:

ENCRYPTION_KEY=your-local-encryption-key

The actual value should never be committed to GitHub.

5. Start the application
python web_app.py

The application runs on:

http://localhost:8000
🐳 Docker

The application is containerized using the following Docker workflow:

Dockerfile
     │
     ▼
Docker Build
     │
     ▼
Docker Image
     │
     ▼
Docker Container
     │
     ▼
Flask Application
Build the Docker image
docker build -t web-based-password-manager .
Run the container

The application requires the encryption key as an environment variable.

docker run -d \
  --name password-manager \
  -p 8000:8000 \
  -e ENCRYPTION_KEY="your-local-encryption-key" \
  web-based-password-manager

Check the container:

docker ps

Open:

http://localhost:8000
🧪 Automated Testing

The project contains an automated test script:

test.sh

The tests validate:

1. Python syntax
python3 -m py_compile app.py web_app.py
2. Required Python packages

The project checks:

flask
passlib
cryptography
bcrypt
3. Required project files

The pipeline verifies that the following files exist:

app.py
web_app.py
requirements.txt
Dockerfile

Run the tests locally with:

chmod +x test.sh
./test.sh

Expected result:

All tests passed successfully!
⚙️ Jenkins CI/CD Pipeline

Jenkins is used to automate the complete build and deployment process.

The pipeline is defined in:

Jenkinsfile

The pipeline contains the following stages:

Checkout
   ↓
Build
   ↓
Test
   ↓
Package
   ↓
Docker Push
   ↓
Deploy
   ↓
Verify
   ↓
Rollback Test
🔄 Jenkins Pipeline Stages
1. Checkout

Jenkins checks out the latest source code from GitHub.

checkout scm
2. Build

The pipeline:

Verifies required project files
Builds the Docker image
Tags the image using the Jenkins build number

Example:

nidhi8901/web-based-password-manager:<BUILD_NUMBER>
3. Test

Testing is performed inside the Docker image.

The pipeline checks:

Required Python packages
Python syntax
Required application files

Example validation:

Required packages: PASS

and:

ALL TESTS PASSED
4. Package

The generated image is also tagged as:

latest

Therefore each successful build produces:

nidhi8901/web-based-password-manager:<BUILD_NUMBER>
nidhi8901/web-based-password-manager:latest
5. Docker Push

Jenkins securely authenticates with Docker Hub using Jenkins credentials.

The pipeline pushes:

<BUILD_NUMBER>
latest

to the Docker Hub repository.

Docker credentials are stored in Jenkins using the credential ID:

dockerhub_cred

The Docker Hub password/token is not stored in the Jenkinsfile.

🌐 GitHub Webhook Integration

GitHub is integrated with Jenkins using a webhook.

The workflow is:

GitHub Push
     │
     ▼
GitHub Webhook
     │
     ▼
Jenkins
     │
     ▼
CI/CD Pipeline

For the local Jenkins environment, ngrok was used to provide a public endpoint for GitHub webhook delivery.

The Jenkins webhook endpoint used is:

/github-webhook/

A successful webhook delivery automatically triggers a Jenkins build.

Example Jenkins build message:

Started by GitHub push by Nidhi8901

Note: The ngrok URL is temporary and should not be stored in the repository README because it can change when the ngrok session is restarted.

☸️ Kubernetes Deployment

The application is deployed to a local Kubernetes cluster created using Kind.

The Kubernetes configuration is stored in:

k8s/
├── deployment.yaml
└── service.yaml
Kubernetes Deployment

The Deployment is configured with:

Replicas: 3

This provides three application pods.

The Deployment uses the Kubernetes:

RollingUpdate

strategy.

Configuration:

strategy:
  type: RollingUpdate
  rollingUpdate:
    maxUnavailable: 1
    maxSurge: 1

The application container exposes:

8000
🔑 Kubernetes Secret

The application encryption key is provided to the container through a Kubernetes Secret.

The Deployment references:

password-manager-secret

and the environment variable:

ENCRYPTION_KEY

The secret configuration is intentionally not committed to GitHub.

The secret can be created locally with:

kubectl create secret generic password-manager-secret \
  --from-literal=ENCRYPTION_KEY="your-local-encryption-key"

Do not place a real encryption key in this README or in a public repository.

🌍 Kubernetes Service

The application is exposed using a Kubernetes NodePort Service.

Service Name:
password-manager-service

Service configuration:

Type: NodePort
Port: 8000
Target Port: 8000
Node Port: 30080

Check the service:

kubectl get service password-manager-service
🚀 Deploy the Application Manually

Select the Kubernetes context:

kubectl config use-context kind-kind

Apply the Deployment:

kubectl apply -f k8s/deployment.yaml

Apply the Service:

kubectl apply -f k8s/service.yaml

Check the Deployment:

kubectl get deployment password-manager

Check the pods:

kubectl get pods -l app=password-manager

Check the Service:

kubectl get svc password-manager-service

Wait for the Deployment to complete:

kubectl rollout status deployment/password-manager
🔄 Rolling Deployment

The application uses Kubernetes RollingUpdate.

A new Docker image can be deployed using:

kubectl set image deployment/password-manager \
  password-manager=nidhi8901/web-based-password-manager:9

Then verify the rollout:

kubectl rollout status deployment/password-manager

Check the pods:

kubectl get pods -l app=password-manager

During the rolling update, Kubernetes gradually replaces the old application pods with the new ones.

This helps avoid replacing all application pods at the same time.

↩️ Rollback

Kubernetes rollout history can be checked using:

kubectl rollout history deployment/password-manager

If a previous deployment needs to be restored:

kubectl rollout undo deployment/password-manager

Then verify:

kubectl rollout status deployment/password-manager

Finally:

kubectl get pods -l app=password-manager

The Jenkins pipeline also contains a Rollback Test stage to demonstrate the rollback process automatically.

✅ Deployment Verification

The Jenkins Verify stage checks:

Deployment
kubectl get deployment password-manager
Pods
kubectl get pods -l app=password-manager -o wide
Service
kubectl get service password-manager-service
Rollout
kubectl rollout status deployment/password-manager

A successful deployment should show:

3/3 replicas ready

and the application pods should be in:

Running

state.

🔎 Application Verification

The application can be accessed locally using Kubernetes port forwarding:

kubectl port-forward service/password-manager-service 8000:8000

Then open:

http://localhost:8000

The application can be tested by:

Opening the web application
Creating a user account
Logging in
Adding passwords
Viewing stored passwords
Testing password generation
Testing password updates
Checking the dashboard
📊 CI/CD Pipeline Result

The completed Jenkins pipeline contains these stages:

✓ Checkout SCM
✓ Checkout
✓ Build
✓ Test
✓ Package
✓ Docker Push
✓ Deploy
✓ Verify
✓ Rollback Test
✓ Post Actions

The pipeline successfully demonstrates:

GitHub integration
Automated CI/CD
Docker image creation
Automated testing
Docker Hub publishing
Kubernetes deployment
Rolling updates
Deployment verification
Rollback
📸 Project Evidence

Project screenshots and execution evidence are included in:

project screenshots.pdf

The evidence covers the application and DevOps workflow, including:

GitHub repository
GitHub webhook
Jenkins pipeline
Successful pipeline execution
Docker build and push
Kubernetes deployment
Kubernetes pods
Rolling deployment
Rollback
Application verification
📋 Week 9 CI/CD Implementation

This project demonstrates the following DevOps implementation:

Requirement	Implementation
Source Code Management	GitHub
CI/CD	Jenkins
Automated Testing	Docker-based tests
Containerization	Docker
Container Registry	Docker Hub
Environment Variables	ENCRYPTION_KEY
Deployment	Kubernetes
Orchestration	Kind / Kubernetes
Rolling Deployment	Kubernetes RollingUpdate
Verification	Jenkins + kubectl
Rollback	Kubernetes rollout undo
Webhook Automation	GitHub Webhook
Secrets Management	Jenkins Credentials + Kubernetes Secret
🎯 Key DevOps Concepts Demonstrated

Through this project, the following concepts were implemented:

Git and GitHub
GitHub Webhooks
Jenkins
CI/CD pipelines
Jenkins Pipeline syntax
Docker
Docker image tagging
Docker Hub
Automated testing
Environment variables
Jenkins credentials
Kubernetes Deployments
Kubernetes Services
Kubernetes Secrets
Kubernetes Pods
Rolling Updates
Deployment verification
Kubernetes Rollback
Local Kubernetes using Kind
💡 CI/CD Architecture
                    ┌─────────────────┐
                    │     Developer   │
                    └────────┬────────┘
                             │
                             │ git push
                             ▼
                    ┌─────────────────┐
                    │     GitHub      │
                    └────────┬────────┘
                             │
                       Webhook Trigger
                             │
                             ▼
                    ┌─────────────────┐
                    │     Jenkins     │
                    └────────┬────────┘
                             │
             ┌───────────────┼────────────────┐
             │               │                │
             ▼               ▼                ▼
          Build           Test            Package
             │               │                │
             └───────────────┼────────────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │    Docker Hub   │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │    Kubernetes   │
                    │      Kind       │
                    └────────┬────────┘
                             │
                ┌────────────┼────────────┐
                │            │            │
                ▼            ▼            ▼
             Deploy       Verify      Rollback
                │
                ▼
        Password Manager App
🧹 Repository Security

The repository is configured to avoid committing local secrets and generated application data.

Files such as:

.env
*.db
*.sqlite
passwords.json
__pycache__/
k8s/secret.yaml

are excluded from version control.

Only an example configuration is provided:

.env.example

No Docker Hub authentication token or actual encryption key should be stored in the source code.

📚 Learning Outcomes

This project helped demonstrate how an application can move from source code to an automated deployment environment.

The main workflow implemented was:

Code
 ↓
GitHub
 ↓
Jenkins
 ↓
Automated Testing
 ↓
Docker Build
 ↓
Docker Hub
 ↓
Kubernetes Deployment
 ↓
Rolling Update
 ↓
Verification
 ↓
Rollback

This provides practical experience with a complete entry-level DevOps CI/CD workflow.

👩‍💻 Author

Nidhi Kumari

# 🔐 Web-Based Password Manager

A web-based password manager built with **Python Flask** and extended with a complete **DevOps CI/CD workflow** using GitHub, Jenkins, Docker, Docker Hub, and Kubernetes.

The project demonstrates an end-to-end workflow from source-code commit to automated testing, container image publishing, Kubernetes deployment, rolling update, verification, and rollback.

---

## 📌 Project Overview

The Web-Based Password Manager is a Flask-based application for managing passwords through a web interface.

The project includes both application development and DevOps automation.

### Application capabilities

* User registration and login
* Password management
* Password generation
* Password strength checking
* Password updates
* Password listing
* Password expiry support
* Password hashing
* Password encryption
* Web-based interface

### DevOps capabilities

* Git-based source control
* GitHub integration
* Jenkins CI/CD
* GitHub webhook triggering
* Automated testing
* Docker containerization
* Docker Hub image publishing
* Kubernetes deployment
* Kubernetes rolling updates
* Deployment verification
* Kubernetes rollback
* Environment-based secret handling

---

# 🚀 DevOps Workflow

The project follows this workflow:

```text
Developer
    │
    │ git push
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
    ├── Rolling Update
    ├── Deployment Verification
    └── Rollback
    │
    ▼
Password Manager Application
```

---

# 🛠️ Technology Stack

| Technology            | Purpose                            |
| --------------------- | ---------------------------------- |
| Python                | Application development            |
| Flask                 | Web application framework          |
| Passlib               | Password hashing                   |
| Cryptography / Fernet | Data encryption                    |
| Git                   | Version control                    |
| GitHub                | Source code management             |
| Jenkins               | CI/CD automation                   |
| Docker                | Containerization                   |
| Docker Hub            | Container image registry           |
| Kubernetes            | Container orchestration            |
| Kind                  | Local Kubernetes cluster           |
| Bash                  | Automation and testing             |
| ngrok                 | Local Jenkins webhook connectivity |

---

# ✨ Application Features

* User registration and authentication
* Password storage and management
* Password generation
* Password strength checking
* Password updates
* Password listing
* Password expiry handling
* Password hashing
* Password encryption
* Web-based password management interface

---

# 📁 Project Structure

```text
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
```

### Important files

| File                      | Purpose                                                         |
| ------------------------- | --------------------------------------------------------------- |
| `app.py`                  | Core password-manager functionality                             |
| `web_app.py`              | Flask web application                                           |
| `key.py`                  | Key-related application utility                                 |
| `requirements.txt`        | Python dependencies                                             |
| `Dockerfile`              | Docker image configuration                                      |
| `Jenkinsfile`             | Jenkins CI/CD pipeline                                          |
| `test.sh`                 | Automated project validation                                    |
| `.env.example`            | Example environment configuration                               |
| `.gitignore`              | Prevents local secrets and generated files from being committed |
| `k8s/deployment.yaml`     | Kubernetes Deployment configuration                             |
| `k8s/service.yaml`        | Kubernetes Service configuration                                |
| `project screenshots.pdf` | Project and DevOps execution evidence                           |

---

# 🔐 Security and Secrets

The application uses an environment variable for the encryption key.

The actual encryption key should not be stored in source code or committed to GitHub.

The repository provides an example configuration:

```text
ENCRYPTION_KEY=your-fernet-encryption-key-here
```

through:

```text
.env.example
```

The actual `.env` file is excluded using `.gitignore`.

The repository also excludes local application data and generated files such as:

```text
.env
*.db
*.sqlite
*.sqlite3
passwords.json
__pycache__/
k8s/secret.yaml
```

For Kubernetes, the encryption key is provided through a Kubernetes Secret and referenced by the Deployment as the `ENCRYPTION_KEY` environment variable.

> Never store a real encryption key, password, Docker Hub token, Kubernetes credential, or other secret in this repository.

---

# 💻 Run the Application Locally

## 1. Clone the repository

```bash
git clone <repository-url>
cd web-based-password-manager
```

## 2. Create a virtual environment

### Linux / WSL / Git Bash

```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows

```powershell
python -m venv venv
venv\Scripts\activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Configure the encryption key

Create a local `.env` file based on `.env.example` and provide your local encryption key.

Example:

```text
ENCRYPTION_KEY=your-local-encryption-key
```

Do not commit the `.env` file.

## 5. Start the application

```bash
python web_app.py
```

The application runs on:

```text
http://localhost:8000
```

---

# 🐳 Docker

The application is containerized using Docker.

The Docker workflow is:

```text
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
```

## Build the image

```bash
docker build -t web-based-password-manager .
```

## Run the container

The application requires the encryption key as an environment variable.

```bash
docker run -d \
  --name password-manager \
  -p 8000:8000 \
  -e ENCRYPTION_KEY="your-local-encryption-key" \
  web-based-password-manager
```

Check the running container:

```bash
docker ps
```

Open the application:

```text
http://localhost:8000
```

---

# 🧪 Automated Testing

The project contains an automated testing script:

```text
test.sh
```

The script validates three areas.

### 1. Python syntax

```bash
python3 -m py_compile app.py web_app.py
```

### 2. Required Python packages

The project checks the required packages:

```text
flask
passlib
cryptography
bcrypt
```

### 3. Required project files

The test verifies the existence of:

```text
app.py
web_app.py
requirements.txt
Dockerfile
```

Run the tests locally:

```bash
chmod +x test.sh
./test.sh
```

Expected result:

```text
All tests passed successfully!
```

---

# ⚙️ Jenkins CI/CD

The CI/CD pipeline is defined in:

```text
Jenkinsfile
```

The Jenkins pipeline automates the application lifecycle:

```text
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
```

The pipeline uses the Docker image:

```text
nidhi8901/web-based-password-manager
```

and creates a build-specific image tag using the Jenkins build number.

---

# 🔄 Jenkins Pipeline Stages

## 1. Checkout

Jenkins checks out the latest source code from the GitHub repository.

```groovy
checkout scm
```

---

## 2. Build

The Build stage:

* Verifies required project files
* Builds the Docker image
* Tags the image using the Jenkins build number

Example image:

```text
nidhi8901/web-based-password-manager:<BUILD_NUMBER>
```

---

## 3. Test

Testing is performed using the newly built Docker image.

The pipeline checks:

* Required Python packages
* Python syntax
* Required application files

The pipeline reports:

```text
ALL TESTS PASSED
```

when the checks succeed.

---

## 4. Package

The build-specific image is also tagged as:

```text
latest
```

The resulting image tags are:

```text
nidhi8901/web-based-password-manager:<BUILD_NUMBER>
nidhi8901/web-based-password-manager:latest
```

---

## 5. Docker Push

Jenkins authenticates with Docker Hub using a Jenkins credential.

The credential is referenced by the ID:

```text
dockerhub_cred
```

The pipeline pushes both:

```text
<BUILD_NUMBER>
latest
```

Docker authentication details are not hard-coded in the Jenkinsfile.

---

# 🌐 GitHub Webhook Integration

GitHub is integrated with Jenkins using a webhook.

The workflow is:

```text
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
```

For the local Jenkins setup, ngrok was used to expose Jenkins for webhook delivery.

The Jenkins webhook endpoint is:

```text
/github-webhook/
```

A successful GitHub push can automatically trigger a Jenkins build.

Example Jenkins trigger:

```text
Started by GitHub push by Nidhi8901
```

> The ngrok public URL is intentionally not stored in this README because free ngrok sessions can change their public URL.

---

# ☸️ Kubernetes Deployment

The application is deployed to a local Kubernetes cluster using **Kind**.

Kubernetes configuration is stored in:

```text
k8s/
├── deployment.yaml
└── service.yaml
```

---

# 📦 Kubernetes Deployment Configuration

The Kubernetes Deployment runs:

```text
3 replicas
```

The application container exposes:

```text
8000
```

The Deployment uses the Kubernetes:

```text
RollingUpdate
```

strategy.

Configuration:

```yaml
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxUnavailable: 1
    maxSurge: 1
```

This allows Kubernetes to replace application pods gradually instead of replacing all replicas at once.

---

# 🔑 Kubernetes Secret

The Deployment obtains the application encryption key from a Kubernetes Secret.

Secret name:

```text
password-manager-secret
```

Environment variable:

```text
ENCRYPTION_KEY
```

The secret is referenced using:

```yaml
env:
  - name: ENCRYPTION_KEY
    valueFrom:
      secretKeyRef:
        name: password-manager-secret
        key: ENCRYPTION_KEY
```

The Kubernetes secret configuration is not committed to the repository.

A local secret can be created using:

```bash
kubectl create secret generic password-manager-secret \
  --from-literal=ENCRYPTION_KEY="your-local-encryption-key"
```

---

# 🌍 Kubernetes Service

The application is exposed using a Kubernetes NodePort Service.

```text
Service:
password-manager-service

Type:
NodePort

Port:
8000

Target Port:
8000

Node Port:
30080
```

Check the Service:

```bash
kubectl get service password-manager-service
```

---

# 🚀 Deploy to Kubernetes

Select the Kind Kubernetes context:

```bash
kubectl config use-context kind-kind
```

Create the application secret if it does not already exist:

```bash
kubectl create secret generic password-manager-secret \
  --from-literal=ENCRYPTION_KEY="your-local-encryption-key" \
  --dry-run=client -o yaml | kubectl apply -f -
```

Apply the Deployment:

```bash
kubectl apply -f k8s/deployment.yaml
```

Apply the Service:

```bash
kubectl apply -f k8s/service.yaml
```

Check the Deployment:

```bash
kubectl get deployment password-manager
```

Check the Pods:

```bash
kubectl get pods -l app=password-manager
```

Check the Service:

```bash
kubectl get svc password-manager-service
```

Wait for the rollout:

```bash
kubectl rollout status deployment/password-manager
```

---

# 🔄 Rolling Deployment

The Kubernetes Deployment uses the `RollingUpdate` strategy.

A specific image version can be deployed using:

```bash
kubectl set image deployment/password-manager \
  password-manager=nidhi8901/web-based-password-manager:9
```

Then check the rollout:

```bash
kubectl rollout status deployment/password-manager
```

Check the application pods:

```bash
kubectl get pods -l app=password-manager -o wide
```

Kubernetes gradually replaces old pods with new pods according to the configured rolling-update strategy.

---

# ↩️ Rollback

Deployment history can be viewed with:

```bash
kubectl rollout history deployment/password-manager
```

If a previous version needs to be restored:

```bash
kubectl rollout undo deployment/password-manager
```

Verify the rollback:

```bash
kubectl rollout status deployment/password-manager
```

Then check the Pods:

```bash
kubectl get pods -l app=password-manager
```

The Jenkins pipeline also includes a dedicated:

```text
Rollback Test
```

stage.

---

# 🔎 Deployment Verification

The Jenkins `Verify` stage checks the Kubernetes deployment using:

```bash
kubectl get deployment password-manager
```

Pods:

```bash
kubectl get pods -l app=password-manager -o wide
```

Service:

```bash
kubectl get service password-manager-service
```

Rollout status:

```bash
kubectl rollout status deployment/password-manager
```

A successful deployment is expected to show:

```text
3/3 replicas ready
```

with the application Pods in:

```text
Running
```

state.

---

# ❤️ Readiness and Liveness Probes

The Kubernetes Deployment uses TCP socket probes on port `8000`.

### Readiness probe

The readiness probe checks whether the application container is ready to receive traffic.

### Liveness probe

The liveness probe checks whether the application container is still running correctly.

These probes allow Kubernetes to monitor the application container during deployment.

---

# 🖥️ Application Verification

The application can be accessed locally using Kubernetes port forwarding:

```bash
kubectl port-forward service/password-manager-service 8000:8000
```

Then open:

```text
http://localhost:8000
```

Application verification includes:

1. Opening the web application
2. Registering a user
3. Logging in
4. Adding passwords
5. Viewing stored passwords
6. Testing password generation
7. Testing password updates
8. Checking the dashboard

---

# 🐳 Docker Hub

The Docker image used by the CI/CD pipeline is:

```text
nidhi8901/web-based-password-manager
```

The Jenkins pipeline publishes:

```text
latest
```

and build-number tags such as:

```text
9
10
11
```

This allows individual CI/CD builds to be identified and deployed.

---

# 📊 Complete Jenkins Pipeline

The completed Jenkins pipeline contains:

```text
✓ Checkout
✓ Build
✓ Test
✓ Package
✓ Docker Push
✓ Deploy
✓ Verify
✓ Rollback Test
✓ Post Actions
```

The pipeline therefore covers the complete workflow:

```text
Source Code
     ↓
Build
     ↓
Automated Test
     ↓
Docker Image
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
```

---

# 👩‍💻 What I Implemented

As part of the DevOps implementation, I worked on:

* Containerizing the Flask application using Docker
* Creating automated application validation tests
* Creating the Jenkins CI/CD pipeline
* Integrating GitHub with Jenkins using a webhook
* Building Docker images automatically
* Tagging Docker images using Jenkins build numbers
* Publishing Docker images to Docker Hub
* Configuring Kubernetes Deployment and Service
* Running three application replicas
* Configuring Kubernetes RollingUpdate
* Configuring readiness and liveness probes
* Managing the application encryption key using environment variables and Kubernetes Secrets
* Adding deployment verification
* Implementing Kubernetes rollback
* Testing the complete GitHub-to-Jenkins-to-Docker-to-Kubernetes workflow

---

# 📸 Project Evidence

The repository contains:

```text
project screenshots.pdf
```

The project evidence includes screenshots related to:

* GitHub repository
* GitHub webhook
* Successful Jenkins pipeline
* Jenkins console output
* Docker image build and push
* Kubernetes Deployment
* Kubernetes Pods
* Kubernetes Service
* Rolling deployment
* Rollback
* Application verification

---

# 📋 Week 9 Implementation

| Requirement            | Implementation                          |
| ---------------------- | --------------------------------------- |
| Source Code Management | GitHub                                  |
| CI/CD                  | Jenkins                                 |
| GitHub Automation      | GitHub Webhook                          |
| Automated Testing      | Docker-based validation                 |
| Containerization       | Docker                                  |
| Image Registry         | Docker Hub                              |
| Image Tagging          | Jenkins build number + latest           |
| Environment Variables  | `ENCRYPTION_KEY`                        |
| Secrets                | Jenkins Credentials + Kubernetes Secret |
| Deployment             | Kubernetes                              |
| Kubernetes Environment | Kind                                    |
| Replicas               | 3                                       |
| Deployment Strategy    | RollingUpdate                           |
| Readiness              | TCP socket probe                        |
| Liveness               | TCP socket probe                        |
| Verification           | Jenkins + kubectl                       |
| Rollback               | Kubernetes `rollout undo`               |

---

# 🎯 DevOps Concepts Demonstrated

This project provides practical implementation experience with:

* Linux
* Git
* GitHub
* GitHub Webhooks
* Jenkins
* Jenkins Pipeline
* CI/CD
* Docker
* Docker image tagging
* Docker Hub
* Automated testing
* Environment variables
* Jenkins Credentials
* Kubernetes
* Kubernetes Pods
* Kubernetes Deployments
* Kubernetes Services
* Kubernetes Secrets
* Kubernetes RollingUpdate
* Readiness probes
* Liveness probes
* Deployment verification
* Kubernetes rollback
* Kind

---

# 🏗️ CI/CD Architecture

```text
                    ┌─────────────────┐
                    │    Developer    │
                    └────────┬────────┘
                             │
                         git push
                             │
                             ▼
                    ┌─────────────────┐
                    │     GitHub      │
                    └────────┬────────┘
                             │
                         Webhook
                             │
                             ▼
                    ┌─────────────────┐
                    │     Jenkins     │
                    └────────┬────────┘
                             │
            ┌────────────────┼────────────────┐
            │                │                │
            ▼                ▼                ▼
         Checkout          Build            Test
            │                │                │
            └────────────────┼────────────────┘
                             │
                             ▼
                         Package
                             │
                             ▼
                      Docker Push
                             │
                             ▼
                    ┌─────────────────┐
                    │    Docker Hub   │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   Kubernetes    │
                    │      Kind       │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
              ▼              ▼              ▼
           Deploy         Verify        Rollback
              │
              ▼
      Password Manager App
```

---

# 🧹 Repository Security

The repository is configured to keep local secrets and generated application data out of version control.

The following types of files are excluded:

```text
.env
*.db
*.sqlite
*.sqlite3
passwords.json
__pycache__/
k8s/secret.yaml
```

The repository provides:

```text
.env.example
```

as a safe configuration template.

Sensitive credentials such as:

* Encryption keys
* Docker Hub tokens
* Jenkins credentials
* Kubernetes credentials

should be stored outside the source code.

---

# 📚 Learning Outcomes

This project demonstrates how a Flask application can be integrated into a complete DevOps workflow.

The implemented process is:

```text
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
Deployment Verification
  ↓
Rollback
```

The project provided practical experience with source control, CI/CD automation, containerization, container registries, Kubernetes deployment, deployment strategies, secrets handling, verification, and rollback.

---

# ⭐ Project Summary

The Web-Based Password Manager is a Flask application extended with a complete DevOps CI/CD pipeline.

The project demonstrates:

**GitHub → Jenkins → Automated Testing → Docker → Docker Hub → Kubernetes → Rolling Deployment → Verification → Rollback**

It provides a practical example of automating the application lifecycle from source-code changes through container build and registry publishing to Kubernetes deployment and recovery.

---

# 👩‍💻 Author

**Nidhi Kumari**

DevOps / Cloud & DevOps Learner

### Technologies explored

```text
Linux
Git
GitHub
Jenkins
Docker
Kubernetes
AWS
Terraform
Ansible
Python


CI/CD
```

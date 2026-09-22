# 🔐 Web-Based Password Manager

A web-based password manager built with **Python Flask** and extended with a complete **DevOps CI/CD and DevSecOps workflow** using GitHub, Jenkins, Docker, Docker Hub, Kubernetes, and Trivy.

The project demonstrates an end-to-end workflow from source-code changes to automated testing, security scanning, container image publishing, Kubernetes deployment, verification, and rollback testing.

---

## 📌 Project Overview

The Web-Based Password Manager is a Flask-based application for managing passwords through a web interface.

### Application capabilities

- User registration and login
- Password management
- Password generation
- Password strength checking
- Password updates
- Password listing
- Password expiry support
- Password hashing
- Password encryption
- Web-based interface

### DevOps capabilities

- Git-based source control
- GitHub integration
- GitHub Webhook
- Jenkins CI/CD
- Automated testing
- Docker containerization
- Docker Hub image publishing
- Kubernetes deployment
- Kubernetes rolling updates
- Deployment verification
- Kubernetes rollback
- Environment-based secret handling

### Week 9 DevSecOps improvements

- Docker image hardening
- Non-root container execution
- Docker build security improvements
- `.dockerignore` implementation
- Secret and generated-file exclusion
- Trivy vulnerability scanning
- Critical vulnerability pipeline gate
- Container user validation
- Docker health check
- Dependency/security review
- Production readiness review
- Kubernetes deployment verification

---

# 🚀 Complete DevOps / DevSecOps Workflow

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
    ├── Security Scan
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

| Technology | Purpose |
|---|---|
| Python | Application development |
| Flask | Web application framework |
| Passlib | Password hashing |
| Cryptography / Fernet | Data encryption |
| Git | Version control |
| GitHub | Source code management |
| Jenkins | CI/CD automation |
| Docker | Containerization |
| Docker Hub | Container image registry |
| Kubernetes | Container orchestration |
| Kind | Local Kubernetes cluster |
| Trivy | Container vulnerability scanning |
| Bash | Automation and testing |
| ngrok | Local Jenkins webhook connectivity |

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
├── .dockerignore
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

| File | Purpose |
|---|---|
| `app.py` | Core password-manager functionality |
| `web_app.py` | Flask web application |
| `key.py` | Key-related application utility |
| `requirements.txt` | Python dependencies |
| `Dockerfile` | Secure Docker image configuration |
| `.dockerignore` | Prevents unnecessary and sensitive files from entering the image |
| `Jenkinsfile` | Jenkins CI/CD and security pipeline |
| `test.sh` | Automated project validation |
| `.env.example` | Example environment configuration |
| `.gitignore` | Prevents secrets and generated files from being committed |
| `k8s/deployment.yaml` | Kubernetes Deployment configuration |
| `k8s/service.yaml` | Kubernetes Service configuration |

---

# 🔐 Security and Secrets

The application uses an environment variable for the encryption key.

The actual encryption key is not stored in source code.

Example configuration:

```text
ENCRYPTION_KEY=your-fernet-encryption-key-here
```

The example configuration is provided through:

```text
.env.example
```

The actual `.env` file is excluded from Git.

The repository also excludes local application data and generated files such as:

```text
.env
*.db
*.sqlite
*.sqlite3
passwords.json
__pycache__/
```

Sensitive information such as:

- Encryption keys
- Docker Hub credentials
- Jenkins credentials
- Kubernetes credentials

must not be committed to the repository.

---

# 🐳 Docker

The application is containerized using Docker.

## Week 9 Secure Dockerfile

The Docker image was hardened during Week 9.

The security improvements include:

- Updating Debian packages
- Upgrading pip, setuptools and wheel
- Installing only required Python dependencies
- Creating a dedicated non-root `appuser`
- Running the application as `appuser`
- Using `COPY --chown`
- Adding a Docker health check
- Removing apt package lists after installation
- Excluding secrets and unnecessary files through `.dockerignore`

The container no longer runs the application as the root user.

---

# 🛡️ Docker Security Improvements

### Non-root user

The image creates:

```text
appuser
```

and the application runs using:

```dockerfile
USER appuser
```

The Jenkins pipeline also verifies that the resulting container does not run as UID `0`.

### Health check

The Docker image includes a health check:

```dockerfile
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/', timeout=3)" || exit 1
```

### `.dockerignore`

The following files are excluded from the Docker build context:

```text
.git
.gitignore
.env
.env.*
__pycache__
*.pyc
*.pyo
*.pyd
.venv
venv
password_manager.db
*.db
*.json
trivy-before.txt
trivy-high-critical.txt
trivy.exe
trivy.zip
trivy-after.txt
```

This prevents local secrets, databases, scanner files and generated files from unnecessarily entering the Docker image.

---

# 🧪 Automated Testing

The project contains:

```text
test.sh
```

The test script validates:

### Python syntax

```bash
python3 -m py_compile app.py web_app.py
```

### Required Python packages

```text
flask
passlib
cryptography
bcrypt
```

### Required project files

```text
app.py
web_app.py
requirements.txt
Dockerfile
```

Run locally:

```bash
chmod +x test.sh
./test.sh
```

Expected result:

```text
All tests passed successfully!
```

The Jenkins pipeline also performs application and container validation.

---

# 🔒 DevSecOps Security Scanning

Week 9 introduced Trivy container vulnerability scanning into the CI/CD pipeline.

The Jenkins pipeline uses:

```text
aquasec/trivy:0.74.0
```

The security stage performs:

1. HIGH and CRITICAL vulnerability reporting
2. CRITICAL vulnerability gating

The pipeline is configured so that HIGH findings are reported without automatically stopping the build, while a CRITICAL vulnerability causes the security gate to fail.

Example:

```bash
docker run --rm \
    -v /var/run/docker.sock:/var/run/docker.sock \
    aquasec/trivy:0.74.0 \
    image \
    --severity HIGH,CRITICAL \
    --exit-code 0 \
    ${DOCKER_IMAGE}:${IMAGE_TAG}
```

Critical vulnerability gate:

```bash
docker run --rm \
    -v /var/run/docker.sock:/var/run/docker.sock \
    aquasec/trivy:0.74.0 \
    image \
    --severity CRITICAL \
    --exit-code 1 \
    ${DOCKER_IMAGE}:${IMAGE_TAG}
```

---

# 📊 Week 9 Security Scan Results

## Before Security Improvements

The initial Trivy scan reported:

```text
Total: 180

UNKNOWN: 2
LOW: 58
MEDIUM: 63
HIGH: 54
CRITICAL: 3
```

The initial image therefore contained:

```text
3 CRITICAL vulnerabilities
54 HIGH vulnerabilities
```

---

## After Security Improvements

After Dockerfile hardening, `.dockerignore` improvements and removal of unnecessary scanner files from the image, the final scan reported:

```text
Total: 152

UNKNOWN: 2
LOW: 57
MEDIUM: 49
HIGH: 44
CRITICAL: 0
```

The final scan therefore achieved:

```text
CRITICAL: 0
```

The remaining findings were primarily associated with operating-system packages in the Debian base image.

A separate Python dependency scan reported:

```text
Total: 3

UNKNOWN: 0
LOW: 0
MEDIUM: 1
HIGH: 2
CRITICAL: 0
```

The remaining dependency findings should be reviewed and upgraded where compatible fixes are available.

> Security scanning is part of the CI/CD process, but a zero-vulnerability result should not be assumed from this scan. Remaining non-critical findings require continued dependency and base-image maintenance.

---

# ⚙️ Jenkins CI/CD

The CI/CD pipeline is defined in:

```text
Jenkinsfile
```

The final Week 9 pipeline contains:

```text
Checkout
    ↓
Build
    ↓
Test
    ↓
Security Scan
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

---

# 🔄 Jenkins Pipeline Stages

## 1. Checkout

Jenkins checks out the latest source code from GitHub.

---

## 2. Build

The pipeline:

- Checks required project files
- Builds the Docker image
- Creates a build-specific image tag

Example:

```text
nidhi8901/web-based-password-manager:<BUILD_NUMBER>
```

---

## 3. Test

The pipeline validates:

- Python syntax
- Required packages
- Required files
- Container configuration
- Non-root container execution

The non-root check verifies that the container user ID is not:

```text
0
```

---

## 4. Security Scan

Trivy scans the Docker image for:

```text
HIGH
CRITICAL
```

vulnerabilities.

The pipeline reports HIGH and CRITICAL findings and uses a separate CRITICAL-only gate.

---

## 5. Package

The build image is also tagged:

```text
latest
```

Resulting tags:

```text
nidhi8901/web-based-password-manager:<BUILD_NUMBER>
nidhi8901/web-based-password-manager:latest
```

---

## 6. Docker Push

Jenkins authenticates to Docker Hub using the Jenkins credential:

```text
dockerhub_cred
```

Credentials are not hard-coded in the Jenkinsfile.

The pipeline pushes:

```text
<BUILD_NUMBER>
latest
```

---

# 🌐 GitHub Webhook Integration

GitHub is integrated with Jenkins using a webhook.

Workflow:

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

For the local Jenkins environment, ngrok was used to expose Jenkins for webhook delivery.

The Jenkins webhook endpoint is:

```text
/github-webhook/
```

A successful trigger appears in Jenkins as:

```text
Started by GitHub push by Nidhi8901
```

The temporary ngrok URL is intentionally not stored in this README because free ngrok URLs can change.

---

# ☸️ Kubernetes Deployment

The application is deployed to a local Kubernetes cluster using Kind.

Kubernetes configuration:

```text
k8s/
├── deployment.yaml
└── service.yaml
```

The Kubernetes environment used for the final Week 9 pipeline was:

```text
Kind
Kubernetes v1.30.0
```

The final cluster contained:

```text
kind-control-plane
```

with status:

```text
Ready
```

---

# 📦 Kubernetes Deployment

The application deployment uses:

```text
3 replicas
```

The application container exposes:

```text
8000
```

The deployment uses:

```text
RollingUpdate
```

strategy.

Example:

```yaml
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxUnavailable: 1
    maxSurge: 1
```

---

# 🔑 Kubernetes Secrets

The application encryption key is supplied through a Kubernetes Secret.

Secret:

```text
password-manager-secret
```

Environment variable:

```text
ENCRYPTION_KEY
```

The application secret is not stored as plaintext in the Git repository.

---

# 🌍 Kubernetes Service

The application is exposed through a Kubernetes Service.

The service configuration is stored in:

```text
k8s/service.yaml
```

The service provides access to the application running on port:

```text
8000
```

---

# 🔎 Deployment Verification

The Jenkins Verify stage checks the Kubernetes deployment using commands such as:

```bash
kubectl get deployment password-manager
```

```bash
kubectl get pods -l app=password-manager -o wide
```

```bash
kubectl get service password-manager-service
```

```bash
kubectl rollout status deployment/password-manager
```

The purpose of the verification stage is to confirm that the application has successfully reached the expected Kubernetes deployment state.

---

# ↩️ Kubernetes Rollback

Deployment history can be checked using:

```bash
kubectl rollout history deployment/password-manager
```

A previous version can be restored with:

```bash
kubectl rollout undo deployment/password-manager
```

Then verify:

```bash
kubectl rollout status deployment/password-manager
```

The Jenkins pipeline also contains a dedicated:

```text
Rollback Test
```

stage.

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
             ┌───────────────┼───────────────┐
             │               │               │
             ▼               ▼               ▼
          Build            Test       Security Scan
             │               │               │
             └───────────────┼───────────────┘
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

The repository uses `.gitignore` and `.dockerignore` to prevent sensitive and unnecessary files from being committed or copied into Docker images.

Examples:

```text
.env
*.db
*.sqlite
*.sqlite3
passwords.json
__pycache__/
trivy.exe
trivy.zip
trivy-before.txt
trivy-after.txt
trivy-high-critical.txt
```

The repository provides:

```text
.env.example
```

as a safe configuration template.

---

# 📋 Week 9 DevSecOps Implementation

| Requirement | Implementation |
|---|---|
| CI/CD Review | Jenkins pipeline reviewed and updated |
| YAML/Configuration Review | Kubernetes deployment and service reviewed |
| Container Security | Dockerfile hardened |
| Non-root Execution | `appuser` implemented |
| Docker Health Check | Implemented |
| Secret Protection | `.env` excluded |
| Docker Build Context | `.dockerignore` implemented |
| Vulnerability Scanning | Trivy |
| Security Gate | CRITICAL vulnerability gate |
| Automated Testing | Jenkins Test stage |
| Container Validation | Non-root user validation |
| Image Registry | Docker Hub |
| Deployment | Kubernetes |
| Deployment Strategy | RollingUpdate |
| Verification | Jenkins Verify stage |
| Rollback | Jenkins Rollback Test |
| GitHub Automation | GitHub Webhook |
| Production Readiness | Reviewed and documented |

---

# 📊 Before and After Security Summary

| Security Area | Before Week 9 | After Week 9 |
|---|---|---|
| Docker user | Root | Non-root `appuser` |
| Docker health check | Not implemented | Implemented |
| `.dockerignore` | Limited/absent | Implemented |
| Local scanner files in image | Possible | Excluded |
| Trivy CRITICAL findings | 3 | 0 |
| Trivy HIGH findings | 54 | 44 |
| Trivy total findings | 180 | 152 |
| CI security scanning | Not integrated | Integrated |
| Critical security gate | Not implemented | Implemented |
| Kubernetes deployment verification | Implemented | Retained |
| Rollback testing | Implemented | Retained |

---

# ✅ Final Production Readiness Status

The final Week 9 pipeline was successfully executed.

The final workflow completed:

```text
✓ GitHub Webhook
✓ Jenkins Checkout
✓ Build
✓ Test
✓ Security Scan
✓ Docker Image Build
✓ Docker Hub Push
✓ Kubernetes Deployment
✓ Deployment Verification
✓ Rollback Test
```

The final pipeline successfully demonstrated an automated application delivery workflow with DevSecOps controls.

---

# 🎯 DevOps Concepts Demonstrated

This project provides practical implementation experience with:

- Linux
- Git
- GitHub
- GitHub Webhooks
- Jenkins
- Jenkins Pipeline
- CI/CD
- Docker
- Docker image tagging
- Docker Hub
- Trivy
- Container security
- Non-root containers
- Environment variables
- Jenkins Credentials
- Kubernetes
- Kubernetes Pods
- Kubernetes Deployments
- Kubernetes Services
- Kubernetes Secrets
- Kubernetes RollingUpdate
- Readiness and liveness concepts
- Deployment verification
- Kubernetes rollback
- Kind

---

# 📚 Learning Outcomes

This project demonstrates how a Flask application can be integrated into a complete DevOps and DevSecOps workflow.

The implemented process is:

```text
Code
  ↓
GitHub
  ↓
GitHub Webhook
  ↓
Jenkins
  ↓
Automated Testing
  ↓
Security Scan
  ↓
Docker Build
  ↓
Docker Hub
  ↓
Kubernetes Deployment
  ↓
Deployment Verification
  ↓
Rollback
```

The project provided practical experience with source control, CI/CD automation, containerization, security scanning, container hardening, registry publishing, Kubernetes deployment, deployment strategies, secret handling, verification, and rollback.

---

# ⭐ Project Summary

The Web-Based Password Manager is a Flask application extended with a complete DevOps and DevSecOps pipeline.

The final workflow demonstrates:

**GitHub → Jenkins → Testing → Trivy Security Scan → Docker → Docker Hub → Kubernetes → Verification → Rollback**

The project provides a practical example of automating the application lifecycle from source-code changes through security validation, container build, registry publishing, Kubernetes deployment, verification, and recovery.

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
Docker Hub
Kubernetes
Kind
Trivy
AWS
Terraform
Ansible
Python
CI/CD
```
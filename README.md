# 🔐 Password Manager Web App

A simple, secure, multi-tenant **web-based password manager** built for a DevOps intern-level assignment.

---

## 📌 Features

* ✅ Multi-tenant user system (multiple users supported)
* 🔐 Secure password storage (encrypted backend)
* 📋 List saved passwords
* ✏️ Update existing passwords
* ⏰ Password expiry support
* 🛡️ Password strength validation
* 🔁 Auto-generate strong passwords
* 🌐 Web-based UI (runs on localhost)

---

## 🛠 Tech Stack

* **Backend:** Python, Flask
* **Database:** SQLite
* **Security:** passlib (password hashing), cryptography (encryption)
* **Containerization:** Docker

---

## 🚀 How to Run Locally

### 1️⃣ Install Dependencies

```bash
pip install flask passlib cryptography
```

---

### 2️⃣ Set Encryption Key (Required)

**Windows (PowerShell):**

```powershell
setx ENCRYPTION_KEY "mysecretkey"
```

**Windows (Git Bash):**

```bash
export ENCRYPTION_KEY=mysecretkey
```

Restart terminal after setting.

---

### 3️⃣ Run the Web App

```bash
python web_app.py
```

---

### 4️⃣ Open in Browser

```
http://localhost:8000
```

---

## 🐳 Run with Docker

### Build Image

```bash
docker build -t password-manager .
```

### Run Container

```bash
docker run -p 8000:8000 -e ENCRYPTION_KEY=mysecretkey password-manager
```

---

## 🎯 Core Functionalities

| Feature                 | Status |
| ----------------------- | ------ |
| User Registration       | ✅      |
| Login Authentication    | ✅      |
| Add Password            | ✅      |
| Update Password         | ✅      |
| List Passwords          | ✅      |
| Password Expiry         | ✅      |
| Auto Password Generator | ✅      |
| Secure Storage          | ✅      |

---

## 🧪 Testing

Basic tests have been run manually via UI and CLI and all core features are working as expected.

---

## 🎤 Interview Explanation (Simple)

> "This is a secure, multi-user password manager built using Flask. Passwords are encrypted before storage, users can add, update, and list their passwords, and the app enforces password strength rules and expiry. It is containerized using Docker and runs locally on localhost."

---

## 📁 Project Structure

```
Web-based-password-manager/
│
├── app.py              # Core backend logic
├── web_app.py          # Flask web server
├── requirements.txt    # Python dependencies
├── Dockerfile          # Container configuration
├── passwords.db        # SQLite database (auto-created)
└── README.md           # Project documentation
```

---

## ✅ Assignment Compliance

This project fully satisfies the assignment requirements:

✔ CLI/Web-based password manager
✔ Multi-tenant
✔ Secure password storage
✔ Add, list, update passwords
✔ Password expiry
✔ Password strength compliance
✔ Auto-generation of passwords

---
Webhook test

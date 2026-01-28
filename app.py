import os
import sqlite3
import re
import base64
from datetime import datetime
from passlib.context import CryptContext
from cryptography.fernet import Fernet

# ----------------- CONFIG -----------------

DB_NAME = "password_manager.db"
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")

if not ENCRYPTION_KEY:
    raise ValueError("ENCRYPTION_KEY environment variable not set")

fernet = Fernet(base64.urlsafe_b64encode(ENCRYPTION_KEY.encode().ljust(32)[:32]))
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# ----------------- DATABASE -----------------

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT DEFAULT 'user'
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            service TEXT,
            account TEXT,
            password TEXT,
            expiry TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    conn.commit()
    conn.close()

# ----------------- UTILITIES -----------------

def hash_password(password):
    return pwd_context.hash(password)

def verify_password(password, hashed):
    return pwd_context.verify(password, hashed)

def encrypt_password(password):
    return fernet.encrypt(password.encode()).decode()

def decrypt_password(encrypted):
    return fernet.decrypt(encrypted.encode()).decode()

def is_strong_password(password):
    return (
        len(password) >= 8 and
        re.search(r"[A-Z]", password) and
        re.search(r"[a-z]", password) and
        re.search(r"[0-9]", password) and
        re.search(r"[!@#$%^&*()_+=\-{}[\]:;'\"<>,.?/]", password)
    )

def generate_password():
    import secrets
    import string
    chars = string.ascii_letters + string.digits + "!@#$%^&*()_+-="
    return "".join(secrets.choice(chars) for _ in range(12))

# ----------------- USER MANAGEMENT -----------------

def register_user(username, password, role="user"):
    if not is_strong_password(password):
        raise ValueError("Weak password")

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                  (username, hash_password(password), role))
        conn.commit()
    except sqlite3.IntegrityError:
        raise ValueError("Username already exists")
    finally:
        conn.close()

def login_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, password, role FROM users WHERE username=?", (username,))
    row = c.fetchone()
    conn.close()
    if not row or not verify_password(password, row[1]):
        raise ValueError("Invalid credentials")
    return row[0], row[2]

# ----------------- PASSWORD MANAGEMENT -----------------

def add_password(user_id, service, account, password, expiry):
    if not is_strong_password(password):
        raise ValueError("Weak password")
    encrypted = encrypt_password(password)
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        INSERT INTO passwords (user_id, service, account, password, expiry)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, service, account, encrypted, expiry))
    conn.commit()
    conn.close()

def list_passwords(user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        SELECT id, service, account, expiry FROM passwords
        WHERE user_id=?
    """, (user_id,))
    rows = c.fetchall()
    conn.close()
    return rows

def update_password(user_id, password_id, new_password, new_expiry):
    if not is_strong_password(new_password):
        raise ValueError("Weak password")
    encrypted = encrypt_password(new_password)
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        UPDATE passwords
        SET password=?, expiry=?
        WHERE id=? AND user_id=?
    """, (encrypted, new_expiry, password_id, user_id))
    conn.commit()
    conn.close()

def view_password(user_id, password_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        SELECT password FROM passwords
        WHERE id=? AND user_id=?
    """, (password_id, user_id))
    row = c.fetchone()
    conn.close()
    if not row:
        raise ValueError("Password not found")
    return decrypt_password(row[0])
import random
import string


# ----------------- SUPERADMIN VIEW -----------------

def view_password_as_superadmin(super_username, super_password, password_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, password, role FROM users WHERE username=?", (super_username,))
    row = c.fetchone()
    if not row or not verify_password(super_password, row[1]) or row[2] != "superadmin":
        conn.close()
        raise ValueError("Unauthorized")
    c.execute("SELECT password FROM passwords WHERE id=?", (password_id,))
    row = c.fetchone()
    conn.close()
    if not row:
        raise ValueError("Password not found")
    return decrypt_password(row[0])
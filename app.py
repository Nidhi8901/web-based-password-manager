# main.py
# Simple Password Manager (CLI-based, Intern-friendly)
# Rewritten to avoid FastAPI/SSL dependency issues
# Implements ONLY the listed assignment requirements

import sqlite3
from datetime import datetime
from passlib.context import CryptContext
from cryptography.fernet import Fernet
import re
import os
import secrets

# ---------------- CONFIG ----------------
DB_FILE = "password_manager.db"
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY") or Fernet.generate_key()
fernet = Fernet(ENCRYPTION_KEY)

# Use PBKDF2 instead of bcrypt to avoid Windows bcrypt backend issues
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# ---------------- DB SETUP ----------------
def get_db():
    return sqlite3.connect(DB_FILE)


def init_db():
    db = get_db()
    cur = db.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password_hash TEXT,
        created_at TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS passwords (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        service_name TEXT,
        username TEXT,
        encrypted_password TEXT,
        expires_at TEXT,
        created_at TEXT,
        updated_at TEXT
    )
    """)

    db.commit()
    db.close()

# ---------------- SECURITY UTILS ----------------
def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(password: str, hashed: str):
    return pwd_context.verify(password, hashed)


def encrypt_password(password: str):
    return fernet.encrypt(password.encode()).decode()


def decrypt_password(enc_password: str):
    return fernet.decrypt(enc_password.encode()).decode()


def is_strong_password(password: str):
    return (
        len(password) >= 8 and
        re.search(r"[A-Z]", password) and
        re.search(r"[a-z]", password) and
        re.search(r"[0-9]", password) and
        re.search(r"[^A-Za-z0-9]", password)
    )

# ---------------- CORE FUNCTIONS ----------------
def register_user(username: str, password: str):
    if not is_strong_password(password):
        raise ValueError("Weak password")

    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT id FROM users WHERE username=?", (username,))
    if cur.fetchone():
        db.close()
        raise ValueError("User already exists")

    cur.execute(
        "INSERT INTO users (username, password_hash, created_at) VALUES (?, ?, ?)",
        (username, hash_password(password), datetime.utcnow().isoformat())
    )
    db.commit()
    db.close()


def login_user(username: str, password: str):
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT id, password_hash FROM users WHERE username=?", (username,))
    row = cur.fetchone()
    db.close()

    if not row or not verify_password(password, row[1]):
        raise ValueError("Invalid credentials")

    return row[0]  # user_id


def add_password(user_id: int, service: str, username: str, password: str, expires_at: str):
    if not is_strong_password(password):
        raise ValueError("Weak password")

    db = get_db()
    cur = db.cursor()
    cur.execute(
        "INSERT INTO passwords VALUES (NULL, ?, ?, ?, ?, ?, ?, ?)",
        (
            user_id,
            service,
            username,
            encrypt_password(password),
            expires_at,
            datetime.utcnow().isoformat(),
            datetime.utcnow().isoformat()
        )
    )
    db.commit()
    db.close()


def list_passwords(user_id: int):
    db = get_db()
    cur = db.cursor()
    cur.execute(
        "SELECT id, service_name, username, expires_at FROM passwords WHERE user_id=?",
        (user_id,)
    )
    rows = cur.fetchall()
    db.close()
    return rows


def view_password(user_id: int, password_id: int):
    db = get_db()
    cur = db.cursor()
    cur.execute(
        "SELECT service_name, username, encrypted_password, expires_at FROM passwords WHERE id=? AND user_id=?",
        (password_id, user_id)
    )
    row = cur.fetchone()
    db.close()

    if not row:
        raise ValueError("Password not found")

    return row[0], row[1], decrypt_password(row[2]), row[3]


def update_password(user_id: int, password_id: int, new_password: str, new_expiry: str):
    if not is_strong_password(new_password):
        raise ValueError("Weak password")

    db = get_db()
    cur = db.cursor()
    cur.execute(
        "UPDATE passwords SET encrypted_password=?, expires_at=?, updated_at=? WHERE id=? AND user_id=?",
        (
            encrypt_password(new_password),
            new_expiry,
            datetime.utcnow().isoformat(),
            password_id,
            user_id
        )
    )
    db.commit()
    db.close()


def generate_password():
    """
    Generate a strong password that ALWAYS satisfies the strength rules:
    - At least 1 uppercase
    - At least 1 lowercase
    - At least 1 digit
    - At least 1 special character
    - Minimum length 12
    """
    lower = secrets.choice("abcdefghijklmnopqrstuvwxyz")
    upper = secrets.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    digit = secrets.choice("0123456789")
    special = secrets.choice("!@#$%^&*")

    remaining = ''.join(
        secrets.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*")
        for _ in range(8)
    )

    password = list(lower + upper + digit + special + remaining)
    secrets.SystemRandom().shuffle(password)

    return ''.join(password)

# ---------------- BASIC TESTS ----------------
# Note: Uses pbkdf2_sha256 for hashing to ensure compatibility on Windows
if __name__ == "__main__":
    init_db()

    # Simple sanity tests
    try:
        register_user("testuser", "Strong@123")
    except ValueError:
        pass

    uid = login_user("testuser", "Strong@123")

    pwd = generate_password()
    add_password(uid, "Gmail", "test@gmail.com", pwd, "2025-12-31")

    items = list_passwords(uid)
    assert len(items) >= 1

    sid = items[0][0]
    service, uname, secret, expiry = view_password(uid, sid)
    assert secret

    update_password(uid, sid, "NewStrong@456", "2026-01-01")

    print("All basic tests passed.")
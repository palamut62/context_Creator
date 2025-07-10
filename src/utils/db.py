import os
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Dict
from cryptography.fernet import Fernet


DATA_DIR = Path(__file__).resolve().parent.parent.parent / 'data'
DB_PATH = DATA_DIR / 'app.db'
KEY_PATH = DATA_DIR / 'fernet.key'


def _ensure_dirs():
    DATA_DIR.mkdir(exist_ok=True)


def _get_fernet():
    _ensure_dirs()
    if not KEY_PATH.exists():
        KEY_PATH.write_bytes(Fernet.generate_key())
    key = KEY_PATH.read_bytes()
    return Fernet(key)


def init_db():
    _ensure_dirs()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS api_keys (
            provider TEXT PRIMARY KEY,
            secret TEXT NOT NULL,
            model TEXT,
            updated_at TEXT NOT NULL
        )
        """
    )
    conn.commit()

    # ensure model column exists
    try:
        cur.execute("PRAGMA table_info(api_keys)")
        cols = [row[1] for row in cur.fetchall()]
        if 'model' not in cols:
            cur.execute("ALTER TABLE api_keys ADD COLUMN model TEXT")
            conn.commit()
    except Exception:
        pass

    conn.close()


def save_api_keys(settings: Dict[str, Dict[str, str]]):
    """Insert or update provided keys dict into DB (encrypted)."""
    if not settings:
        return
    f = _get_fernet()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    for provider, info in settings.items():
        secret = info.get('api_key', '')
        model = info.get('model')
        encrypted = f.encrypt(secret.encode()).decode() if secret else ''
        cur.execute(
            """
            INSERT INTO api_keys(provider, secret, model, updated_at)
            VALUES(?, ?, ?, ?)
            ON CONFLICT(provider) DO UPDATE SET secret=excluded.secret, model=excluded.model, updated_at=excluded.updated_at
            """,
            (provider, encrypted, model, datetime.utcnow().isoformat())
        )
    conn.commit()
    conn.close()


def load_api_keys() -> Dict[str, Dict[str, str]]:
    """Return dict {provider: {'api_key': secret, 'model': model}}"""
    f = _get_fernet()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT provider, secret, model FROM api_keys")
    rows = cur.fetchall()
    conn.close()
    result = {}
    for provider, secret, model in rows:
        try:
            decrypted = f.decrypt(secret.encode()).decode()
        except Exception:
            decrypted = ''
        result[provider] = {'api_key': decrypted, 'model': model}
    return result 
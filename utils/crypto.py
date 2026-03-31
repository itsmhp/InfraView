"""Fernet-based encryption for dashboard content stored in the database."""
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from flask import current_app

PREFIX = 'enc:v1:'
_SALT = b'infraview-dashboard-encryption-v1'


def _get_fernet():
    """Derive a Fernet key from the app's ENCRYPTION_KEY or SECRET_KEY."""
    secret = current_app.config.get('ENCRYPTION_KEY') or current_app.config['SECRET_KEY']
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=_SALT,
        iterations=480_000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(secret.encode('utf-8')))
    return Fernet(key)


def encrypt_content(plaintext):
    """Encrypt a string. Returns prefixed ciphertext suitable for DB storage."""
    if not plaintext:
        return plaintext
    f = _get_fernet()
    token = f.encrypt(plaintext.encode('utf-8'))
    return PREFIX + token.decode('ascii')


def decrypt_content(stored):
    """Decrypt stored content. Returns plaintext. Handles unencrypted data gracefully."""
    if not stored or not stored.startswith(PREFIX):
        return stored
    f = _get_fernet()
    token = stored[len(PREFIX):].encode('ascii')
    return f.decrypt(token).decode('utf-8')

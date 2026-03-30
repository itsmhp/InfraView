import re
from datetime import datetime, timezone
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from models import db


def validate_password(password):
    """Validate password strength. Returns error message or None if valid."""
    if len(password) < 8:
        return 'Password minimal 8 karakter.'
    if not re.search(r'[A-Z]', password):
        return 'Password harus mengandung huruf besar.'
    if not re.search(r'[a-z]', password):
        return 'Password harus mengandung huruf kecil.'
    if not re.search(r'[0-9]', password):
        return 'Password harus mengandung angka.'
    return None


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    display_name = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='viewer')  # 'admin' or 'viewer'
    is_active_user = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    last_login = db.Column(db.DateTime, nullable=True)
    must_change_password = db.Column(db.Boolean, default=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_active(self):
        return self.is_active_user

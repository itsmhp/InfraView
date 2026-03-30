import time
from collections import defaultdict
from datetime import datetime, timezone
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from models import db
from models.user import User, validate_password

auth_bp = Blueprint('auth', __name__)

# Simple in-memory rate limiter
_login_attempts = defaultdict(list)


def _is_rate_limited(ip, max_attempts=5, window=300):
    """Check if IP has exceeded login attempts (5 per 5 minutes)."""
    now = time.time()
    _login_attempts[ip] = [t for t in _login_attempts[ip] if now - t < window]
    if len(_login_attempts[ip]) >= max_attempts:
        return True
    _login_attempts[ip].append(now)
    return False


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.hub'))

    if request.method == 'POST':
        # Rate limit check
        if _is_rate_limited(request.remote_addr):
            flash('Terlalu banyak percobaan login. Coba lagi dalam 5 menit.', 'error')
            return render_template('login.html')

        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password) and user.is_active:
            # Record login time
            user.last_login = datetime.now(timezone.utc)
            db.session.commit()
            login_user(user, remember=True)
            next_page = request.args.get('next')
            flash(f'Selamat datang, {user.display_name}!', 'success')
            return redirect(next_page or url_for('main.hub'))

        flash('Username atau password salah.', 'error')

    return render_template('login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Anda telah logout.', 'info')
    return redirect(url_for('auth.login'))


@auth_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        new_password = request.form.get('new_password', '')
        confirm = request.form.get('confirm_password', '')

        if new_password != confirm:
            flash('Password tidak cocok.', 'error')
            return redirect(request.url)

        error = validate_password(new_password)
        if error:
            flash(error, 'error')
            return redirect(request.url)

        current_user.set_password(new_password)
        current_user.must_change_password = False
        db.session.commit()
        flash('Password berhasil diubah!', 'success')
        return redirect(url_for('main.hub'))

    return render_template('change_password.html')

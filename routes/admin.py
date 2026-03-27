from datetime import datetime, timezone
from functools import wraps
from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from models import db
from models.user import User
from models.dashboard import Dashboard

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


def admin_required(f):
    @wraps(f)
    @login_required
    def decorated(*args, **kwargs):
        if not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated


@admin_bp.route('/')
@admin_required
def panel():
    dashboards = Dashboard.query.order_by(Dashboard.sort_order).all()
    users = User.query.order_by(User.created_at).all()
    return render_template('admin/panel.html', dashboards=dashboards, users=users)


@admin_bp.route('/upload/<slug>', methods=['GET', 'POST'])
@admin_required
def upload(slug):
    dashboard = Dashboard.query.filter_by(slug=slug).first_or_404()

    if request.method == 'POST':
        file = request.files.get('html_file')

        if not file or file.filename == '':
            flash('Tidak ada file yang dipilih.', 'error')
            return redirect(request.url)

        if not file.filename.lower().endswith(('.html', '.htm')):
            flash('Hanya file .html atau .htm yang diperbolehkan.', 'error')
            return redirect(request.url)

        content = file.read()

        if len(content) > 5 * 1024 * 1024:
            flash('Ukuran file melebihi 5 MB.', 'error')
            return redirect(request.url)

        dashboard.html_content = content.decode('utf-8', errors='replace')
        dashboard.file_size = len(content)
        dashboard.uploaded_by = current_user.id
        dashboard.uploaded_at = datetime.now(timezone.utc)
        db.session.commit()

        flash(f'Dashboard "{dashboard.name}" berhasil diupdate!', 'success')
        return redirect(url_for('admin.panel'))

    return render_template('admin/upload.html', dashboard=dashboard)


@admin_bp.route('/dashboard/new', methods=['GET', 'POST'])
@admin_required
def new_dashboard():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        slug = request.form.get('slug', '').strip().lower()
        description = request.form.get('description', '').strip()
        icon = request.form.get('icon', '📊').strip()
        sort_order = request.form.get('sort_order', 0, type=int)

        if not name or not slug:
            flash('Nama dan slug wajib diisi.', 'error')
            return redirect(request.url)

        if Dashboard.query.filter_by(slug=slug).first():
            flash(f'Slug "{slug}" sudah digunakan.', 'error')
            return redirect(request.url)

        dashboard = Dashboard(
            name=name, slug=slug, description=description,
            icon=icon, sort_order=sort_order
        )
        db.session.add(dashboard)
        db.session.commit()

        flash(f'Dashboard "{name}" berhasil ditambahkan!', 'success')
        return redirect(url_for('admin.panel'))

    return render_template('admin/new_dashboard.html')


@admin_bp.route('/dashboard/<int:id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_dashboard(id):
    dashboard = db.session.get(Dashboard, id) or abort(404)

    if request.method == 'POST':
        dashboard.name = request.form.get('name', dashboard.name).strip()
        dashboard.description = request.form.get('description', '').strip()
        dashboard.icon = request.form.get('icon', '📊').strip()
        dashboard.sort_order = request.form.get('sort_order', 0, type=int)
        is_active = request.form.get('is_active') == 'on'
        dashboard.is_active = is_active
        db.session.commit()

        flash(f'Dashboard "{dashboard.name}" berhasil diupdate!', 'success')
        return redirect(url_for('admin.panel'))

    return render_template('admin/edit_dashboard.html', dashboard=dashboard)


@admin_bp.route('/dashboard/<int:id>/delete', methods=['POST'])
@admin_required
def delete_dashboard(id):
    dashboard = db.session.get(Dashboard, id) or abort(404)
    name = dashboard.name
    db.session.delete(dashboard)
    db.session.commit()
    flash(f'Dashboard "{name}" berhasil dihapus.', 'success')
    return redirect(url_for('admin.panel'))


@admin_bp.route('/users')
@admin_required
def users():
    all_users = User.query.order_by(User.created_at).all()
    return render_template('admin/users.html', users=all_users)


@admin_bp.route('/users/new', methods=['GET', 'POST'])
@admin_required
def new_user():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        display_name = request.form.get('display_name', '').strip()
        password = request.form.get('password', '')
        role = request.form.get('role', 'viewer')

        if not username or not password:
            flash('Username dan password wajib diisi.', 'error')
            return redirect(request.url)

        if User.query.filter_by(username=username).first():
            flash(f'Username "{username}" sudah digunakan.', 'error')
            return redirect(request.url)

        user = User(
            username=username,
            display_name=display_name or username,
            role=role if role in ('admin', 'viewer') else 'viewer',
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash(f'User "{username}" berhasil ditambahkan!', 'success')
        return redirect(url_for('admin.users'))

    return render_template('admin/new_user.html')


@admin_bp.route('/users/<int:id>/toggle', methods=['POST'])
@admin_required
def toggle_user(id):
    user = db.session.get(User, id) or abort(404)
    if user.id == current_user.id:
        flash('Tidak bisa menonaktifkan diri sendiri.', 'error')
        return redirect(url_for('admin.users'))

    user.is_active_user = not user.is_active_user
    db.session.commit()
    status = 'diaktifkan' if user.is_active_user else 'dinonaktifkan'
    flash(f'User "{user.username}" berhasil {status}.', 'success')
    return redirect(url_for('admin.users'))


@admin_bp.route('/users/<int:id>/reset-password', methods=['POST'])
@admin_required
def reset_password(id):
    user = db.session.get(User, id) or abort(404)
    new_password = request.form.get('new_password', '').strip()
    if not new_password:
        flash('Password baru wajib diisi.', 'error')
        return redirect(url_for('admin.users'))

    user.set_password(new_password)
    db.session.commit()
    flash(f'Password user "{user.username}" berhasil direset.', 'success')
    return redirect(url_for('admin.users'))

from flask import Blueprint, render_template, Response, abort
from flask_login import login_required
from models.dashboard import Dashboard

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
@login_required
def hub():
    dashboards = Dashboard.query.filter_by(is_active=True).order_by(Dashboard.sort_order).all()
    return render_template('hub.html', dashboards=dashboards)


@main_bp.route('/dashboard/<slug>')
@login_required
def view(slug):
    dashboard = Dashboard.query.filter_by(slug=slug, is_active=True).first_or_404()
    dashboards = Dashboard.query.filter_by(is_active=True).order_by(Dashboard.sort_order).all()
    return render_template('view.html', dashboard=dashboard, dashboards=dashboards)


@main_bp.route('/dashboard/<slug>/raw')
@login_required
def raw(slug):
    """Serve the stored HTML content directly (for iframe embedding)."""
    dashboard = Dashboard.query.filter_by(slug=slug, is_active=True).first_or_404()
    if not dashboard.has_content:
        abort(404)
    return Response(dashboard.html_content, mimetype='text/html')

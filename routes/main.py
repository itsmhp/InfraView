from flask import Blueprint, render_template, Response, abort
from flask_login import login_required, current_user
from models.dashboard import Dashboard
from utils.crypto import decrypt_content

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
@login_required
def hub():
    dashboards = Dashboard.query.filter_by(is_active=True).order_by(Dashboard.sort_order).all()

    # Compute KPI stats for hub summary
    total = len(dashboards)
    fresh = sum(1 for d in dashboards if d.freshness == 'fresh')
    stale = sum(1 for d in dashboards if d.freshness in ('stale', 'aging'))
    with_data = sum(1 for d in dashboards if d.has_content)

    # Find latest update across all dashboards
    latest = max((d.uploaded_at for d in dashboards if d.uploaded_at), default=None)

    return render_template('hub.html', dashboards=dashboards,
                           stats={'total': total, 'fresh': fresh, 'stale': stale,
                                  'with_data': with_data, 'latest': latest})


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
    return Response(decrypt_content(dashboard.html_content), mimetype='text/html')

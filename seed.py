"""Seed script: creates admin user + default dashboard slots."""
from app import create_app
from models import db
from models.user import User
from models.dashboard import Dashboard

DASHBOARDS = [
    {
        'name': 'CJE0 Budget Monitoring',
        'slug': 'cje0',
        'description': 'Real-time budget tracking dari SAP CJE0 — OPEX, CAPEX, Satelit',
        'icon': '💰',
        'sort_order': 1,
    },
    {
        'name': 'Laporan RKA IT',
        'slug': 'rka',
        'description': 'Laporan Realisasi Anggaran TI — bulanan & kumulatif',
        'icon': '📋',
        'sort_order': 2,
    },
    {
        'name': 'Status Pengadaan',
        'slug': 'pengadaan',
        'description': 'Analisis status pengadaan INF — pipeline & cross-tab',
        'icon': '📦',
        'sort_order': 3,
    },
    {
        'name': 'Tracking Pengadaan PLO',
        'slug': 'tracking-plo',
        'description': 'Dashboard tracking pengadaan PLO Group',
        'icon': '🚀',
        'sort_order': 4,
    },
]


def seed():
    app = create_app()
    with app.app_context():
        # Ensure schema is up-to-date (idempotent migrations)
        from sqlalchemy import text
        with db.engine.connect() as conn:
            conn.execute(text("""
                ALTER TABLE users
                ADD COLUMN IF NOT EXISTS last_login TIMESTAMP WITH TIME ZONE;
            """))
            conn.commit()
            print('[+] Column last_login ensured')

        # Create admin if not exists
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                display_name='Administrator',
                role='admin',
            )
            admin.set_password('admin123')
            db.session.add(admin)
            print('[+] Admin user created (admin / admin123)')
        else:
            print('[=] Admin user already exists')

        # Create viewer if not exists
        viewer = User.query.filter_by(username='viewer').first()
        if not viewer:
            viewer = User(
                username='viewer',
                display_name='Viewer',
                role='viewer',
            )
            viewer.set_password('viewer123')
            db.session.add(viewer)
            print('[+] Viewer user created (viewer / viewer123)')
        else:
            print('[=] Viewer user already exists')

        # Migrate old slug kirim5 -> tracking-plo
        old_kirim5 = Dashboard.query.filter_by(slug='kirim5').first()
        if old_kirim5:
            old_kirim5.slug = 'tracking-plo'
            db.session.commit()
            print('[~] Renamed slug kirim5 -> tracking-plo')

        # Create or update dashboard slots
        for d in DASHBOARDS:
            existing = Dashboard.query.filter_by(slug=d['slug']).first()
            if not existing:
                dashboard = Dashboard(**d)
                db.session.add(dashboard)
                print(f'[+] Dashboard "{d["name"]}" created')
            else:
                existing.name = d['name']
                existing.description = d['description']
                existing.icon = d['icon']
                existing.sort_order = d['sort_order']
                print(f'[~] Dashboard "{d["name"]}" updated')

        db.session.commit()
        print('\nSeed complete!')


if __name__ == '__main__':
    seed()

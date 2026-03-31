"""One-time migration: encrypt existing plain-text dashboard content."""
from app import create_app
from models import db
from models.dashboard import Dashboard
from utils.crypto import encrypt_content, PREFIX


def migrate():
    app = create_app()
    with app.app_context():
        dashboards = Dashboard.query.filter(Dashboard.html_content.isnot(None)).all()
        count = 0
        for d in dashboards:
            if d.html_content and not d.html_content.startswith(PREFIX):
                d.html_content = encrypt_content(d.html_content)
                count += 1
                print(f'[+] Encrypted: {d.name} ({d.slug})')
            else:
                print(f'[=] Already encrypted or empty: {d.name} ({d.slug})')
        db.session.commit()
        print(f'\nDone! Encrypted {count} dashboard(s).')


if __name__ == '__main__':
    migrate()

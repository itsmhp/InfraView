from flask import Flask, render_template
from flask_login import LoginManager
from config import Config
from models import db
from models.user import User


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Init extensions
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Silakan login terlebih dahulu.'
    login_manager.login_message_category = 'info'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    # Context processor: sidebar dashboards available in all templates
    @app.context_processor
    def inject_sidebar():
        from models.dashboard import Dashboard

        def get_sidebar_dashboards():
            return Dashboard.query.filter_by(is_active=True).order_by(Dashboard.sort_order).all()

        return dict(get_sidebar_dashboards=get_sidebar_dashboards)

    # Register blueprints
    from routes.auth import auth_bp
    from routes.main import main_bp
    from routes.admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)

    # Error handlers
    @app.errorhandler(404)
    def not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('errors/403.html'), 403

    # Create tables + seed
    with app.app_context():
        db.create_all()
        # Idempotent migration: add columns that db.create_all() won't add to existing tables
        from sqlalchemy import text
        with db.engine.connect() as conn:
            conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS last_login TIMESTAMP;"))
            conn.commit()
        # Seed default users if not exist
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', display_name='Administrator', role='admin')
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()

    return app


# Module-level app for gunicorn: `gunicorn app:app`
app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)

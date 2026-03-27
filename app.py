from flask import Flask
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

    # Create tables
    with app.app_context():
        db.create_all()

    return app


# Module-level app for gunicorn: `gunicorn app:app`
app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)

from datetime import datetime
import os
from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Global extensions (initialized in create_app)
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"


def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DATABASE_URL", f"sqlite:///{os.path.join(os.path.dirname(__file__), 'erp.db')}"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Init extensions
    db.init_app(app)
    login_manager.init_app(app)

    # Import models to register with SQLAlchemy
    from . import models  # noqa: F401

    # Register blueprints
    from .blueprints.auth.routes import auth_bp
    from .blueprints.dashboard.routes import dashboard_bp
    from .blueprints.finance.routes import finance_bp
    from .blueprints.hr.routes import hr_bp
    from .blueprints.marketing.routes import marketing_bp
    from .blueprints.inventory.routes import inventory_bp
    from .blueprints.admin.routes import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(finance_bp)
    app.register_blueprint(hr_bp)
    app.register_blueprint(marketing_bp)
    app.register_blueprint(inventory_bp)
    app.register_blueprint(admin_bp)

    @app.route("/")
    def index():
        return redirect(url_for("dashboard.index"))

    # Create DB and seed data
    with app.app_context():
        db.create_all()
        from .seed import seed_demo_data
        seed_demo_data()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

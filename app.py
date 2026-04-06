import os
from datetime import timedelta
from flask import Flask, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from werkzeug.middleware.proxy_fix import ProxyFix
from config import Config

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    # =========================
    # ⚙️ CONFIGURATION GLOBALE
    # =========================
    app.config.from_object(Config)

    # 🔐 SECRET KEY
    app.secret_key = os.getenv(
        "SECRET_KEY",
        "smart_commune_malicounda_2026_ultra_secure"
    )

    # 🍪 SESSION / COOKIES
    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
    app.config["SESSION_COOKIE_SECURE"] = (
        os.getenv("FLASK_ENV") == "production"
    )
    app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=12)

    # 🧠 DEBUG / TEMPLATES
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0

    # 🌍 PROXY RENDER / HTTPS
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

    # 🗄️ DATABASE
    db.init_app(app)

    # =========================
    # 📦 IMPORT BLUEPRINTS
    # =========================
    from routes.landing_routes import landing_bp
    from routes.dashboard_routes import dashboard_bp
    from routes.land_routes import land_bp
    from routes.finance_routes import finance_bp
    from routes.project_routes import project_bp
    from routes.incident_routes import incident_bp
    from routes.auth_routes import auth_bp
    from routes.report_routes import report_bp
    from routes.qr_routes import qr_bp
    from routes.pitch_routes import pitch_bp
    from routes.stats_routes import stats_bp

    blueprints = [
        landing_bp,
        dashboard_bp,
        land_bp,
        finance_bp,
        project_bp,
        incident_bp,
        auth_bp,
        report_bp,
        qr_bp,
        pitch_bp,
        stats_bp
    ]

    for bp in blueprints:
        app.register_blueprint(bp)

    # =========================
    # 🏠 HOME REDIRECT INTELLIGENT
    # =========================
    @app.route("/")
    def home():
        return redirect(url_for("landing.landing"))

    # =========================
    # ❤️ HEALTHCHECK
    # =========================
    @app.route("/health")
    def health():
        return {
            "status": "ok",
            "app": "Smart Commune Cockpit",
            "environment": os.getenv("FLASK_ENV", "development")
        }

    # =========================
    # 🚫 ERROR HANDLERS
    # =========================
    @app.errorhandler(404)
    def not_found(error):
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def server_error(error):
        return render_template("500.html"), 500

    return app


# =========================
# ▶️ RUN LOCAL
# =========================
if __name__ == "__main__":
    app = create_app()
    app.run(
        debug=True,
        host="0.0.0.0",
        port=int(os.getenv("PORT", 5000))
    )
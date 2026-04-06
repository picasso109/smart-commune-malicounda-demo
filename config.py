import os


class Config:
    # =========================
    # 🔐 SÉCURITÉ
    # =========================
    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "smart_commune_malicounda_secure_2026"
    )

    # =========================
    # 🗄️ BASE DE DONNÉES
    # =========================
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "sqlite:///smart_commune.db"
    )

    # 🌍 Compatibilité PostgreSQL Render
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace(
            "postgres://",
            "postgresql://",
            1
        )

    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # =========================
    # 📦 TEMPLATES & CACHE
    # =========================
    TEMPLATES_AUTO_RELOAD = True
    SEND_FILE_MAX_AGE_DEFAULT = 0

    # =========================
    # 🍪 COOKIES
    # =========================
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = (
        os.getenv("FLASK_ENV", "development") == "production"
    )

    # =========================
    # ⚙️ DEBUG
    # =========================
    DEBUG = os.getenv(
        "FLASK_ENV",
        "development"
    ) != "production"
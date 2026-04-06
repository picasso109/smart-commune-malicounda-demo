from flask import Blueprint, render_template, jsonify
from datetime import datetime

stats_bp = Blueprint(
    "stats",
    __name__,
    url_prefix="/stats"
)

# =========================
# 🕒 UTILITAIRE DATE
# =========================
def maintenant():
    return datetime.now().strftime("%d/%m/%Y %H:%M")


# =========================
# 📊 DONNÉES ANALYTICS
# =========================
ANALYTICS = {
    "croissance_recettes": "+32%",
    "litiges_resolus": "87%",
    "projets_livres": 5,
    "roi": "900%",
    "agents_connectes": 12,
    "temps_resolution": "-45%"
}


# =========================
# 📈 DASHBOARD ANALYTICS
# =========================
@stats_bp.route("/")
def analytics_dashboard():
    return render_template(
        "stats.html",
        analytics=ANALYTICS,
        updated_at=maintenant()
    )


# =========================
# 📊 API LIVE ANALYTICS
# =========================
@stats_bp.route("/api/live")
def analytics_api():
    return jsonify({
        "status": "success",
        "updated_at": maintenant(),
        "analytics": ANALYTICS
    })


# =========================
# 📦 EXPORT POLICY BRIEF
# =========================
@stats_bp.route("/export")
def export_policy_brief():
    return jsonify({
        "status": "success",
        "module": "analytics",
        "message": "Brief analytique généré avec succès",
        "generated_at": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "data": ANALYTICS
    })
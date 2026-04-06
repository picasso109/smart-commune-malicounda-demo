from flask import Blueprint, render_template
from datetime import datetime

landing_bp = Blueprint(
    "landing",
    __name__
)

# =========================
# 🕒 UTILITAIRE DATE
# =========================
def maintenant():
    return datetime.now().strftime("%d/%m/%Y %H:%M")


# =========================
# 🌍 PORTAIL PUBLIC
# =========================
@landing_bp.route("/accueil")
def landing():
    metrics = {
        "roi": "900%",
        "gain": "100 000 000 FCFA",
        "litiges": "-70%",
        "recettes": "+25%",
        "satisfaction": "96%"
    }

    return render_template(
        "landing.html",
        metrics=metrics,
        updated_at=maintenant(),
        commune="Malicounda"
    )
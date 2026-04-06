from flask import Blueprint, render_template, jsonify, abort
from datetime import datetime

finance_bp = Blueprint(
    "finance",
    __name__,
    template_folder="../templates",
    url_prefix="/finances"
)

# =========================
# 🕒 UTILITAIRE DATE
# =========================
def maintenant():
    return datetime.now().strftime("%d/%m/%Y %H:%M")


# =========================
# 💰 DONNÉES FINANCIÈRES
# =========================
FINANCE_DATA = {
    "taxes_foncieres": "45 000 000 FCFA",
    "marches": "12 000 000 FCFA",
    "tourisme": "18 000 000 FCFA",
    "projection": "+25%",
    "updated_at": maintenant()
}

REVENUE_STREAMS = [
    {
        "id": 1,
        "module": "Taxes foncières",
        "zone": "Pointe Sarène",
        "montant": "45 000 000 FCFA",
        "compliance": "91%",
        "status": "stable"
    },
    {
        "id": 2,
        "module": "Marchés",
        "zone": "Malicounda Centre",
        "montant": "12 000 000 FCFA",
        "compliance": "88%",
        "status": "growth"
    },
    {
        "id": 3,
        "module": "Tourisme",
        "zone": "Zone côtière",
        "montant": "18 000 000 FCFA",
        "compliance": "94%",
        "status": "peak"
    }
]


# =========================
# 💎 PAGE FINANCE
# =========================
@finance_bp.route("/")
def finance():
    finances = {
        **FINANCE_DATA,
        "updated_at": maintenant()
    }

    return render_template(
        "finance.html",
        finances=finances,
        revenues=REVENUE_STREAMS
    )


# =========================
# 📄 DÉTAIL D’UNE LIGNE
# =========================
@finance_bp.route("/revenue/<int:revenue_id>")
def revenue_detail(revenue_id):
    revenue = next(
        (r for r in REVENUE_STREAMS if r["id"] == revenue_id),
        None
    )

    if not revenue:
        abort(404, description="Ligne de revenu introuvable")

    return render_template(
        "finance_detail.html",
        revenue=revenue,
        updated_at=maintenant()
    )


# =========================
# 📊 API TREND CHART
# =========================
@finance_bp.route("/api/trend")
def finance_trend():
    return jsonify({
        "updated_at": maintenant(),
        "labels": ["Jan", "Fév", "Mar", "Avr", "Mai", "Juin"],
        "values": [52, 58, 61, 66, 71, 75]
    })


# =========================
# 📦 EXPORT PACK FINANCE
# =========================
@finance_bp.route("/export")
def finance_export():
    return jsonify({
        "status": "success",
        "module": "finance",
        "message": "Pack trésorerie généré avec succès",
        "generated_at": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "revenues_count": len(REVENUE_STREAMS),
        "data": REVENUE_STREAMS
    })
from flask import Blueprint, render_template, jsonify, abort
from datetime import datetime

incident_bp = Blueprint(
    "incidents",
    __name__,
    url_prefix="/incidents"
)

# =========================
# 🕒 UTILITAIRE DATE
# =========================
def maintenant():
    return datetime.now().strftime("%d/%m/%Y %H:%M")


# =========================
# 🚨 DONNÉES INCIDENTS
# =========================
INCIDENTS = [
    {
        "id": 1,
        "titre": "Panne éclairage public",
        "zone": "Falokh",
        "priorite": "Haute",
        "statut": "En cours",
        "agent": "Brigade éclairage",
        "reported_at": "06/04/2026 08:10"
    },
    {
        "id": 2,
        "titre": "Dépôt sauvage",
        "zone": "Madinatou Salam",
        "priorite": "Moyenne",
        "statut": "Signalé",
        "agent": "Hygiène urbaine",
        "reported_at": "06/04/2026 09:20"
    },
    {
        "id": 3,
        "titre": "Route dégradée",
        "zone": "Pointe Sarène",
        "priorite": "Critique",
        "statut": "Urgent",
        "agent": "Voirie rapide",
        "reported_at": "06/04/2026 10:05"
    }
]


# =========================
# 🚨 PAGE INCIDENTS
# =========================
@incident_bp.route("/")
def incidents():
    return render_template(
        "incidents.html",
        incidents=INCIDENTS,
        updated_at=maintenant()
    )


# =========================
# 👁️ DÉTAIL INCIDENT
# =========================
@incident_bp.route("/<int:incident_id>")
def incident_detail(incident_id):
    incident = next(
        (i for i in INCIDENTS if i["id"] == incident_id),
        None
    )

    if not incident:
        abort(404, description="Incident introuvable")

    return render_template(
        "incident_detail.html",
        incident=incident,
        updated_at=maintenant()
    )


# =========================
# 📊 API INCIDENTS LIVE
# =========================
@incident_bp.route("/api/live")
def incidents_live():
    return jsonify({
        "updated_at": maintenant(),
        "total": len(INCIDENTS),
        "incidents": INCIDENTS
    })


# =========================
# 📦 EXPORT BRIEF DE CRISE
# =========================
@incident_bp.route("/export")
def export_incidents():
    return jsonify({
        "status": "success",
        "module": "incidents",
        "message": "Brief de crise exporté avec succès",
        "generated_at": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "incidents_count": len(INCIDENTS),
        "data": INCIDENTS
    })
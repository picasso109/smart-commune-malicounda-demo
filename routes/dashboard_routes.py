from flask import Blueprint, render_template, jsonify, abort
from datetime import datetime
from routes.auth_routes import login_required

dashboard_bp = Blueprint(
    "dashboard",
    __name__,
    url_prefix="/dashboard"
)

# =========================
# 📦 DONNÉES DÉMO CENTRALISÉES
# =========================
DASHBOARD_STATS = {
    "recettes": "87 500 000 FCFA",
    "projection": "+24%",
    "parcelles": 342,
    "litiges": 12,
    "projets": 7,
    "etat_civil": 1250
}

INCIDENTS = [
    {
        "id": 1,
        "zone": "Pointe Sarène",
        "niveau": "critique",
        "message": "Litige foncier sur zone touristique",
        "date": "06/04/2026",
        "agent": "Service Foncier"
    },
    {
        "id": 2,
        "zone": "Malicounda Gare",
        "niveau": "moyen",
        "message": "Retard chantier voirie",
        "date": "06/04/2026",
        "agent": "Direction Technique"
    },
    {
        "id": 3,
        "zone": "Falokh",
        "niveau": "faible",
        "message": "Zone stable et sécurisée",
        "date": "06/04/2026",
        "agent": "Police Municipale"
    }
]

PROJECTS = [
    {
        "id": 1,
        "nom": "Centre de santé",
        "progress": 78,
        "budget": "145 000 000 FCFA",
        "entreprise": "SEN BATIMENT"
    },
    {
        "id": 2,
        "nom": "Éclairage public",
        "progress": 55,
        "budget": "82 000 000 FCFA",
        "entreprise": "SENELEC PARTNER"
    },
    {
        "id": 3,
        "nom": "Voirie Malicounda Gare",
        "progress": 32,
        "budget": "210 000 000 FCFA",
        "entreprise": "TERANGA BTP"
    }
]


# =========================
# 🕒 UTILITAIRE DATE
# =========================
def maintenant():
    return datetime.now().strftime("%d/%m/%Y %H:%M")


# =========================
# 🏛️ PAGE COCKPIT MAIRE
# =========================
@dashboard_bp.route("/")
@login_required
def dashboard():
    stats = {
        **DASHBOARD_STATS,
        "updated_at": maintenant()
    }

    return render_template(
        "dashboard_mayor.html",
        stats=stats,
        incidents=INCIDENTS[:3],
        projects=PROJECTS[:3]
    )


# =========================
# 📊 PAGE DÉTAIL KPI
# =========================
@dashboard_bp.route("/kpis")
@login_required
def dashboard_kpis_page():
    return render_template(
        "dashboard_kpis.html",
        stats=DASHBOARD_STATS,
        updated_at=maintenant()
    )


# =========================
# 📊 API KPI LIVE
# =========================
@dashboard_bp.route("/api/kpis")
@login_required
def dashboard_kpis():
    return jsonify({
        **DASHBOARD_STATS,
        "recettes_value": 87500000,
        "projection_value": 24,
        "updated_at": maintenant()
    })


# =========================
# 🚨 PAGE INCIDENTS
# =========================
@dashboard_bp.route("/incidents")
@login_required
def incidents_page():
    return render_template(
        "dashboard_incidents.html",
        incidents=INCIDENTS,
        updated_at=maintenant()
    )


# =========================
# 🚨 DÉTAIL INCIDENT
# =========================
@dashboard_bp.route("/incidents/<int:incident_id>")
@login_required
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
# 🚨 API ALERTES LIVE
# =========================
@dashboard_bp.route("/api/incidents-live")
@login_required
def incidents_live():
    return jsonify({
        "updated_at": maintenant(),
        "total": len(INCIDENTS),
        "incidents": INCIDENTS
    })


# =========================
# 🏗️ PAGE PROJETS
# =========================
@dashboard_bp.route("/projects")
@login_required
def projects_page():
    return render_template(
        "dashboard_projects.html",
        projects=PROJECTS,
        updated_at=maintenant()
    )


# =========================
# 🏗️ DÉTAIL PROJET
# =========================
@dashboard_bp.route("/projects/<int:project_id>")
@login_required
def project_detail(project_id):
    project = next(
        (p for p in PROJECTS if p["id"] == project_id),
        None
    )

    if not project:
        abort(404, description="Projet introuvable")

    return render_template(
        "project_detail.html",
        project=project,
        updated_at=maintenant()
    )


# =========================
# 🏗️ API PROJETS LIVE
# =========================
@dashboard_bp.route("/api/projects-progress")
@login_required
def projects_progress():
    return jsonify({
        "updated_at": maintenant(),
        "total": len(PROJECTS),
        "projects": PROJECTS
    })
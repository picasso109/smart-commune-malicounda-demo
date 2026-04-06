from flask import Blueprint, render_template, jsonify, abort
from datetime import datetime

project_bp = Blueprint(
    "projects",
    __name__,
    url_prefix="/projets"
)

# =========================
# 🕒 UTILITAIRE DATE
# =========================
def maintenant():
    return datetime.now().strftime("%d/%m/%Y %H:%M")


# =========================
# 🏗️ DONNÉES PROJETS
# =========================
PROJECTS = [
    {
        "id": 1,
        "nom": "Route Falokh",
        "budget": "250 000 000 FCFA",
        "avancement": 75,
        "progress": 75,  # compat dashboard
        "statut": "En cours",
        "entreprise": "TERANGA BTP",
        "zone": "Falokh",
        "deadline": "Juin 2026"
    },
    {
        "id": 2,
        "nom": "Éclairage Pointe Sarène",
        "budget": "95 000 000 FCFA",
        "avancement": 40,
        "progress": 40,
        "statut": "Retard",
        "entreprise": "SENELEC PARTNER",
        "zone": "Pointe Sarène",
        "deadline": "Août 2026"
    },
    {
        "id": 3,
        "nom": "Marché Madinatou Salam",
        "budget": "180 000 000 FCFA",
        "avancement": 90,
        "progress": 90,
        "statut": "Presque terminé",
        "entreprise": "BAOBAB CONSTRUCTION",
        "zone": "Madinatou Salam",
        "deadline": "Mai 2026"
    }
]


# =========================
# 🏗️ PAGE PROJETS
# =========================
@project_bp.route("/")
def projects():
    return render_template(
        "projects.html",
        projects=PROJECTS,
        updated_at=maintenant()
    )


# =========================
# 👁️ DÉTAIL PROJET
# =========================
@project_bp.route("/<int:project_id>")
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
# 📊 API AVANCEMENT
# =========================
@project_bp.route("/api/progress")
def project_progress():
    return jsonify({
        "updated_at": maintenant(),
        "total": len(PROJECTS),
        "projects": PROJECTS
    })


# =========================
# 📦 EXPORT PORTEFEUILLE
# =========================
@project_bp.route("/export")
def export_projects():
    return jsonify({
        "status": "success",
        "module": "projets",
        "message": "Portefeuille projets exporté avec succès",
        "generated_at": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "projects_count": len(PROJECTS),
        "data": PROJECTS
    })
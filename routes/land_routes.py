from flask import Blueprint, render_template, jsonify, abort
from datetime import datetime

# ✅ garder le même nom pour compatibilité app.py
land_bp = Blueprint(
    "foncier",
    __name__,
    template_folder="../templates",
    url_prefix="/foncier"
)

# =========================
# 🕒 UTILITAIRE DATE
# =========================
def maintenant():
    return datetime.now().strftime("%d/%m/%Y %H:%M")


# =========================
# 🗺️ BASE CADASTRALE MALICOUNDA
# =========================
PARCELLES = [
    {
        "id": "P-001",
        "zone": "Falokh",
        "statut": "Sécurisée",
        "superficie": 600,
        "proprietaire": "Commune de Malicounda",
        "valeur": 18000000,
        "historique": "Réserve communale sécurisée en 2024",
        "latitude": 14.47189,
        "longitude": -16.94645,
        "limites": [
            [14.47199, -16.94655],
            [14.47199, -16.94635],
            [14.47179, -16.94635],
            [14.47179, -16.94655]
        ]
    },
    {
        "id": "P-002",
        "zone": "Pointe Sarène",
        "statut": "Litige",
        "superficie": 1200,
        "proprietaire": "Litige en cours",
        "valeur": 95000000,
        "historique": "Litige entre héritiers - dossier 2025",
        "latitude": 14.28638,
        "longitude": -16.91611,
        "limites": [
            [14.28650, -16.91625],
            [14.28650, -16.91595],
            [14.28620, -16.91595],
            [14.28620, -16.91625]
        ]
    },
    {
        "id": "P-003",
        "zone": "Madinatou Salam",
        "statut": "Disponible",
        "superficie": 450,
        "proprietaire": "Réserve foncière",
        "valeur": 11000000,
        "historique": "Lotissement 2026 - prêt à attribution",
        "latitude": 14.35020,
        "longitude": -16.94210,
        "limites": [
            [14.35030, -16.94220],
            [14.35030, -16.94200],
            [14.35010, -16.94200],
            [14.35010, -16.94220]
        ]
    }
]


# =========================
# 🔄 NORMALISATION TEMPLATE
# =========================
def normaliser_parcelle(parcelle):
    """Compatibilité FR + anciens templates EN."""
    return {
        **parcelle,
        "status": parcelle["statut"],
        "area": parcelle["superficie"],
        "owner": parcelle["proprietaire"],
        "value": parcelle["valeur"],
        "history": parcelle["historique"],
        "lat": parcelle["latitude"],
        "lng": parcelle["longitude"],
        "boundary": parcelle["limites"],
        # compat rétro
        "plot": parcelle
    }


# =========================
# 🏠 MODULE FONCIER
# =========================
@land_bp.route("/")
def accueil_foncier():
    parcelles_normalisees = [normaliser_parcelle(p) for p in PARCELLES]

    return render_template(
        "land.html",
        parcelles=parcelles_normalisees,
        plots=parcelles_normalisees,  # compat ancien template
        mis_a_jour=maintenant(),
        updated_at=maintenant()
    )


# =========================
# 👁️ DÉTAIL PARCELLE
# =========================
@land_bp.route("/parcelle/<identifiant>")
def detail_parcelle(identifiant):
    parcelle = next(
        (p for p in PARCELLES if p["id"] == identifiant),
        None
    )

    if not parcelle:
        abort(404, description="Parcelle introuvable dans la commune de Malicounda")

    parcelle_normalisee = normaliser_parcelle(parcelle)

    return render_template(
        "plot_detail.html",
        parcelle=parcelle_normalisee,
        plot=parcelle_normalisee,  # compat ancien template
        updated_at=maintenant()
    )


# =========================
# 📊 API REGISTRE FONCIER
# =========================
@land_bp.route("/api/registre")
def api_registre_foncier():
    parcelles_normalisees = [normaliser_parcelle(p) for p in PARCELLES]

    return jsonify({
        "statut": "succès",
        "commune": "Malicounda",
        "total": len(PARCELLES),
        "mis_a_jour": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "parcelles": parcelles_normalisees
    })


# =========================
# 📦 EXPORT CADASTRE
# =========================
@land_bp.route("/export")
def exporter_cadastre():
    parcelles_normalisees = [normaliser_parcelle(p) for p in PARCELLES]

    return jsonify({
        "statut": "succès",
        "commune": "Malicounda",
        "nombre_parcelles": len(PARCELLES),
        "message": "Export du dossier cadastral effectué avec succès",
        "genere_le": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "donnees": parcelles_normalisees
    })
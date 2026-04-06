from flask import Blueprint, send_file, request, jsonify, render_template, abort
import qrcode
from pathlib import Path
from datetime import datetime

qr_bp = Blueprint(
    "qr",
    __name__,
    url_prefix="/qr"
)

# =========================
# 🕒 UTILITAIRE DATE
# =========================
def maintenant():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")


# =========================
# 📦 REGISTRE QR DÉMO
# =========================
QR_REGISTRY = {
    "P-001": {
        "type": "Parcelle",
        "zone": "Falokh",
        "status": "Sécurisée",
        "owner": "Commune de Malicounda"
    },
    "P-002": {
        "type": "Parcelle",
        "zone": "Pointe Sarène",
        "status": "Litige",
        "owner": "Dossier en contentieux"
    },
    "R-001": {
        "type": "Quittance",
        "zone": "Marché Central",
        "status": "Payée",
        "owner": "Régie financière"
    }
}


# =========================
# 🔳 GÉNÉRATION QR IMAGE
# =========================
@qr_bp.route("/<module>/<doc_id>")
def generate_qr(module, doc_id):
    output_dir = Path("static/img/qr")
    output_dir.mkdir(parents=True, exist_ok=True)

    file_path = output_dir / f"qr_{module}_{doc_id}.png"

    base_url = request.host_url.rstrip("/")
    target_url = f"{base_url}/qr/verify/{module}/{doc_id}"

    if not file_path.exists():
        qr = qrcode.QRCode(
            version=4,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4
        )

        qr.add_data(target_url)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        img.save(file_path)

    return send_file(file_path, mimetype="image/png")


# =========================
# 👁️ PAGE VÉRIFICATION
# =========================
@qr_bp.route("/verify/<module>/<doc_id>")
def verify_document(module, doc_id):
    data = QR_REGISTRY.get(doc_id)

    if not data:
        abort(404, description="Document QR introuvable")

    return render_template(
        "qr_verify.html",
        doc_id=doc_id,
        module=module,
        data=data,
        verified_at=maintenant()
    )


# =========================
# 📊 API VÉRIFICATION
# =========================
@qr_bp.route("/api/verify/<doc_id>")
def verify_api(doc_id):
    data = QR_REGISTRY.get(doc_id)

    if not data:
        return jsonify({
            "status": "error",
            "message": "Document introuvable",
            "verified_at": maintenant()
        }), 404

    return jsonify({
        "status": "verified",
        "doc_id": doc_id,
        "data": data,
        "verified_at": maintenant()
    })
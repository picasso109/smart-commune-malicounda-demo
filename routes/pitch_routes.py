from flask import Blueprint, send_file
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from datetime import datetime
import os

pitch_bp = Blueprint(
    "pitch",
    __name__,
    url_prefix="/pitch"
)


# =========================
# 📄 GÉNÉRATION DEVIS PDF
# =========================
@pitch_bp.route("/devis")
def pitch_devis():
    dossier_temp = "generated"
    os.makedirs(dossier_temp, exist_ok=True)

    file_path = os.path.join(
        dossier_temp,
        "devis_smart_commune_malicounda.pdf"
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "Title",
        parent=styles["Title"],
        fontSize=20,
        leading=24,
        alignment=TA_CENTER
    )

    normal_style = ParagraphStyle(
        "NormalCustom",
        parent=styles["Normal"],
        fontSize=11,
        leading=20,
        alignment=TA_LEFT
    )

    doc = SimpleDocTemplate(
        file_path,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm
    )

    story = []

    # 🏛️ titre
    story.append(Paragraph(
        "OFFRE OFFICIELLE – SMART COMMUNE COCKPIT<br/>Commune de Malicounda",
        title_style
    ))
    story.append(Spacer(1, 1 * cm))

    # 📋 introduction
    story.append(Paragraph(
        "Plateforme intelligente de gouvernance territoriale pour le pilotage "
        "des finances, du foncier, des projets, des incidents et du reporting exécutif.",
        normal_style
    ))
    story.append(Spacer(1, 0.8 * cm))

    # 📦 modules
    story.append(Paragraph("<b>Modules inclus</b>", normal_style))

    modules = [
        "Gestion foncière avec QR code",
        "Finances communales",
        "Suivi des projets",
        "Centre incidents citoyens",
        "Reporting PDF exécutif",
        "Application PWA terrain",
        "Accès sécurisé Maire et agents"
    ]

    for module in modules:
        story.append(Paragraph(f"• {module}", normal_style))

    story.append(Spacer(1, 0.8 * cm))

    # 💵 tableau devis
    data = [
        ["Élément", "Valeur"],
        ["Budget pilote", "5 000 000 FCFA"],
        ["ROI estimé", "900%"],
        ["Durée de déploiement", "30 jours"],
        ["Formation agents", "Incluse"],
        ["Support", "90 jours"],
        ["Maintenance évolutive", "Optionnelle"],
        ["Date génération", datetime.now().strftime("%d/%m/%Y")]
    ]

    table = Table(data, colWidths=[7 * cm, 7 * cm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0d6efd")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1),
         [colors.whitesmoke, colors.lightgrey]),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8)
    ]))

    story.append(table)
    story.append(Spacer(1, 1 * cm))

    # 🚀 conclusion
    story.append(Paragraph(
        "<b>Recommandation :</b> déploiement pilote immédiat sur Malicounda "
        "avant extension aux autres communes du Sénégal.",
        normal_style
    ))

    doc.build(story)

    return send_file(
        file_path,
        as_attachment=True,
        download_name="devis_smart_commune_malicounda.pdf"
    )
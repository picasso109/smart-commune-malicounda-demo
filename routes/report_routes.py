from flask import Blueprint, send_file, jsonify
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from pathlib import Path
from datetime import datetime

report_bp = Blueprint(
    "reports",
    __name__,
    url_prefix="/rapports"
)


# =========================
# 🕒 UTILITAIRE DATE
# =========================
def maintenant():
    return datetime.now().strftime("%d/%m/%Y à %H:%M")


# =========================
# 📄 CONSTRUCTEUR PDF
# =========================
def build_executive_pdf(file_path, title, kpis, recommendations):
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "Title",
        parent=styles["Title"],
        fontSize=20,
        leading=24,
        alignment=TA_CENTER
    )

    text_style = ParagraphStyle(
        "Text",
        parent=styles["Normal"],
        fontSize=11,
        leading=20,
        alignment=TA_LEFT
    )

    doc = SimpleDocTemplate(
        str(file_path),
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm
    )

    story = []

    # 🏛️ couverture
    story.append(Paragraph(title, title_style))
    story.append(Spacer(1, 0.6 * cm))

    story.append(Paragraph(
        f"Rapport généré le {maintenant()}",
        text_style
    ))
    story.append(Spacer(1, 1 * cm))

    # 📊 tableau KPI
    table_data = [["Indicateur", "Valeur"]] + kpis

    table = Table(table_data, colWidths=[8 * cm, 6 * cm])
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

    # 🧠 recommandations
    story.append(Paragraph("<b>Recommandations stratégiques</b>", text_style))
    story.append(Spacer(1, 0.4 * cm))

    for item in recommendations:
        story.append(Paragraph(f"• {item}", text_style))

    story.append(PageBreak())

    # 🚀 vision
    story.append(Paragraph(
        "<b>Vision d’extension régionale</b><br/>"
        "Le cockpit Smart Commune peut être étendu aux communes voisines "
        "pour créer une gouvernance territoriale intercommunale.",
        text_style
    ))

    doc.build(story)


# =========================
# 📄 RAPPORT MAIRE
# =========================
@report_bp.route("/maire")
def mayor_report():
    reports_dir = Path("static/reports")
    reports_dir.mkdir(parents=True, exist_ok=True)

    file_path = reports_dir / "rapport_maire_malicounda.pdf"

    kpis = [
        ["💵 Recettes communales", "87 500 000 FCFA"],
        ["🗺️ Parcelles sécurisées", "342"],
        ["🏗️ Projets actifs", "7"],
        ["🚨 Incidents critiques", "3"],
        ["📈 Projection annuelle", "+24%"],
        ["👥 Plaintes résolues", "92%"]
    ]

    recommendations = [
        "Poursuivre la digitalisation foncière",
        "Étendre le QR sécurisé aux quittances",
        "Renforcer le suivi BTP par géolocalisation",
        "Préparer l’extension aux communes voisines"
    ]

    build_executive_pdf(
        file_path=file_path,
        title="RAPPORT EXÉCUTIF DU MAIRE<br/>Smart Commune – Malicounda",
        kpis=kpis,
        recommendations=recommendations
    )

    return send_file(
        file_path,
        as_attachment=True,
        download_name="rapport_maire_malicounda.pdf"
    )


# =========================
# 🌍 RAPPORT BAILLEUR
# =========================
@report_bp.route("/bailleur")
def donor_report():
    reports_dir = Path("static/reports")
    reports_dir.mkdir(parents=True, exist_ok=True)

    file_path = reports_dir / "rapport_bailleur_malicounda.pdf"

    kpis = [
        ["🌱 Impact ESG", "-18% CO₂"],
        ["💧 Continuité eau", "87%"],
        ["🏥 Projets santé", "4"],
        ["🛣️ Modernisation voirie", "32%"],
        ["📚 Couverture éducation", "91%"]
    ]

    recommendations = [
        "Étendre les infrastructures climato-résilientes",
        "Renforcer les API de reporting bailleurs",
        "Créer un hub régional de résilience intelligente"
    ]

    build_executive_pdf(
        file_path=file_path,
        title="RAPPORT EXÉCUTIF BAILLEUR<br/>Smart Commune – Malicounda",
        kpis=kpis,
        recommendations=recommendations
    )

    return send_file(
        file_path,
        as_attachment=True,
        download_name="rapport_bailleur_malicounda.pdf"
    )


# =========================
# 📊 API MÉTADONNÉES
# =========================
@report_bp.route("/api/meta")
def report_meta():
    return jsonify({
        "status": "ready",
        "reports": {
            "maire": "/rapports/maire",
            "bailleur": "/rapports/bailleur"
        },
        "generated_at": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    })
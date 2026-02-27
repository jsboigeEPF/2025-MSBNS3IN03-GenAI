"""
Service PDF — Génération de rapports PDF professionnels avec ReportLab
"""
import os
import re
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

from config import settings

# Palette de couleurs par type
PALETTES = {
    "financial": {"primary": colors.HexColor("#c8a96e"), "dark": colors.HexColor("#1a1200"), "light": colors.HexColor("#fdf8ee")},
    "technical": {"primary": colors.HexColor("#4af0c4"), "dark": colors.HexColor("#003322"), "light": colors.HexColor("#edfff8")},
    "medical":   {"primary": colors.HexColor("#e05c8a"), "dark": colors.HexColor("#1a0010"), "light": colors.HexColor("#fff0f5")},
    "generic":   {"primary": colors.HexColor("#5b8dee"), "dark": colors.HexColor("#001133"), "light": colors.HexColor("#f0f4ff")},
}


def markdown_to_rl(text: str, style) -> list:
    """Convertit un texte Markdown basique en éléments ReportLab."""
    flowables = []
    paragraphs = text.split("\n\n")

    for para in paragraphs:
        para = para.strip()
        if not para:
            continue

        # Titres ## 
        if para.startswith("## "):
            heading_style = ParagraphStyle(
                "Heading2RL", parent=style,
                fontSize=13, fontName="Helvetica-Bold",
                spaceAfter=6, spaceBefore=14, textColor=colors.HexColor("#333")
            )
            flowables.append(Paragraph(para[3:], heading_style))

        # Listes à puces
        elif para.startswith("- ") or para.startswith("• "):
            items = [line.lstrip("- •").strip() for line in para.split("\n") if line.strip()]
            bullet_style = ParagraphStyle(
                "Bullet", parent=style, fontSize=10,
                leftIndent=20, spaceAfter=3, leading=14
            )
            for item in items:
                item_clean = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", item)
                flowables.append(Paragraph(f"• {item_clean}", bullet_style))
            flowables.append(Spacer(1, 4))

        # Paragraphes normaux
        else:
            # Conversion **gras**
            para_clean = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", para)
            # Conversion *italique*
            para_clean = re.sub(r"\*(.+?)\*", r"<i>\1</i>", para_clean)
            flowables.append(Paragraph(para_clean, style))
            flowables.append(Spacer(1, 8))

    return flowables


def generate_pdf(
    report_name: str,
    report_type: str,
    narrative: str,
    data: dict,
    kpis: list[dict],
    output_path: str,
) -> str:
    """Génère un PDF complet du rapport."""

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    palette = PALETTES.get(report_type, PALETTES["generic"])

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
    )

    styles = getSampleStyleSheet()
    story = []

    # ── Styles personnalisés ──────────────────────────────────
    title_style = ParagraphStyle(
        "ReportTitle",
        fontName="Helvetica-Bold",
        fontSize=22,
        textColor=palette["dark"],
        spaceAfter=6,
        leading=26,
    )
    subtitle_style = ParagraphStyle(
        "ReportSubtitle",
        fontName="Helvetica",
        fontSize=11,
        textColor=colors.HexColor("#777777"),
        spaceAfter=20,
    )
    body_style = ParagraphStyle(
        "ReportBody",
        fontName="Helvetica",
        fontSize=10,
        leading=16,
        spaceAfter=8,
        alignment=TA_JUSTIFY,
        textColor=colors.HexColor("#222222"),
    )
    section_title_style = ParagraphStyle(
        "SectionTitle",
        fontName="Helvetica-Bold",
        fontSize=13,
        textColor=palette["dark"],
        spaceBefore=16,
        spaceAfter=8,
        borderPad=4,
    )

    # ── En-tête ───────────────────────────────────────────────
    type_labels = {"financial": "RAPPORT FINANCIER", "technical": "RAPPORT TECHNIQUE",
                   "medical": "RAPPORT MÉDICAL", "generic": "RAPPORT ANALYTIQUE"}
    badge_style = ParagraphStyle(
        "Badge", fontName="Helvetica-Bold", fontSize=9,
        textColor=palette["primary"], spaceAfter=8, letterSpacing=2
    )
    story.append(Paragraph(type_labels.get(report_type, "RAPPORT"), badge_style))
    story.append(Paragraph(report_name, title_style))
    story.append(Paragraph(
        f"Généré le {datetime.now().strftime('%d %B %Y à %H:%M')} — Powered by GPT-4o",
        subtitle_style
    ))
    story.append(HRFlowable(width="100%", thickness=2, color=palette["primary"], spaceAfter=20))

    # ── KPIs ─────────────────────────────────────────────────
    if kpis:
        story.append(Paragraph("Indicateurs Clés", section_title_style))

        color_map = {
            "green": colors.HexColor("#2e7d32"),
            "red": colors.HexColor("#c62828"),
            "blue": colors.HexColor("#1565c0"),
            "gold": colors.HexColor("#c8a96e"),
        }

        kpi_data = []
        row = []
        for i, kpi in enumerate(kpis[:4]):
            cell_color = color_map.get(kpi.get("color", "blue"), colors.HexColor("#1565c0"))
            cell = [
                Paragraph(f'<font color="#{kpi.get("color","blue") == "gold" and "c8a96e" or "555555"}">{kpi["label"]}</font>',
                          ParagraphStyle("KpiLabel", fontName="Helvetica", fontSize=9, textColor=colors.HexColor("#666"))),
                Paragraph(f'<b>{kpi["value"]}</b>',
                          ParagraphStyle("KpiVal", fontName="Helvetica-Bold", fontSize=16, textColor=cell_color)),
                Paragraph(kpi.get("trend", ""),
                          ParagraphStyle("KpiTrend", fontName="Helvetica", fontSize=9, textColor=colors.HexColor("#888"))),
            ]
            row.append(cell)
            if len(row) == 2 or i == len(kpis) - 1:
                while len(row) < 2:
                    row.append(["", "", ""])
                kpi_data.append(row)
                row = []

        if kpi_data:
            flat_data = []
            for r in kpi_data:
                flat_data.append(r)

            kpi_table = Table(
                [[r[0], r[1]] for r in kpi_data],
                colWidths=[8 * cm, 8 * cm]
            )
            kpi_table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), palette["light"]),
                ("BOX", (0, 0), (0, -1), 0.5, palette["primary"]),
                ("BOX", (1, 0), (1, -1), 0.5, palette["primary"]),
                ("TOPPADDING", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                ("LEFTPADDING", (0, 0), (-1, -1), 14),
                ("RIGHTPADDING", (0, 0), (-1, -1), 14),
                ("ROWBACKGROUNDS", (0, 0), (-1, -1), [palette["light"], colors.white]),
            ]))
            story.append(kpi_table)
            story.append(Spacer(1, 20))

    # ── Narratif ──────────────────────────────────────────────
    story.append(Paragraph("Analyse Narrative", section_title_style))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#dddddd"), spaceAfter=12))
    story.extend(markdown_to_rl(narrative, body_style))

    # ── Pied de page ──────────────────────────────────────────
    story.append(Spacer(1, 20))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#dddddd"), spaceAfter=8))
    footer_style = ParagraphStyle(
        "Footer", fontName="Helvetica", fontSize=8,
        textColor=colors.HexColor("#aaaaaa"), alignment=TA_CENTER
    )
    story.append(Paragraph(
        f"D5 — Rédacteur de Rapports IA | {datetime.now().strftime('%Y')} | Confidentiel",
        footer_style
    ))

    doc.build(story)
    return output_path

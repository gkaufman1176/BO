"""
PDF Report Generator for Compliance Results
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from io import BytesIO
from datetime import datetime


def generate_pdf_report(extracted_data, compliance_results):
    """
    Generate a PDF compliance report

    Args:
        extracted_data: Extracted nutrition data
        compliance_results: Compliance check results

    Returns:
        bytes: PDF file as bytes
    """
    buffer = BytesIO()

    # Create PDF document
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=0.75 * inch,
        leftMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch
    )

    # Container for PDF elements
    elements = []

    # Styles
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1f2937'),
        spaceAfter=30,
        alignment=TA_CENTER
    )

    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#374151'),
        spaceAfter=12,
        spaceBefore=12
    )

    # Title
    title = Paragraph("FDA Nutrition Label Compliance Report", title_style)
    elements.append(title)

    # Metadata
    product_name = extracted_data.get("productName", "Unknown Product")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    meta_data = [
        ["Product:", product_name],
        ["Report Date:", timestamp],
        ["Product Type:", extracted_data.get("_metadata", {}).get("productType", "N/A")],
    ]

    meta_table = Table(meta_data, colWidths=[1.5*inch, 4.5*inch])
    meta_table.setStyle(TableStyle([
        ('FONT', (0, 0), (0, -1), 'Helvetica-Bold', 10),
        ('FONT', (1, 0), (1, -1), 'Helvetica', 10),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#374151')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))

    elements.append(meta_table)
    elements.append(Spacer(1, 0.3 * inch))

    # Overall Score
    score = compliance_results.get("overallScore", 0)
    passed = compliance_results.get("passed", 0)
    failed = compliance_results.get("failed", 0)
    warnings = compliance_results.get("warnings", 0)

    # Score color
    if score >= 90:
        score_color = colors.green
    elif score >= 70:
        score_color = colors.orange
    else:
        score_color = colors.red

    score_heading = Paragraph("Overall Compliance Score", heading_style)
    elements.append(score_heading)

    score_data = [
        ["Overall Score", "Passed", "Failed", "Warnings"],
        [
            f"{score}%",
            str(passed),
            str(failed),
            str(warnings)
        ]
    ]

    score_table = Table(score_data, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 1.5*inch])
    score_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f3f4f6')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#1f2937')),
        ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold', 12),
        ('FONT', (0, 1), (-1, 1), 'Helvetica-Bold', 14),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TEXTCOLOR', (0, 1), (0, 1), score_color),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e5e7eb'))
    ]))

    elements.append(score_table)
    elements.append(Spacer(1, 0.3 * inch))

    # Detailed Results
    elements.append(Paragraph("Detailed Compliance Checks", heading_style))
    elements.append(Spacer(1, 0.1 * inch))

    # Group by category
    categories = {}
    for check in compliance_results.get("checks", []):
        cat = check["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(check)

    # Create table for each category
    for category_name, checks in categories.items():
        # Category header
        cat_para = Paragraph(f"<b>{category_name}</b>", styles['Heading3'])
        elements.append(cat_para)
        elements.append(Spacer(1, 0.05 * inch))

        # Create table data
        table_data = [["Status", "Requirement", "Details"]]

        for check in checks:
            status_symbol = {
                "PASS": "✓",
                "FAIL": "✗",
                "WARNING": "⚠",
                "MANUAL": "👁"
            }.get(check["status"], "?")

            status_cell = f"{status_symbol}"
            requirement_cell = check["requirement"][:60]  # Truncate long text
            details_cell = check.get("details", "")[:80]

            table_data.append([
                status_cell,
                requirement_cell,
                details_cell
            ])

        # Create table
        checks_table = Table(
            table_data,
            colWidths=[0.5*inch, 2.5*inch, 3.5*inch]
        )

        # Style table
        table_style = [
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f3f4f6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#1f2937')),
            ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold', 9),
            ('FONT', (0, 1), (-1, -1), 'Helvetica', 8),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e5e7eb')),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ]

        # Color code status column
        for i, check in enumerate(checks, start=1):
            status = check["status"]
            if status == "PASS":
                table_style.append(('TEXTCOLOR', (0, i), (0, i), colors.green))
            elif status == "FAIL":
                table_style.append(('TEXTCOLOR', (0, i), (0, i), colors.red))
            elif status == "WARNING":
                table_style.append(('TEXTCOLOR', (0, i), (0, i), colors.orange))

        checks_table.setStyle(TableStyle(table_style))

        elements.append(checks_table)
        elements.append(Spacer(1, 0.2 * inch))

    # Page break before extracted data
    elements.append(PageBreak())

    # Extracted Data Section
    elements.append(Paragraph("Extracted Nutrition Data", heading_style))
    elements.append(Spacer(1, 0.1 * inch))

    # Serving Information
    if "servingInfo" in extracted_data:
        serving_info = extracted_data["servingInfo"]

        serving_para = Paragraph("<b>Serving Information:</b>", styles['Normal'])
        elements.append(serving_para)

        serving_data = [
            ["Serving Size:",
             f"{serving_info.get('servingSize', {}).get('value', 'N/A')} "
             f"{serving_info.get('servingSize', {}).get('unit', '')} "
             f"({serving_info.get('servingSize', {}).get('householdMeasure', '')})"],
            ["Servings per Container:", str(serving_info.get("servingsPerContainer", "N/A"))]
        ]

        serving_table = Table(serving_data, colWidths=[2*inch, 4*inch])
        serving_table.setStyle(TableStyle([
            ('FONT', (0, 0), (0, -1), 'Helvetica-Bold', 9),
            ('FONT', (1, 0), (1, -1), 'Helvetica', 9),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))

        elements.append(serving_table)
        elements.append(Spacer(1, 0.15 * inch))

    # Calories
    if "calories" in extracted_data:
        cal_para = Paragraph("<b>Calories:</b>", styles['Normal'])
        elements.append(cal_para)

        calories = extracted_data["calories"]
        cal_data = [["Per Serving:", str(calories.get("perServing", "N/A"))]]

        if calories.get("perContainer"):
            cal_data.append(["Per Container:", str(calories.get("perContainer"))])

        cal_table = Table(cal_data, colWidths=[2*inch, 4*inch])
        cal_table.setStyle(TableStyle([
            ('FONT', (0, 0), (0, -1), 'Helvetica-Bold', 9),
            ('FONT', (1, 0), (1, -1), 'Helvetica', 9),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))

        elements.append(cal_table)
        elements.append(Spacer(1, 0.15 * inch))

    # Nutrients
    if "nutrients" in extracted_data:
        nut_para = Paragraph("<b>Nutrients:</b>", styles['Normal'])
        elements.append(nut_para)

        nutrients = extracted_data["nutrients"]
        nutrient_data = [["Nutrient", "Amount", "% Daily Value"]]

        nutrient_labels = {
            "totalFat": "Total Fat",
            "saturatedFat": "Saturated Fat",
            "transFat": "Trans Fat",
            "cholesterol": "Cholesterol",
            "sodium": "Sodium",
            "totalCarbohydrate": "Total Carbohydrate",
            "dietaryFiber": "Dietary Fiber",
            "totalSugars": "Total Sugars",
            "addedSugars": "Added Sugars",
            "protein": "Protein",
            "vitaminD": "Vitamin D",
            "calcium": "Calcium",
            "iron": "Iron",
            "potassium": "Potassium"
        }

        for key, label in nutrient_labels.items():
            if key in nutrients:
                nut = nutrients[key]
                amount = f"{nut.get('value', 'N/A')} {nut.get('unit', '')}"
                dv = f"{nut.get('dailyValue', '-')}%" if nut.get('dailyValue') is not None else "-"
                nutrient_data.append([label, amount, dv])

        nutrient_table = Table(nutrient_data, colWidths=[2*inch, 2*inch, 2*inch])
        nutrient_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f3f4f6')),
            ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold', 9),
            ('FONT', (0, 1), (-1, -1), 'Helvetica', 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e5e7eb')),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))

        elements.append(nutrient_table)
        elements.append(Spacer(1, 0.15 * inch))

    # Ingredients
    if "ingredients" in extracted_data:
        ing_para = Paragraph("<b>Ingredients:</b>", styles['Normal'])
        elements.append(ing_para)

        ingredients_text = extracted_data["ingredients"].get("text", "Not extracted")
        ing_content = Paragraph(ingredients_text, styles['Normal'])
        elements.append(ing_content)
        elements.append(Spacer(1, 0.15 * inch))

    # Allergens
    if "allergens" in extracted_data:
        allergens = extracted_data["allergens"]
        if allergens.get("allergenList"):
            all_para = Paragraph("<b>Allergens:</b>", styles['Normal'])
            elements.append(all_para)

            allergen_text = ", ".join(allergens.get("allergenList", []))
            all_content = Paragraph(allergen_text, styles['Normal'])
            elements.append(all_content)
            elements.append(Spacer(1, 0.15 * inch))

    # Footer
    elements.append(Spacer(1, 0.5 * inch))
    footer_text = """
    <i>
    This report is generated for internal use only and does not constitute legal or regulatory advice.
    Always consult with qualified regulatory professionals for final label approval.
    CFR References: 21 CFR 101.9, 21 CFR 101.4, FALCPA
    </i>
    """
    footer = Paragraph(footer_text, styles['Normal'])
    elements.append(footer)

    # Build PDF
    doc.build(elements)

    # Get PDF bytes
    pdf_bytes = buffer.getvalue()
    buffer.close()

    return pdf_bytes

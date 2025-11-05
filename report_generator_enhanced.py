"""
Enhanced PDF Report Generator
Includes comparison reports and claims validation
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from io import BytesIO
from datetime import datetime

# Import original function
from report_generator import generate_pdf_report as generate_basic_pdf_report


def generate_comparison_pdf_report(spec_data, pkg_data, comparison_results):
    """
    Generate PDF report for spec vs packaging comparison

    Args:
        spec_data: Extracted data from spec sheet
        pkg_data: Extracted data from packaging
        comparison_results: Comparison results

    Returns:
        bytes: PDF file as bytes
    """
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=0.75 * inch,
        leftMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch
    )

    elements = []
    styles = getSampleStyleSheet()

    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1f2937'),
        spaceAfter=30,
        alignment=TA_CENTER
    )

    title = Paragraph("Spec vs Packaging Comparison Report", title_style)
    elements.append(title)

    # Metadata
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    spec_name = spec_data.get("productName", "Spec Sheet")
    pkg_name = pkg_data.get("productName", "Packaging Label")

    meta_data = [
        ["Spec Sheet:", spec_name],
        ["Packaging:", pkg_name],
        ["Report Date:", timestamp],
        ["Match Score:", f"{comparison_results.get('matchScore', 0)}%"],
        ["Overall Status:", "PASS ✓" if comparison_results.get('overallMatch') else "FAIL ✗"]
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

    # Summary Statistics
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#374151'),
        spaceAfter=12,
        spaceBefore=12
    )

    elements.append(Paragraph("Summary", heading_style))

    summary = comparison_results.get("summary", {})
    summary_data = [
        ["Metric", "Count"],
        ["Total Sections Checked", str(summary.get("totalChecks", 0))],
        ["Exact Matches", str(summary.get("exactMatches", 0))],
        ["Within Tolerance", str(summary.get("withinTolerance", 0))],
        ["Out of Tolerance", str(summary.get("outOfTolerance", 0))]
    ]

    summary_table = Table(summary_data, colWidths=[3*inch, 2*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f3f4f6')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#1f2937')),
        ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold', 11),
        ('FONT', (0, 1), (-1, -1), 'Helvetica', 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e5e7eb')),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))

    elements.append(summary_table)
    elements.append(Spacer(1, 0.3 * inch))

    # Critical Mismatches
    critical = comparison_results.get("criticalMismatches", [])
    if critical:
        elements.append(Paragraph("❌ Critical Mismatches", heading_style))

        crit_data = [["Field", "Spec", "Packaging", "Difference", "Message"]]

        for diff in critical:
            crit_data.append([
                diff.get("field", "")[:25],
                str(diff.get("spec", ""))[:20],
                str(diff.get("packaging", ""))[:20],
                str(diff.get("difference", ""))[:15],
                diff.get("message", "")[:40]
            ])

        crit_table = Table(crit_data, colWidths=[1.2*inch, 1.1*inch, 1.1*inch, 0.9*inch, 2.2*inch])
        crit_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#fee2e2')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#7f1d1d')),
            ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold', 9),
            ('FONT', (0, 1), (-1, -1), 'Helvetica', 7),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#fca5a5')),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))

        elements.append(crit_table)
        elements.append(Spacer(1, 0.2 * inch))

    # Minor Differences
    minor = comparison_results.get("minorDifferences", [])
    if minor:
        elements.append(Paragraph("⚠ Minor Differences (Within Tolerance)", heading_style))

        minor_data = [["Field", "Spec", "Packaging", "Message"]]

        for diff in minor[:10]:  # Limit to first 10
            minor_data.append([
                diff.get("field", "")[:30],
                str(diff.get("spec", ""))[:25],
                str(diff.get("packaging", ""))[:25],
                diff.get("message", "")[:50]
            ])

        minor_table = Table(minor_data, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 2*inch])
        minor_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#fef3c7')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#78350f')),
            ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold', 9),
            ('FONT', (0, 1), (-1, -1), 'Helvetica', 7),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#fde68a')),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))

        elements.append(minor_table)
        elements.append(Spacer(1, 0.2 * inch))

    # Exact Matches
    exact = comparison_results.get("exactMatches", [])
    if exact:
        elements.append(Paragraph("✅ Exact Matches", heading_style))
        exact_text = ", ".join(exact)
        elements.append(Paragraph(exact_text, styles['Normal']))
        elements.append(Spacer(1, 0.2 * inch))

    # Footer
    elements.append(PageBreak())
    footer_text = """
    <i>
    This comparison report is generated for internal quality control purposes only.
    Critical mismatches should be investigated and corrected before production.
    Always verify packaging matches approved specifications.
    </i>
    """
    footer = Paragraph(footer_text, styles['Normal'])
    elements.append(footer)

    # Build PDF
    doc.build(elements)

    pdf_bytes = buffer.getvalue()
    buffer.close()

    return pdf_bytes


def generate_enhanced_pdf_report(extracted_data, compliance_results, claims_results=None, comparison_results=None):
    """
    Generate enhanced PDF report with claims validation and optional comparison

    Args:
        extracted_data: Extracted nutrition data
        compliance_results: Compliance check results
        claims_results: Optional claims validation results
        comparison_results: Optional comparison results

    Returns:
        bytes: PDF file as bytes
    """
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=0.75 * inch,
        leftMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch
    )

    elements = []
    styles = getSampleStyleSheet()

    # Title
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

    # Compliance Score
    score = compliance_results.get("overallScore", 0)
    passed = compliance_results.get("passed", 0)
    failed = compliance_results.get("failed", 0)

    score_heading = Paragraph("Overall Compliance Score", heading_style)
    elements.append(score_heading)

    score_color = colors.green if score >= 90 else colors.orange if score >= 70 else colors.red

    score_data = [
        ["Overall Score", "Passed", "Failed"],
        [f"{score}%", str(passed), str(failed)]
    ]

    score_table = Table(score_data, colWidths=[2*inch, 2*inch, 2*inch])
    score_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f3f4f6')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#1f2937')),
        ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold', 12),
        ('FONT', (0, 1), (-1, 1), 'Helvetica-Bold', 14),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('TEXTCOLOR', (0, 1), (0, 1), score_color),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e5e7eb')),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ]))

    elements.append(score_table)
    elements.append(Spacer(1, 0.2 * inch))

    # Claims Validation (if provided)
    if claims_results:
        elements.append(PageBreak())
        elements.append(Paragraph("Nutrition Claims Validation", heading_style))

        valid_claims = claims_results.get("validClaims", [])
        if valid_claims:
            elements.append(Paragraph("✅ Valid Claims", styles['Heading3']))

            valid_data = [["Claim", "Requirement", "Actual Value", "CFR Reference"]]

            for claim in valid_claims[:10]:  # First 10
                valid_data.append([
                    claim.get("claim", ""),
                    claim.get("requirement", "")[:40],
                    claim.get("actualValue", ""),
                    claim.get("cfr_reference", "")
                ])

            valid_table = Table(valid_data, colWidths=[1.5*inch, 2*inch, 1.2*inch, 1.8*inch])
            valid_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#d1fae5')),
                ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold', 9),
                ('FONT', (0, 1), (-1, -1), 'Helvetica', 8),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#a7f3d0')),
                ('TOPPADDING', (0, 0), (-1, -1), 5),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ]))

            elements.append(valid_table)
            elements.append(Spacer(1, 0.2 * inch))

        suggested_claims = claims_results.get("suggestedClaims", [])
        if suggested_claims:
            elements.append(Paragraph("💡 Suggested Claims (Close to Qualifying)", styles['Heading3']))

            for claim in suggested_claims[:5]:
                text = f"<b>{claim.get('claim')}</b>: {claim.get('message')} - {claim.get('suggestion', '')}"
                elements.append(Paragraph(text, styles['Normal']))
                elements.append(Spacer(1, 0.1 * inch))

    # Add original compliance details
    # (Simplified - would include full compliance check details here)

    # Footer
    elements.append(Spacer(1, 0.5 * inch))
    footer_text = """
    <i>
    This report is generated for internal use only and does not constitute legal or regulatory advice.
    Always consult with qualified regulatory professionals for final label approval.
    CFR References: 21 CFR 101.9, 21 CFR 101.4, 21 CFR 101.54, 21 CFR 101.60, FALCPA
    </i>
    """
    footer = Paragraph(footer_text, styles['Normal'])
    elements.append(footer)

    # Build PDF
    doc.build(elements)

    pdf_bytes = buffer.getvalue()
    buffer.close()

    return pdf_bytes

#!/usr/bin/env python3
"""
Plant Protein Literature Review Generator
Creates a beautifully formatted Word document for lentil, oat, and mung bean protein research
"""

from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

def add_hyperlink(paragraph, url, text):
    """Add a hyperlink to a paragraph"""
    part = paragraph.part
    r_id = part.relate_to(url, 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink', is_external=True)

    hyperlink = OxmlElement('w:hyperlink')
    hyperlink.set(qn('r:id'), r_id)

    new_run = OxmlElement('w:r')
    rPr = OxmlElement('w:rPr')

    # Hyperlink styling
    c = OxmlElement('w:color')
    c.set(qn('w:val'), '0563C1')
    rPr.append(c)

    u = OxmlElement('w:u')
    u.set(qn('w:val'), 'single')
    rPr.append(u)

    new_run.append(rPr)
    new_run.text = text
    hyperlink.append(new_run)
    paragraph._p.append(hyperlink)

    return hyperlink

def set_cell_background(cell, color):
    """Set cell background color"""
    shading_elm = OxmlElement('w:shd')
    shading_elm.set(qn('w:fill'), color)
    cell._element.get_or_add_tcPr().append(shading_elm)

def create_literature_review():
    doc = Document()

    # Set document margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    # Title
    title = doc.add_heading('Plant Protein Purification Literature Review', 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title_run = title.runs[0]
    title_run.font.color.rgb = RGBColor(0, 51, 102)

    # Subtitle
    subtitle = doc.add_paragraph('Lentil, Oat, and Mung Bean Protein Extraction & Purification')
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    subtitle_run = subtitle.runs[0]
    subtitle_run.font.size = Pt(14)
    subtitle_run.font.color.rgb = RGBColor(51, 102, 153)
    subtitle_run.bold = True

    # Date
    date_para = doc.add_paragraph('Research Period: 2010-2025 | Created: November 2025')
    date_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    date_run = date_para.runs[0]
    date_run.font.size = Pt(11)
    date_run.font.color.rgb = RGBColor(102, 102, 102)

    doc.add_paragraph()  # Spacer

    # ============ EXECUTIVE SUMMARY ============
    heading = doc.add_heading('📋 Executive Summary', 1)
    heading.runs[0].font.color.rgb = RGBColor(0, 51, 102)

    summary = doc.add_paragraph()
    summary.add_run('This literature review covers the latest advances in plant protein extraction from lentils, oats, and mung beans over the past 15 years. The research is organized by:').font.size = Pt(11)

    bullets = [
        'Protein source (lentil, oat, mung bean)',
        'Extraction method and yield efficiency',
        'Novel technologies (ultrasound, enzyme-assisted, pulsed electric field)',
        'Industrial applications and scale-up considerations',
        'Patents and commercial processes'
    ]
    for bullet in bullets:
        p = doc.add_paragraph(bullet, style='List Bullet')
        p.runs[0].font.size = Pt(11)

    doc.add_paragraph()

    # ============ COLOR LEGEND ============
    heading = doc.add_heading('🎨 Color Coding Legend', 1)
    heading.runs[0].font.color.rgb = RGBColor(0, 51, 102)

    legend_table = doc.add_table(rows=6, cols=2)
    legend_table.style = 'Light Grid Accent 1'

    legend_data = [
        ('Review Article', 'E6F2FF', 'Comprehensive overviews and meta-analyses'),
        ('Original Research', 'FFF4E6', 'Primary experimental studies'),
        ('Optimization Study', 'E8F5E9', 'Process optimization and yield improvement'),
        ('Novel Technology', 'FFF3E0', 'Emerging extraction methods'),
        ('Patent/Industrial', 'F3E5F5', 'Patents and commercial applications'),
        ('HIGH PRIORITY', 'FFE6E6', 'Essential reading - start here!')
    ]

    for idx, (study_type, color, description) in enumerate(legend_data):
        row = legend_table.rows[idx]
        set_cell_background(row.cells[0], color)
        cell0 = row.cells[0].paragraphs[0]
        cell0_run = cell0.add_run(study_type)
        cell0_run.bold = True
        cell0_run.font.size = Pt(10)

        cell1 = row.cells[1].paragraphs[0]
        cell1_run = cell1.add_run(description)
        cell1_run.font.size = Pt(10)

    doc.add_page_break()

    # ============ PRIORITY READING LIST ============
    heading = doc.add_heading('⭐ Priority Reading List - Start Here!', 1)
    heading.runs[0].font.color.rgb = RGBColor(204, 0, 0)

    doc.add_paragraph('These are the most important papers covering all three protein sources, extraction methods, and yields. Read these first to build foundational knowledge.')

    priority_papers = [
        {
            'title': 'Advances in legume protein extraction technologies: A review',
            'url': 'https://www.sciencedirect.com/science/article/abs/pii/S1466856422002843',
            'why': 'Comprehensive review of ALL legume extraction technologies with comparative yield data',
            'key_findings': 'Compares alkaline, enzymatic, ultrasound, and emerging methods. Essential overview.',
            'type': 'Review'
        },
        {
            'title': 'Lentil protein: impact of different extraction methods on structural and functional properties',
            'url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC9703575/',
            'why': 'Direct comparison of extraction methods on lentil protein with yield data',
            'key_findings': 'Alkaline extraction vs ultrasound vs enzyme-assisted. pH 9 optimal, 14.5g/100g yield.',
            'type': 'Original Research'
        },
        {
            'title': 'Oat proteins: Review of extraction methods and techno-functionality',
            'url': 'https://www.sciencedirect.com/science/article/abs/pii/S0023643821006319',
            'why': 'Most comprehensive review of oat protein extraction methods',
            'key_findings': 'Compares AE-IEP (70.1% DM, 0.27 g/g yield) vs water-based vs enzymatic methods.',
            'type': 'Review'
        },
        {
            'title': 'Lentil and Mungbean protein isolates: Processing, functional properties, and potential food applications',
            'url': 'https://www.sciencedirect.com/science/article/abs/pii/S0268005X22006622',
            'why': 'DIRECTLY compares lentil and mung bean - exactly what you need!',
            'key_findings': 'Side-by-side comparison of processing, yields, and functional properties.',
            'type': 'Original Research'
        },
        {
            'title': 'Ultrasound-assisted processing: Science, technology and challenges for the plant-based protein industry',
            'url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC8881724/',
            'why': 'Critical for understanding ultrasound impact on yield (31.78% → 58.96%)',
            'key_findings': 'Ultrasound increased cowpea protein yield by 85%. Mechanism and applications explained.',
            'type': 'Review'
        },
        {
            'title': 'A comprehensive review of mung bean proteins',
            'url': 'https://ift.onlinelibrary.wiley.com/doi/abs/10.1111/1541-4337.13183',
            'why': 'Most recent comprehensive mung bean review (2023)',
            'key_findings': 'Extraction, characterization, modifications, and applications. Yields: 8-19%.',
            'type': 'Review'
        }
    ]

    for idx, paper in enumerate(priority_papers, 1):
        table = doc.add_table(rows=5, cols=1)
        table.style = 'Light Grid Accent 1'
        set_cell_background(table.rows[0].cells[0], 'FFE6E6')

        # Title row
        title_cell = table.rows[0].cells[0]
        title_para = title_cell.paragraphs[0]
        title_run = title_para.add_run(f'#{idx}: {paper["title"]}')
        title_run.bold = True
        title_run.font.size = Pt(12)
        title_run.font.color.rgb = RGBColor(153, 0, 0)

        # URL row
        url_cell = table.rows[1].cells[0]
        url_para = url_cell.paragraphs[0]
        url_para.add_run('🔗 Link: ').bold = True
        add_hyperlink(url_para, paper['url'], paper['url'])

        # Why important row
        why_cell = table.rows[2].cells[0]
        why_para = why_cell.paragraphs[0]
        why_para.add_run('⭐ Why Read This: ').bold = True
        why_para.add_run(paper['why'])

        # Key findings row
        key_cell = table.rows[3].cells[0]
        key_para = key_cell.paragraphs[0]
        key_para.add_run('📊 Key Findings: ').bold = True
        key_para.add_run(paper['key_findings'])

        # Notes row
        notes_cell = table.rows[4].cells[0]
        notes_para = notes_cell.paragraphs[0]
        notes_para.add_run('📝 Your Notes:\n\n\n').bold = True

        doc.add_paragraph()  # Spacer

    doc.add_page_break()

    # ============ LENTIL PROTEIN SECTION ============
    heading = doc.add_heading('🌱 LENTIL PROTEIN EXTRACTION', 1)
    heading.runs[0].font.color.rgb = RGBColor(76, 175, 80)

    intro = doc.add_paragraph()
    intro.add_run('Lentils (Lens culinaris) contain 22-31% protein. Optimal extraction: pH 9.0, solid/solvent ratio 1:10, 22°C, 1 hour. Expected yield: 14.5 g protein/100g flour with 82% protein content.').font.size = Pt(11)
    doc.add_paragraph()

    lentil_papers = [
        {
            'title': 'Optimization of lentil protein extraction and the influence of process pH on protein structure and functionality',
            'url': 'https://www.sciencedirect.com/science/article/abs/pii/S002364381400111X',
            'year': '2014',
            'type': 'Optimization Study',
            'color': 'E8F5E9',
            'findings': 'pH 9.0 optimal. Solid/solvent ratio 1:10. Yield: 14.5g/100g flour, 82% protein content.',
            'impact': 'Foundational study - most cited for lentil protein extraction parameters'
        },
        {
            'title': 'Lentil protein: impact of different extraction methods on structural and functional properties',
            'url': 'https://pubmed.ncbi.nlm.nih.gov/36451759/',
            'year': '2022',
            'type': 'Original Research',
            'color': 'FFF4E6',
            'findings': 'Enzyme and ultrasound-assisted extraction did NOT increase yield vs alkaline alone.',
            'impact': 'Important negative result - saves time by showing what doesn\'t work for lentils'
        },
        {
            'title': 'Lentil protein: A review of functional properties and food application',
            'url': 'https://www.researchgate.net/publication/321216780_Lentil_protein_A_review_of_functional_properties_and_food_application_An_overview_of_lentil_protein_functionality',
            'year': '2017',
            'type': 'Review Article',
            'color': 'E6F2FF',
            'findings': 'Lentil protein = 80% storage proteins. Comparable gelling/emulsifying to pea and soy.',
            'impact': 'Explains WHY lentil protein works well - structural insights'
        }
    ]

    for paper in lentil_papers:
        table = doc.add_table(rows=6, cols=1)
        table.style = 'Light Grid Accent 1'
        set_cell_background(table.rows[0].cells[0], paper['color'])

        # Title
        cell = table.rows[0].cells[0]
        para = cell.paragraphs[0]
        run = para.add_run(paper['title'])
        run.bold = True
        run.font.size = Pt(11)

        # Year & Type
        cell = table.rows[1].cells[0]
        para = cell.paragraphs[0]
        para.add_run(f"📅 Year: {paper['year']} | 📑 Type: {paper['type']}").font.size = Pt(10)

        # URL
        cell = table.rows[2].cells[0]
        para = cell.paragraphs[0]
        para.add_run('🔗 ').font.size = Pt(10)
        add_hyperlink(para, paper['url'], paper['url'])

        # Key findings
        cell = table.rows[3].cells[0]
        para = cell.paragraphs[0]
        para.add_run('📊 Key Findings: ').bold = True
        para.add_run(paper['findings']).font.size = Pt(10)

        # Impact
        cell = table.rows[4].cells[0]
        para = cell.paragraphs[0]
        para.add_run('💡 Impact on Yield/Process: ').bold = True
        para.add_run(paper['impact']).font.size = Pt(10)

        # Notes
        cell = table.rows[5].cells[0]
        para = cell.paragraphs[0]
        para.add_run('📝 Your Notes:\n\n\n').bold = True

        doc.add_paragraph()

    doc.add_page_break()

    # ============ OAT PROTEIN SECTION ============
    heading = doc.add_heading('🌾 OAT PROTEIN EXTRACTION', 1)
    heading.runs[0].font.color.rgb = RGBColor(255, 152, 0)

    intro = doc.add_paragraph()
    intro.add_run('Oats contain 15-20% protein (60% globulins, 40% prolamins). Multiple extraction methods available with varying yields and quality. Alkaline extraction-IEP: 70.1% DM, 0.27 g/g yield. Water-based: lower yield but better color.').font.size = Pt(11)
    doc.add_paragraph()

    oat_papers = [
        {
            'title': 'Oat proteins: Review of extraction methods and techno-functionality for liquid and semi-solid applications',
            'url': 'https://www.sciencedirect.com/science/article/abs/pii/S0023643821006319',
            'year': '2021',
            'type': 'Review Article',
            'color': 'E6F2FF',
            'findings': 'AE-IEP: 70.1% DM, 0.27 g/g yield. WBE: 69.5% DM but 2.5× lower yield. Enzyme: up to 86%.',
            'impact': 'Most comprehensive comparison of oat extraction methods and yields'
        },
        {
            'title': 'Protein extraction from oat: Isoelectric precipitation and water-based extraction',
            'url': 'https://www.sciencedirect.com/science/article/pii/S2666833525000541',
            'year': '2025',
            'type': 'Original Research',
            'color': 'FFF4E6',
            'findings': 'Water-based extraction = lighter color but 2.5× lower yield than alkaline method.',
            'impact': 'Trade-off between yield and quality - important for product development'
        },
        {
            'title': 'Large-scale protein extraction from oat hulls using hydrodynamic cavitation',
            'url': 'https://www.sciencedirect.com/science/article/abs/pii/S0308814624043747',
            'year': '2024',
            'type': 'Novel Technology',
            'color': 'FFF3E0',
            'findings': 'HDC 50× more efficient than conventional NaOH extraction. HDC 20× 3.6× better.',
            'impact': 'Revolutionary yield improvement - potential game-changer for industrial scale'
        },
        {
            'title': 'Effect of Enzymatic Pre-Treatment on Oat Flakes Protein Recovery and Properties',
            'url': 'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10001348/',
            'year': '2023',
            'type': 'Optimization Study',
            'color': 'E8F5E9',
            'findings': 'Enzymatic treatment reached 86 g/100g DM, but broke down polysaccharides reduced yield.',
            'impact': 'High purity vs high yield trade-off with enzymatic methods'
        },
        {
            'title': 'Oat Protein Concentrates with Improved Solubility Produced by an Enzyme-Aided Ultrafiltration',
            'url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC8701216/',
            'year': '2021',
            'type': 'Original Research',
            'color': 'FFF4E6',
            'findings': 'Enzyme-aided pH 8.0 extraction + ultrafiltration = 40-50% protein at pilot scale.',
            'impact': 'Proven at pilot scale - viable for commercial production'
        }
    ]

    for paper in oat_papers:
        table = doc.add_table(rows=6, cols=1)
        table.style = 'Light Grid Accent 1'
        set_cell_background(table.rows[0].cells[0], paper['color'])

        # Title
        cell = table.rows[0].cells[0]
        para = cell.paragraphs[0]
        run = para.add_run(paper['title'])
        run.bold = True
        run.font.size = Pt(11)

        # Year & Type
        cell = table.rows[1].cells[0]
        para = cell.paragraphs[0]
        para.add_run(f"📅 Year: {paper['year']} | 📑 Type: {paper['type']}").font.size = Pt(10)

        # URL
        cell = table.rows[2].cells[0]
        para = cell.paragraphs[0]
        para.add_run('🔗 ').font.size = Pt(10)
        add_hyperlink(para, paper['url'], paper['url'])

        # Key findings
        cell = table.rows[3].cells[0]
        para = cell.paragraphs[0]
        para.add_run('📊 Key Findings: ').bold = True
        para.add_run(paper['findings']).font.size = Pt(10)

        # Impact
        cell = table.rows[4].cells[0]
        para = cell.paragraphs[0]
        para.add_run('💡 Impact on Yield/Process: ').bold = True
        para.add_run(paper['impact']).font.size = Pt(10)

        # Notes
        cell = table.rows[5].cells[0]
        para = cell.paragraphs[0]
        para.add_run('📝 Your Notes:\n\n\n').bold = True

        doc.add_paragraph()

    doc.add_page_break()

    # ============ MUNG BEAN PROTEIN SECTION ============
    heading = doc.add_heading('🫘 MUNG BEAN PROTEIN EXTRACTION', 1)
    heading.runs[0].font.color.rgb = RGBColor(102, 187, 106)

    intro = doc.add_paragraph()
    intro.add_run('Mung beans (Vigna radiata) contain 20-30% protein. Optimal extraction: pH 8-9, liquid ratio 10%, 31.7°C, 33.2 min. Yields: 8-19% product, 63-68% protein recovery, 83-84% crude protein content.').font.size = Pt(11)
    doc.add_paragraph()

    mung_papers = [
        {
            'title': 'A comprehensive review of mung bean proteins: Extraction, characterization, biological potential, techno-functional properties',
            'url': 'https://ift.onlinelibrary.wiley.com/doi/abs/10.1111/1541-4337.13183',
            'year': '2023',
            'type': 'Review Article',
            'color': 'E6F2FF',
            'findings': 'Complete overview: extraction, modifications, applications. Yields 8-19%. MBP = emerging protein source.',
            'impact': 'Most comprehensive mung bean review - essential reading for complete picture'
        },
        {
            'title': 'Physicochemical and chemical properties of mung bean protein isolate affected by the isolation procedure',
            'url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC10494313/',
            'year': '2023',
            'type': 'Original Research',
            'color': 'FFF4E6',
            'findings': 'Six isolation methods compared: pH 8 vs 9, micellization, hybrid with different salts (0.25-0.75M).',
            'impact': 'Direct method comparison - shows micellization = higher purity but lower yield'
        },
        {
            'title': 'Optimization of Extraction Process of Protein Isolate from Mung Bean',
            'url': 'https://www.researchgate.net/publication/271637751_Optimization_of_Extraction_Process_of_Protein_Isolate_from_Mung_Bean',
            'year': '2014',
            'type': 'Optimization Study',
            'color': 'E8F5E9',
            'findings': 'Optimal: 10% liquid ratio, 31.74°C, pH 8.97, settlement pH 4.4, 33.24 min. Yield: 63.51%+',
            'impact': 'Provides exact parameters for maximum yield - practical optimization'
        },
        {
            'title': 'A mild hybrid liquid separation to obtain functional mungbean protein',
            'url': 'https://www.sciencedirect.com/science/article/pii/S002364382101937X',
            'year': '2022',
            'type': 'Novel Technology',
            'color': 'FFF3E0',
            'findings': 'Micellization: 48% less phytic acid, 88% less trypsin inhibitor. Less denaturation.',
            'impact': 'Better protein quality and reduced anti-nutrients - improves functionality'
        },
        {
            'title': 'Extraction, physicochemical characteristics and functional properties of Mung bean protein',
            'url': 'https://www.sciencedirect.com/science/article/abs/pii/S0268005X1730005X',
            'year': '2017',
            'type': 'Original Research',
            'color': 'FFF4E6',
            'findings': 'Alkaline extraction + acid precipitation. pH 8 highest yield (80.9% for Layer 1).',
            'impact': 'Established pH 8 as optimal - foundation for many follow-up studies'
        },
        {
            'title': 'Recent advances in mung bean protein: From structure, function to application',
            'url': 'https://pubmed.ncbi.nlm.nih.gov/38897499/',
            'year': '2024',
            'type': 'Review Article',
            'color': 'E6F2FF',
            'findings': 'Latest 2024 review: structure-function relationships, emerging applications.',
            'impact': 'Most recent perspective - includes latest innovations and future directions'
        },
        {
            'title': 'The Potential Application of Mung Bean Protein in Plant-Based Food Analogs',
            'url': 'https://onlinelibrary.wiley.com/doi/full/10.1002/leg3.70011',
            'year': '2024',
            'type': 'Review Article',
            'color': 'E6F2FF',
            'findings': 'MBP foaming: 89.66% vs soy 68.66%. Good for texturization, comparable to soy products.',
            'impact': 'Shows mung bean superiority in specific applications - market opportunities'
        }
    ]

    for paper in mung_papers:
        table = doc.add_table(rows=6, cols=1)
        table.style = 'Light Grid Accent 1'
        set_cell_background(table.rows[0].cells[0], paper['color'])

        # Title
        cell = table.rows[0].cells[0]
        para = cell.paragraphs[0]
        run = para.add_run(paper['title'])
        run.bold = True
        run.font.size = Pt(11)

        # Year & Type
        cell = table.rows[1].cells[0]
        para = cell.paragraphs[0]
        para.add_run(f"📅 Year: {paper['year']} | 📑 Type: {paper['type']}").font.size = Pt(10)

        # URL
        cell = table.rows[2].cells[0]
        para = cell.paragraphs[0]
        para.add_run('🔗 ').font.size = Pt(10)
        add_hyperlink(para, paper['url'], paper['url'])

        # Key findings
        cell = table.rows[3].cells[0]
        para = cell.paragraphs[0]
        para.add_run('📊 Key Findings: ').bold = True
        para.add_run(paper['findings']).font.size = Pt(10)

        # Impact
        cell = table.rows[4].cells[0]
        para = cell.paragraphs[0]
        para.add_run('💡 Impact on Yield/Process: ').bold = True
        para.add_run(paper['impact']).font.size = Pt(10)

        # Notes
        cell = table.rows[5].cells[0]
        para = cell.paragraphs[0]
        para.add_run('📝 Your Notes:\n\n\n').bold = True

        doc.add_paragraph()

    doc.add_page_break()

    # ============ NOVEL EXTRACTION TECHNOLOGIES ============
    heading = doc.add_heading('🔬 NOVEL EXTRACTION TECHNOLOGIES', 1)
    heading.runs[0].font.color.rgb = RGBColor(156, 39, 176)

    intro = doc.add_paragraph()
    intro.add_run('Emerging technologies to improve yield and reduce environmental impact. Includes ultrasound (up to 87.9% yield), pulsed electric field, enzyme-assisted extraction, and deep eutectic solvents.').font.size = Pt(11)
    doc.add_paragraph()

    novel_papers = [
        {
            'title': 'Ultrasound-assisted processing: Science, technology and challenges for the plant-based protein industry',
            'url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC8881724/',
            'year': '2022',
            'type': 'Novel Technology',
            'color': 'FFF3E0',
            'findings': 'Ultrasound increased cowpea yield 31.78%→58.96%. Combined ultrasound+enzyme: 87.9% yield!',
            'impact': '85-176% yield improvement - biggest impact on extraction efficiency'
        },
        {
            'title': 'Recent Advances on Application of Ultrasound and Pulsed Electric Field Technologies',
            'url': 'https://link.springer.com/article/10.1007/s11947-017-1961-9',
            'year': '2017',
            'type': 'Review Article',
            'color': 'E6F2FF',
            'findings': 'PEF = non-thermal, eco-friendly. High voltage pulses (microseconds-milliseconds).',
            'impact': 'Preserves protein functionality better than thermal methods'
        },
        {
            'title': 'Plant-based proteins: advanced extraction technologies, interactions, physicochemical properties',
            'url': 'https://www.tandfonline.com/doi/full/10.1080/10408398.2023.2279696',
            'year': '2023',
            'type': 'Review Article',
            'color': 'E6F2FF',
            'findings': 'Deep eutectic solvents: 65.42% yield vs 60.76% alkaline. Enzyme: 10-22%→25-48% with enzymes.',
            'impact': 'DES and enzyme combinations show consistent yield improvements across sources'
        },
        {
            'title': 'Emerging protein sources and novel extraction techniques: a systematic review on sustainable approaches',
            'url': 'https://academic.oup.com/ijfst/article/59/10/6797/7911612',
            'year': '2024',
            'type': 'Review Article',
            'color': 'E6F2FF',
            'findings': 'Enzymatic + physical methods (PEF, ultrasound, microwave, high pressure) optimize yield.',
            'impact': 'Systematic overview of sustainability and efficiency of new methods'
        },
        {
            'title': 'Pulsed Electric Fields Effects on Proteins: Extraction, Structural Modification, and Enhancing Enzymatic Activity',
            'url': 'https://www.liebertpub.com/doi/10.1089/bioe.2024.0023',
            'year': '2024',
            'type': 'Novel Technology',
            'color': 'FFF3E0',
            'findings': 'PEF disrupts cell membranes, improves extraction, preserves structure, enhances enzyme activity.',
            'impact': 'Mechanism explained - useful for optimizing PEF parameters'
        }
    ]

    for paper in novel_papers:
        table = doc.add_table(rows=6, cols=1)
        table.style = 'Light Grid Accent 1'
        set_cell_background(table.rows[0].cells[0], paper['color'])

        # Title
        cell = table.rows[0].cells[0]
        para = cell.paragraphs[0]
        run = para.add_run(paper['title'])
        run.bold = True
        run.font.size = Pt(11)

        # Year & Type
        cell = table.rows[1].cells[0]
        para = cell.paragraphs[0]
        para.add_run(f"📅 Year: {paper['year']} | 📑 Type: {paper['type']}").font.size = Pt(10)

        # URL
        cell = table.rows[2].cells[0]
        para = cell.paragraphs[0]
        para.add_run('🔗 ').font.size = Pt(10)
        add_hyperlink(para, paper['url'], paper['url'])

        # Key findings
        cell = table.rows[3].cells[0]
        para = cell.paragraphs[0]
        para.add_run('📊 Key Findings: ').bold = True
        para.add_run(paper['findings']).font.size = Pt(10)

        # Impact
        cell = table.rows[4].cells[0]
        para = cell.paragraphs[0]
        para.add_run('💡 Impact on Yield/Process: ').bold = True
        para.add_run(paper['impact']).font.size = Pt(10)

        # Notes
        cell = table.rows[5].cells[0]
        para = cell.paragraphs[0]
        para.add_run('📝 Your Notes:\n\n\n').bold = True

        doc.add_paragraph()

    doc.add_page_break()

    # ============ COMPARATIVE & INDUSTRIAL STUDIES ============
    heading = doc.add_heading('🏭 COMPARATIVE STUDIES & INDUSTRIAL APPLICATIONS', 1)
    heading.runs[0].font.color.rgb = RGBColor(63, 81, 181)

    intro = doc.add_paragraph()
    intro.add_run('Studies comparing multiple protein sources and methods, plus industrial scale-up considerations and commercial processes.').font.size = Pt(11)
    doc.add_paragraph()

    industrial_papers = [
        {
            'title': 'Protein Extraction and Isolation from Legumes and Algae: An Industry Primer',
            'url': 'https://link.springer.com/article/10.1007/s11947-025-03958-8',
            'year': '2025',
            'type': 'Review Article',
            'color': 'E6F2FF',
            'findings': 'Industry focus: wet fractionation, centrifugation, ultrafiltration. Isoelectric precipitation most common.',
            'impact': 'Real-world industrial perspective - what actually works at scale'
        },
        {
            'title': 'Structure-Function Guided Extraction and Scale-Up of Pea Protein Isolate Production',
            'url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC9793753/',
            'year': '2022',
            'type': 'Optimization Study',
            'color': 'E8F5E9',
            'findings': 'Scale-up challenges: heat transfer, surface area/volume ratio. Benchtop→commercial (50ft long!).',
            'impact': 'Critical for understanding laboratory-to-factory translation challenges'
        },
        {
            'title': 'Legume Proteins in Food Products: Extraction Techniques, Functional Properties, and Current Challenges',
            'url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC12071647/',
            'year': '2024',
            'type': 'Review Article',
            'color': 'E6F2FF',
            'findings': 'Comparative evaluation: physical, chemical, biological methods. Efficiency, yield, purity, economics.',
            'impact': 'Holistic comparison across all legume extraction methods'
        },
        {
            'title': 'Targeting the Nutritional Value of Proteins From Legumes By-Products Through Mild Extraction Technologies',
            'url': 'https://www.frontiersin.org/journals/nutrition/articles/10.3389/fnut.2021.695793/full',
            'year': '2021',
            'type': 'Review Article',
            'color': 'E6F2FF',
            'findings': 'Mild extraction preserves nutritional value. By-products = valuable protein source.',
            'impact': 'Sustainability focus - extracting protein from waste streams'
        }
    ]

    for paper in industrial_papers:
        table = doc.add_table(rows=6, cols=1)
        table.style = 'Light Grid Accent 1'
        set_cell_background(table.rows[0].cells[0], paper['color'])

        # Title
        cell = table.rows[0].cells[0]
        para = cell.paragraphs[0]
        run = para.add_run(paper['title'])
        run.bold = True
        run.font.size = Pt(11)

        # Year & Type
        cell = table.rows[1].cells[0]
        para = cell.paragraphs[0]
        para.add_run(f"📅 Year: {paper['year']} | 📑 Type: {paper['type']}").font.size = Pt(10)

        # URL
        cell = table.rows[2].cells[0]
        para = cell.paragraphs[0]
        para.add_run('🔗 ').font.size = Pt(10)
        add_hyperlink(para, paper['url'], paper['url'])

        # Key findings
        cell = table.rows[3].cells[0]
        para = cell.paragraphs[0]
        para.add_run('📊 Key Findings: ').bold = True
        para.add_run(paper['findings']).font.size = Pt(10)

        # Impact
        cell = table.rows[4].cells[0]
        para = cell.paragraphs[0]
        para.add_run('💡 Impact on Yield/Process: ').bold = True
        para.add_run(paper['impact']).font.size = Pt(10)

        # Notes
        cell = table.rows[5].cells[0]
        para = cell.paragraphs[0]
        para.add_run('📝 Your Notes:\n\n\n').bold = True

        doc.add_paragraph()

    doc.add_page_break()

    # ============ PATENTS ============
    heading = doc.add_heading('⚖️ KEY PATENTS', 1)
    heading.runs[0].font.color.rgb = RGBColor(121, 85, 72)

    intro = doc.add_paragraph()
    intro.add_run('Commercial protein extraction patents covering mung bean, oat, and legume protein processes.').font.size = Pt(11)
    doc.add_paragraph()

    patents = [
        {
            'title': 'WO2017143298A1 - Mung bean protein isolates',
            'url': 'https://patents.google.com/patent/WO2017143298A1/en',
            'year': '2017',
            'findings': 'Methods for producing mung bean protein isolates ≥60% protein by weight.',
            'impact': 'Commercial formulation patent - high purity targets'
        },
        {
            'title': 'US Patent 10,321,705 - Functional mung bean-derived compositions',
            'url': 'https://patents.justia.com/patent/10321705',
            'year': '2019',
            'findings': 'Extraction pH 6.5-10.0, purification via isoelectric precipitation pH 5.0-6.0 or UF/MF.',
            'impact': 'Detailed process parameters protected - industrial standard method'
        },
        {
            'title': 'EP3634146 (A1) - Ultrasound and membrane filtration for legume proteins',
            'url': 'https://patents.google.com/patent/EP3634146A1/',
            'year': '2020',
            'findings': 'Ultrasound + membrane filtration for clean taste, neutral color from legumes, seeds, seaweed.',
            'impact': 'Quality improvement patent - addresses sensory issues'
        },
        {
            'title': 'WO2019228957 (A1) - Masking undesirable notes from pea/wheat/oat protein beverages',
            'url': 'https://patents.google.com/patent/WO2019228957A1/',
            'year': '2019',
            'findings': 'Ethyl cyclohexanoate masks off-flavors in pea, wheat, oat protein beverages.',
            'impact': 'Application-focused - solving taste problems in final products'
        }
    ]

    for patent in patents:
        table = doc.add_table(rows=5, cols=1)
        table.style = 'Light Grid Accent 1'
        set_cell_background(table.rows[0].cells[0], 'F3E5F5')

        # Title
        cell = table.rows[0].cells[0]
        para = cell.paragraphs[0]
        run = para.add_run(patent['title'])
        run.bold = True
        run.font.size = Pt(11)

        # Year
        cell = table.rows[1].cells[0]
        para = cell.paragraphs[0]
        para.add_run(f"📅 Year: {patent['year']} | 📑 Type: Patent").font.size = Pt(10)

        # URL
        cell = table.rows[2].cells[0]
        para = cell.paragraphs[0]
        para.add_run('🔗 ').font.size = Pt(10)
        add_hyperlink(para, patent['url'], patent['url'])

        # Key findings
        cell = table.rows[3].cells[0]
        para = cell.paragraphs[0]
        para.add_run('📊 Patent Claims: ').bold = True
        para.add_run(patent['findings']).font.size = Pt(10)

        # Impact
        cell = table.rows[4].cells[0]
        para = cell.paragraphs[0]
        para.add_run('💡 Commercial Significance: ').bold = True
        para.add_run(patent['impact']).font.size = Pt(10)

        doc.add_paragraph()

    doc.add_page_break()

    # ============ QUICK REFERENCE SUMMARY ============
    heading = doc.add_heading('📑 QUICK REFERENCE: EXTRACTION METHODS & YIELDS', 1)
    heading.runs[0].font.color.rgb = RGBColor(0, 51, 102)

    # Lentil summary
    doc.add_heading('Lentil Protein', 2)
    lentil_table = doc.add_table(rows=4, cols=2)
    lentil_table.style = 'Light Grid Accent 1'
    set_cell_background(lentil_table.rows[0].cells[0], 'E8F5E9')
    set_cell_background(lentil_table.rows[0].cells[1], 'E8F5E9')

    lentil_data = [
        ('Method', 'Alkaline Extraction + Isoelectric Precipitation'),
        ('Optimal pH', 'pH 9.0'),
        ('Yield', '14.5 g protein/100g flour (82% protein content)'),
        ('Note', 'Enzyme & ultrasound did NOT improve yield')
    ]

    for idx, (label, value) in enumerate(lentil_data):
        lentil_table.rows[idx].cells[0].paragraphs[0].add_run(label).bold = True
        lentil_table.rows[idx].cells[1].paragraphs[0].add_run(value)

    doc.add_paragraph()

    # Oat summary
    doc.add_heading('Oat Protein', 2)
    oat_table = doc.add_table(rows=5, cols=2)
    oat_table.style = 'Light Grid Accent 1'
    set_cell_background(oat_table.rows[0].cells[0], 'FFF3E0')
    set_cell_background(oat_table.rows[0].cells[1], 'FFF3E0')

    oat_data = [
        ('Best Method', 'Hydrodynamic Cavitation (HDC)'),
        ('HDC Yield', '5.8-10.8× better than conventional'),
        ('Alkaline-IEP', '70.1% DM, 0.27 g/g protein yield'),
        ('Water-Based', '69.5% DM, but 2.5× lower yield (better color)'),
        ('Enzymatic', 'Up to 86% protein content but reduced yield')
    ]

    for idx, (label, value) in enumerate(oat_data):
        oat_table.rows[idx].cells[0].paragraphs[0].add_run(label).bold = True
        oat_table.rows[idx].cells[1].paragraphs[0].add_run(value)

    doc.add_paragraph()

    # Mung bean summary
    doc.add_heading('Mung Bean Protein', 2)
    mung_table = doc.add_table(rows=5, cols=2)
    mung_table.style = 'Light Grid Accent 1'
    set_cell_background(mung_table.rows[0].cells[0], 'E8F5E9')
    set_cell_background(mung_table.rows[0].cells[1], 'E8F5E9')

    mung_data = [
        ('Method', 'Alkaline Extraction + Acid Precipitation'),
        ('Optimal pH', 'pH 8-9 (pH 8 highest yield: 80.9%)'),
        ('Optimal Conditions', '10% liquid ratio, 31.7°C, 33.2 min, settlement pH 4.4'),
        ('Yield', '8-19% product, 63-68% protein recovery, 83-84% crude protein'),
        ('Alternative', 'Micellization: higher purity, less anti-nutrients, but lower yield')
    ]

    for idx, (label, value) in enumerate(mung_data):
        mung_table.rows[idx].cells[0].paragraphs[0].add_run(label).bold = True
        mung_table.rows[idx].cells[1].paragraphs[0].add_run(value)

    doc.add_paragraph()

    # Novel technologies summary
    doc.add_heading('Novel Extraction Technologies (All Sources)', 2)
    novel_table = doc.add_table(rows=4, cols=2)
    novel_table.style = 'Light Grid Accent 1'
    set_cell_background(novel_table.rows[0].cells[0], 'FFF3E0')
    set_cell_background(novel_table.rows[0].cells[1], 'FFF3E0')

    novel_data = [
        ('Ultrasound-Assisted', 'Up to 85% yield improvement (31.78%→58.96%)'),
        ('Ultrasound + Enzyme', 'Combined: 87.9% yield (best performance)'),
        ('Deep Eutectic Solvents', '65.42% yield vs 60.76% alkaline extraction'),
        ('Enzyme-Assisted', '10-22% → 25-48% yield with papain (best enzyme)')
    ]

    for idx, (label, value) in enumerate(novel_data):
        novel_table.rows[idx].cells[0].paragraphs[0].add_run(label).bold = True
        novel_table.rows[idx].cells[1].paragraphs[0].add_run(value)

    doc.add_paragraph()
    doc.add_paragraph()

    # ============ RESEARCH TRACKING ============
    heading = doc.add_heading('✅ READING PROGRESS TRACKER', 1)
    heading.runs[0].font.color.rgb = RGBColor(0, 51, 102)

    doc.add_paragraph('Use this section to track your reading progress and organize your thoughts.')
    doc.add_paragraph()

    tracking_table = doc.add_table(rows=8, cols=4)
    tracking_table.style = 'Light Grid Accent 1'

    # Header row
    headers = ['Paper Title', 'Date Read', 'Priority', 'Status']
    for idx, header in enumerate(headers):
        cell = tracking_table.rows[0].cells[idx]
        set_cell_background(cell, '00508C')
        para = cell.paragraphs[0]
        run = para.add_run(header)
        run.bold = True
        run.font.color.rgb = RGBColor(255, 255, 255)

    # Empty rows for tracking
    for i in range(1, 8):
        for j in range(4):
            tracking_table.rows[i].cells[j].text = ''

    doc.add_paragraph()
    doc.add_paragraph()

    # Key Insights section
    doc.add_heading('💡 KEY INSIGHTS & SYNTHESIS', 2)
    doc.add_paragraph('As you read, capture overarching themes and insights here:\n\n\n\n\n\n\n')

    doc.add_heading('❓ QUESTIONS FOR FURTHER INVESTIGATION', 2)
    doc.add_paragraph('Note questions that arise during your reading:\n\n\n\n\n\n\n')

    doc.add_heading('🎯 NEXT STEPS & ACTION ITEMS', 2)
    doc.add_paragraph('Based on your review, what experiments or analyses should you conduct?\n\n\n\n\n\n\n')

    # Save document
    doc.save('/home/user/BO/Plant_Protein_Literature_Review_Roadmap.docx')
    print("✅ Document created successfully!")
    print("📄 Saved as: Plant_Protein_Literature_Review_Roadmap.docx")
    print("📊 Total papers included: 30+ with direct links")
    print("🎨 Features: Color-coded by study type, priority reading list, note-taking spaces")

if __name__ == "__main__":
    create_literature_review()

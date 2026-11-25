"""
Script to generate UniMate_IEEE_Research_Paper.docx and UniMate_IEEE_Research_Paper.pdf
Matching IEEE Conference Paper style and academic standards.
Author: Pavan Prakash Naik (USN: SCA25MSD051)
"""

import os
import sys
import re
from pathlib import Path
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

import reportlab
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas

sys.path.append(str(Path(__file__).parent))
from paper_content import (
    PAPER_TITLE, AUTHORS_TEXT, ABSTRACT_TEXT, INDEX_TERMS,
    PAPER_SECTIONS, RESEARCH_PAPER_TABLE_I
)

DOCS_DIR = Path(r"c:\Unimate_AI_Assisstanat\Academic_Documents")

# Helper for XML sanitization in ReportLab
def clean_xml(text):
    if not text:
        return ""
    text = re.sub(r'&(?!(amp|lt|gt|quot|apos);)', '&amp;', text)
    text = re.sub(r'<(?!/?(b|i|u|br|font)\b[^>]*>)', '&lt;', text)
    return text

# Helper for cell formatting in docx
def set_cell_background(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)


# -------------------------------------------------------------
# BUILD IEEE RESEARCH PAPER DOCX
# -------------------------------------------------------------
def build_ieee_research_paper_docx(output_path):
    print("Generating UniMate_IEEE_Research_Paper.docx...")
    doc = docx.Document()

    # Set 0.75-inch margins for IEEE style
    for section in doc.sections:
        section.top_margin = Inches(0.75)
        section.bottom_margin = Inches(0.75)
        section.left_margin = Inches(0.75)
        section.right_margin = Inches(0.75)
        section.page_width = Inches(8.5)
        section.page_height = Inches(11.0)

        # Header
        header = section.header
        p_hdr = header.paragraphs[0]
        p_hdr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r_hdr = p_hdr.add_run("IEEE Conference on Artificial Intelligence and University Systems (IEEE CAIUS 2026)")
        r_hdr.font.name = 'Times New Roman'
        r_hdr.font.size = Pt(8.5)
        r_hdr.font.color.rgb = RGBColor(0x64, 0x74, 0x8B)

        # Footer
        footer = section.footer
        p_ftr = footer.paragraphs[0]
        p_ftr.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        r_ftr = p_ftr.add_run("Author: Pavan Prakash Naik (USN: SCA25MSD051) | UniMate: RAG Framework for University Assistance")
        r_ftr.font.name = 'Times New Roman'
        r_ftr.font.size = Pt(8.5)
        r_ftr.font.color.rgb = RGBColor(0x64, 0x74, 0x8B)

    # Document Title
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(12)
    p_title.paragraph_format.space_after = Pt(12)
    r_t = p_title.add_run(PAPER_TITLE)
    r_t.bold = True
    r_t.font.name = 'Times New Roman'
    r_t.font.size = Pt(18)
    r_t.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)

    # Authors Block
    p_auth = doc.add_paragraph()
    p_auth.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_auth.paragraph_format.space_after = Pt(16)
    r_a = p_auth.add_run(
        "Pavan Prakash Naik\n"
        "Department of Computer Science and Engineering\n"
        "[INSTITUTION_COLLEGE_NAME_PLACEHOLDER], Affiliated to [AFFILIATED_UNIVERSITY_NAME_PLACEHOLDER]\n"
        "Email: pavan.naik@example.edu | USN: SCA25MSD051\n\n"
        "[FACULTY_GUIDE_NAME_PLACEHOLDER]\n"
        "Department of Computer Science and Engineering\n"
        "[INSTITUTION_COLLEGE_NAME_PLACEHOLDER]\n"
        "Email: guide.cse@example.edu"
    )
    r_a.font.name = 'Times New Roman'
    r_a.font.size = Pt(10)
    r_a.font.color.rgb = RGBColor(0x33, 0x41, 0x55)

    # Abstract Box
    tbl_abs = doc.add_table(rows=1, cols=1)
    tbl_abs.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell_abs = tbl_abs.rows[0].cells[0]
    cell_abs.width = Inches(7.0)
    set_cell_background(cell_abs, "F8FAFC")
    set_cell_margins(cell_abs, top=120, bottom=120, left=160, right=160)

    p_abs = cell_abs.paragraphs[0]
    p_abs.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_abs.paragraph_format.space_after = Pt(6)
    r_abh = p_abs.add_run("Abstract—")
    r_abh.bold = True
    r_abh.italic = True
    r_abh.font.name = 'Times New Roman'
    r_abh.font.size = Pt(9.5)
    r_abt = p_abs.add_run(ABSTRACT_TEXT)
    r_abt.font.name = 'Times New Roman'
    r_abt.font.size = Pt(9.5)

    p_idx = cell_abs.add_paragraph()
    p_idx.paragraph_format.space_after = Pt(0)
    r_idxh = p_idx.add_run("Index Terms—")
    r_idxh.bold = True
    r_idxh.italic = True
    r_idxh.font.name = 'Times New Roman'
    r_idxh.font.size = Pt(9)
    r_idxt = p_idx.add_run(", ".join(INDEX_TERMS))
    r_idxt.font.name = 'Times New Roman'
    r_idxt.font.size = Pt(9)

    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_after = Pt(10)

    # Section Helper
    def add_sec(title):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(title.upper())
        run.bold = True
        run.font.name = 'Times New Roman'
        run.font.size = Pt(11)
        run.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)
        return p

    def add_body(text):
        for para in text.split("\n\n"):
            p_clean = para.strip()
            if not p_clean:
                continue
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_after = Pt(6)
            run = p.add_run(p_clean)
            run.font.name = 'Times New Roman'
            run.font.size = Pt(10)

    def add_fig(img_path, caption, width=Inches(6.6)):
        if Path(img_path).exists():
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_before = Pt(6)
            p_img.paragraph_format.space_after = Pt(3)
            run = p_img.add_run()
            run.add_picture(str(img_path), width=width)

            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_before = Pt(2)
            p_cap.paragraph_format.space_after = Pt(8)
            run_cap = p_cap.add_run(caption)
            run_cap.font.name = 'Times New Roman'
            run_cap.font.size = Pt(9)
            run_cap.italic = True
            run_cap.font.color.rgb = RGBColor(0x47, 0x55, 0x69)

    # Sections
    add_sec("I. Introduction")
    add_body(PAPER_SECTIONS["1_introduction"])

    add_sec("II. Related Work")
    add_body(PAPER_SECTIONS["2_related_work"])

    add_sec("III. Problem Definition and Research Motivation")
    add_body(PAPER_SECTIONS["3_problem_formulation"])

    add_sec("IV. Proposed System Architecture")
    add_body(PAPER_SECTIONS["4_architecture"])
    add_fig(DOCS_DIR / "UniMate_Architecture_Diagram.png", "Fig. 1. UniMate Decoupled Multi-Tier System Architecture Diagram.")

    add_sec("V. Methodology")
    add_body(PAPER_SECTIONS["5_methodology"])

    add_sec("VI. Retrieval-Augmented Generation Framework")
    add_body(PAPER_SECTIONS["6_rag_framework"])
    add_fig(DOCS_DIR / "UniMate_RAG_Workflow.png", "Fig. 2. End-to-End Retrieval-Augmented Generation (RAG) Workflow and Data Pipelines.")

    add_sec("VII. Implementation Details")
    add_body(PAPER_SECTIONS["7_implementation_details"])

    add_sec("VIII. Experimental Setup")
    add_body(PAPER_SECTIONS["8_experimental_setup"])

    add_sec("IX. Results and Discussion")
    add_body(PAPER_SECTIONS["9_results_discussion"])

    # Table I
    p_thdr = doc.add_paragraph()
    p_thdr.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_thdr.paragraph_format.space_before = Pt(8)
    p_thdr.paragraph_format.space_after = Pt(4)
    r_th = p_thdr.add_run("TABLE I\nEMPIRICAL LATENCY AND PERFORMANCE BENCHMARKS (50 TRIAL RUNS)")
    r_th.bold = True
    r_th.font.name = 'Times New Roman'
    r_th.font.size = Pt(9.5)

    tbl_bench = doc.add_table(rows=len(RESEARCH_PAPER_TABLE_I) + 1, cols=4)
    tbl_bench.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Subsystem / Operation", "Mean Latency", "Observed Range", "Technical Notes"]
    col_widths = [Inches(2.5), Inches(1.1), Inches(1.3), Inches(2.1)]

    for idx, h in enumerate(headers):
        cell = tbl_bench.rows[0].cells[idx]
        cell.width = col_widths[idx]
        set_cell_background(cell, "0F172A")
        set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(h)
        run.bold = True
        run.font.name = 'Times New Roman'
        run.font.size = Pt(8.5)
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    for r_idx, row_vals in enumerate(RESEARCH_PAPER_TABLE_I):
        row_cells = tbl_bench.rows[r_idx + 1].cells
        bg_col = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(row_vals):
            row_cells[c_idx].width = col_widths[c_idx]
            set_cell_background(row_cells[c_idx], bg_col)
            set_cell_margins(row_cells[c_idx], top=60, bottom=60, left=100, right=100)
            p = row_cells[c_idx].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx in [1, 2] else WD_ALIGN_PARAGRAPH.LEFT
            run = p.add_run(val)
            run.font.name = 'Times New Roman'
            run.font.size = Pt(8)

    p_sp2 = doc.add_paragraph()
    p_sp2.paragraph_format.space_after = Pt(8)

    add_sec("X. Limitations")
    add_body(PAPER_SECTIONS["10_limitations"])

    add_sec("XI. Future Scope")
    add_body(PAPER_SECTIONS["11_future_scope"])

    add_sec("XII. Conclusion")
    add_body(PAPER_SECTIONS["12_conclusion"])

    add_sec("Acknowledgment")
    add_body(PAPER_SECTIONS["acknowledgment"])

    add_sec("References")
    for ref_num, ref_text in PAPER_SECTIONS["references"]:
        p_ref = doc.add_paragraph()
        p_ref.paragraph_format.left_indent = Inches(0.3)
        p_ref.paragraph_format.first_line_indent = Inches(-0.3)
        p_ref.paragraph_format.space_after = Pt(3)
        p_ref.paragraph_format.line_spacing = 1.05
        r_num = p_ref.add_run(f"[{ref_num}] ")
        r_num.bold = True
        r_num.font.name = 'Times New Roman'
        r_num.font.size = Pt(8.5)
        r_txt = p_ref.add_run(ref_text)
        r_txt.font.name = 'Times New Roman'
        r_txt.font.size = Pt(8.5)

    doc.save(str(output_path))
    print(f"IEEE research paper DOCX successfully written to: {output_path}")


# -------------------------------------------------------------
# NUMBERED CANVAS FOR IEEE REPORTLAB PDF
# -------------------------------------------------------------
class IEEEResearchPaperNumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(IEEEResearchPaperNumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(IEEEResearchPaperNumberedCanvas, self).showPage()
        super(IEEEResearchPaperNumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Times-Roman", 8)
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setFillColor(colors.HexColor("#475569"))

        # Running Header
        self.setLineWidth(0.5)
        self.line(45, 755, 567, 755)
        self.drawString(45, 760, "IEEE Conference on Artificial Intelligence and University Systems (IEEE CAIUS 2026)")

        # Running Footer
        self.line(45, 42, 567, 42)
        self.drawString(45, 30, f"Author: Pavan Prakash Naik (USN: SCA25MSD051) | UniMate RAG Framework")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(567, 30, page_str)

        self.restoreState()


# -------------------------------------------------------------
# BUILD IEEE RESEARCH PAPER PDF
# -------------------------------------------------------------
def build_ieee_research_paper_pdf(output_path):
    print("Generating UniMate_IEEE_Research_Paper.pdf...")
    pdf_doc = SimpleDocTemplate(
        str(output_path),
        pagesize=letter,
        leftMargin=45,
        rightMargin=45,
        topMargin=45,
        bottomMargin=45
    )

    styles = getSampleStyleSheet()

    style_title = ParagraphStyle(
        'PaperTitle',
        fontName='Times-Bold',
        fontSize=16,
        leading=19,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#0f172a'),
        spaceAfter=10
    )

    style_authors = ParagraphStyle(
        'PaperAuthors',
        fontName='Times-Roman',
        fontSize=9,
        leading=12,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#334155'),
        spaceAfter=14
    )

    style_sec = ParagraphStyle(
        'PaperSec',
        fontName='Times-Bold',
        fontSize=10,
        leading=13,
        textColor=colors.HexColor('#0f172a'),
        spaceBefore=11,
        spaceAfter=3,
        keepWithNext=True
    )

    style_body = ParagraphStyle(
        'PaperBody',
        fontName='Times-Roman',
        fontSize=8.5,
        leading=11.5,
        alignment=TA_JUSTIFY,
        textColor=colors.HexColor('#1e293b'),
        spaceAfter=5
    )

    style_abs_text = ParagraphStyle(
        'PaperAbsText',
        fontName='Times-Roman',
        fontSize=8.5,
        leading=11.5,
        alignment=TA_JUSTIFY,
        textColor=colors.HexColor('#1e293b')
    )

    style_caption = ParagraphStyle(
        'PaperCaption',
        fontName='Times-Italic',
        fontSize=8,
        leading=10,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#64748b'),
        spaceBefore=3,
        spaceAfter=8,
        keepWithNext=False
    )

    style_table_hdr = ParagraphStyle(
        'PaperTableHdr',
        fontName='Times-Bold',
        fontSize=8,
        leading=10,
        alignment=TA_CENTER,
        textColor=colors.white
    )

    style_table_cell = ParagraphStyle(
        'PaperTableCell',
        fontName='Times-Roman',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor('#1e293b')
    )

    style_table_cell_center = ParagraphStyle(
        'PaperTableCellCenter',
        fontName='Times-Roman',
        fontSize=7.5,
        leading=9.5,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#1e293b')
    )

    story = []

    def add_p(text):
        for para in text.split("\n\n"):
            p_clean = para.strip()
            if p_clean:
                story.append(Paragraph(clean_xml(p_clean), style_body))

    def add_fig_pdf(img_path, caption, w=6.6*inch, h=3.5*inch):
        if Path(img_path).exists():
            story.append(Spacer(1, 4))
            story.append(Image(str(img_path), width=w, height=h))
            story.append(Paragraph(clean_xml(caption), style_caption))

    # Title & Authors
    story.append(Spacer(1, 10))
    story.append(Paragraph(PAPER_TITLE, style_title))
    auth_html = (
        "<b>Pavan Prakash Naik</b><br/>"
        "Department of Computer Science and Engineering, [INSTITUTION_COLLEGE_NAME_PLACEHOLDER]<br/>"
        "Affiliated to [AFFILIATED_UNIVERSITY_NAME_PLACEHOLDER]<br/>"
        "Email: pavan.naik@example.edu | USN: <b>SCA25MSD051</b><br/><br/>"
        "<b>[FACULTY_GUIDE_NAME_PLACEHOLDER]</b><br/>"
        "Department of Computer Science and Engineering, [INSTITUTION_COLLEGE_NAME_PLACEHOLDER]<br/>"
        "Email: guide.cse@example.edu"
    )
    story.append(Paragraph(auth_html, style_authors))
    story.append(Spacer(1, 6))

    # Abstract Box
    abs_cell_content = [
        Paragraph(f"<i><b>Abstract</b></i>—{clean_xml(ABSTRACT_TEXT)}", style_abs_text),
        Spacer(1, 4),
        Paragraph(f"<i><b>Index Terms</b></i>—{clean_xml(', '.join(INDEX_TERMS))}", style_abs_text)
    ]
    abs_table = Table([[abs_cell_content]], colWidths=[7.0*inch])
    abs_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8fafc')),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(abs_table)
    story.append(Spacer(1, 10))

    # Sections
    story.append(Paragraph("I. INTRODUCTION", style_sec))
    add_p(PAPER_SECTIONS["1_introduction"])

    story.append(Paragraph("II. RELATED WORK", style_sec))
    add_p(PAPER_SECTIONS["2_related_work"])

    story.append(Paragraph("III. PROBLEM DEFINITION AND RESEARCH MOTIVATION", style_sec))
    add_p(PAPER_SECTIONS["3_problem_formulation"])

    story.append(Paragraph("IV. PROPOSED SYSTEM ARCHITECTURE", style_sec))
    add_p(PAPER_SECTIONS["4_architecture"])
    add_fig_pdf(DOCS_DIR / "UniMate_Architecture_Diagram.png", "Fig. 1. UniMate Decoupled Multi-Tier System Architecture Diagram.", w=6.6*inch, h=3.7*inch)

    story.append(Paragraph("V. METHODOLOGY", style_sec))
    add_p(PAPER_SECTIONS["5_methodology"])

    story.append(Paragraph("VI. RETRIEVAL-AUGMENTED GENERATION FRAMEWORK", style_sec))
    add_p(PAPER_SECTIONS["6_rag_framework"])
    add_fig_pdf(DOCS_DIR / "UniMate_RAG_Workflow.png", "Fig. 2. End-to-End Retrieval-Augmented Generation (RAG) Workflow and Data Pipelines.", w=6.6*inch, h=3.7*inch)

    story.append(Paragraph("VII. IMPLEMENTATION DETAILS", style_sec))
    add_p(PAPER_SECTIONS["7_implementation_details"])

    story.append(Paragraph("VIII. EXPERIMENTAL SETUP", style_sec))
    add_p(PAPER_SECTIONS["8_experimental_setup"])

    story.append(Paragraph("IX. RESULTS AND DISCUSSION", style_sec))
    add_p(PAPER_SECTIONS["9_results_discussion"])

    # Table I
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>TABLE I: EMPIRICAL LATENCY AND PERFORMANCE BENCHMARKS (50 TRIAL RUNS)</b>", style_caption))
    bench_rows = [[
        Paragraph("<b>Subsystem / Operation</b>", style_table_hdr),
        Paragraph("<b>Mean Latency</b>", style_table_hdr),
        Paragraph("<b>Observed Range</b>", style_table_hdr),
        Paragraph("<b>Technical Notes</b>", style_table_hdr)
    ]]
    for r in RESEARCH_PAPER_TABLE_I:
        bench_rows.append([
            Paragraph(clean_xml(r[0]), style_table_cell),
            Paragraph(clean_xml(r[1]), style_table_cell_center),
            Paragraph(clean_xml(r[2]), style_table_cell_center),
            Paragraph(clean_xml(r[3]), style_table_cell)
        ])
    t_bench = Table(bench_rows, colWidths=[2.4*inch, 1.0*inch, 1.2*inch, 2.4*inch], repeatRows=1)
    t_bench_style = [
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0f172a')),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
    ]
    for r_i in range(1, len(bench_rows)):
        bg = colors.HexColor('#f8fafc') if r_i % 2 == 1 else colors.white
        t_bench_style.append(('BACKGROUND', (0, r_i), (-1, r_i), bg))
    t_bench.setStyle(TableStyle(t_bench_style))
    story.append(t_bench)
    story.append(Spacer(1, 6))

    story.append(Paragraph("X. LIMITATIONS", style_sec))
    add_p(PAPER_SECTIONS["10_limitations"])

    story.append(Paragraph("XI. FUTURE SCOPE", style_sec))
    add_p(PAPER_SECTIONS["11_future_scope"])

    story.append(Paragraph("XII. CONCLUSION", style_sec))
    add_p(PAPER_SECTIONS["12_conclusion"])

    story.append(Paragraph("ACKNOWLEDGMENT", style_sec))
    add_p(PAPER_SECTIONS["acknowledgment"])

    story.append(Paragraph("REFERENCES", style_sec))
    for ref_num, ref_text in PAPER_SECTIONS["references"]:
        story.append(Paragraph(f"<b>[{ref_num}]</b> {clean_xml(ref_text)}", style_body))

    pdf_doc.build(story, canvasmaker=IEEEResearchPaperNumberedCanvas)
    print(f"IEEE research paper PDF successfully written to: {output_path}")


if __name__ == "__main__":
    docx_file = DOCS_DIR / "UniMate_IEEE_Research_Paper.docx"
    pdf_file = DOCS_DIR / "UniMate_IEEE_Research_Paper.pdf"

    build_ieee_research_paper_docx(docx_file)
    build_ieee_research_paper_pdf(pdf_file)

    print("\n--- IEEE RESEARCH PAPER GENERATION COMPLETED ---")
    if docx_file.exists():
        print(f"DOCX: {docx_file.name} ({docx_file.stat().st_size / 1024:.1f} KB)")
    if pdf_file.exists():
        print(f"PDF:  {pdf_file.name} ({pdf_file.stat().st_size / (1024*1024):.2f} MB)")

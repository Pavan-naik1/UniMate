"""
Script to generate UniMate_Final_Project_Report.docx and UniMate_Final_Project_Report.pdf
Containing all 47 sections, complete academic formatting, tables, diagrams, and live screenshots.
"""

import os
import sys
from pathlib import Path
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

import reportlab
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether, HRFlowable, Preformatted
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas
import re

def clean_xml(text):
    if not text:
        return ""
    text = re.sub(r'&(?!(amp|lt|gt|quot|apos);)', '&amp;', text)
    text = re.sub(r'<(?!/?(b|i|u|br|font)\b[^>]*>)', '&lt;', text)
    return text


# Import content and narrative
sys.path.append(str(Path(__file__).parent))
from report_content import (
    PROJECT_TITLE, STUDENT_NAME, STUDENT_USN, DEGREE_NAME, DEPT_NAME,
    COLLEGE_NAME, UNIVERSITY_NAME, GUIDE_NAME, GUIDE_DESIGNATION,
    HOD_NAME, PRINCIPAL_NAME, ACADEMIC_YEAR, CERTIFICATE_TEXT,
    DECLARATION_TEXT, ACKNOWLEDGEMENT_TEXT, ABSTRACT_TEXT,
    TABLE_OF_CONTENTS_DATA, LIST_OF_FIGURES_DATA, LIST_OF_TABLES_DATA,
    HARDWARE_TABLE_ROWS, SOFTWARE_TABLE_ROWS, API_TABLE_ROWS,
    TEST_CASES_DATA, PERFORMANCE_METRICS_ROWS
)
from report_sections_text import SECTIONS_TEXT

DOCS_DIR = Path(r"c:\Unimate_AI_Assisstanat\Academic_Documents")
SCREENSHOTS_DIR = DOCS_DIR / "screenshots"

# -------------------------------------------------------------
# HELPER FUNCTIONS FOR DOCX
# -------------------------------------------------------------
def set_cell_background(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
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

def create_styled_table(doc, headers, data, col_widths, col_alignments=None):
    tbl = doc.add_table(rows=len(data) + 1, cols=len(headers))
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False

    # Header Row
    hdr_cells = tbl.rows[0].cells
    for i, title in enumerate(headers):
        hdr_cells[i].width = col_widths[i]
        set_cell_background(hdr_cells[i], "1E1B4B")  # Deep Indigo
        set_cell_margins(hdr_cells[i], top=120, bottom=120, left=140, right=140)
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        run = p.add_run(title)
        run.bold = True
        run.font.name = 'Times New Roman'
        run.font.size = Pt(10)
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    # Data Rows
    for row_idx, row_data in enumerate(data):
        row_cells = tbl.rows[row_idx + 1].cells
        bg_col = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, val in enumerate(row_data):
            row_cells[col_idx].width = col_widths[col_idx]
            set_cell_background(row_cells[col_idx], bg_col)
            set_cell_margins(row_cells[col_idx], top=80, bottom=80, left=120, right=120)
            p = row_cells[col_idx].paragraphs[0]
            align = col_alignments[col_idx] if col_alignments else WD_ALIGN_PARAGRAPH.LEFT
            p.alignment = align
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            run = p.add_run(str(val))
            run.font.name = 'Times New Roman'
            run.font.size = Pt(9.5)

    p_after = doc.add_paragraph()
    p_after.paragraph_format.space_before = Pt(4)
    p_after.paragraph_format.space_after = Pt(8)
    return tbl


# -------------------------------------------------------------
# BUILD FINAL PROJECT REPORT DOCX
# -------------------------------------------------------------
def build_final_project_report_docx(output_path):
    print("Generating UniMate_Final_Project_Report.docx...")
    doc = docx.Document()

    # Configure 1-inch margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        section.page_width = Inches(8.5)
        section.page_height = Inches(11.0)

        # Header
        header = section.header
        p_hdr = header.paragraphs[0]
        p_hdr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r_hdr = p_hdr.add_run("UniMate: Final Year Project Report — Generative AI & LLMs")
        r_hdr.font.name = 'Times New Roman'
        r_hdr.font.size = Pt(8.5)
        r_hdr.font.color.rgb = RGBColor(0x64, 0x74, 0x8B)

        # Footer
        footer = section.footer
        p_ftr = footer.paragraphs[0]
        p_ftr.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        r_ftr_l = p_ftr.add_run(f"Candidate: {STUDENT_NAME} (USN: {STUDENT_USN})")
        r_ftr_l.font.name = 'Times New Roman'
        r_ftr_l.font.size = Pt(8.5)
        r_ftr_l.font.color.rgb = RGBColor(0x64, 0x74, 0x8B)

    # Helper functions
    def add_h1(title):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(title)
        run.bold = True
        run.font.name = 'Times New Roman'
        run.font.size = Pt(14)
        run.font.color.rgb = RGBColor(0x1E, 0x1B, 0x4B)
        return p

    def add_h2(title):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(title)
        run.bold = True
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)
        run.font.color.rgb = RGBColor(0x33, 0x41, 0x55)
        return p

    def add_body(text):
        for para in text.split("\n\n"):
            para_clean = para.strip()
            if not para_clean:
                continue
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.line_spacing = 1.35
            p.paragraph_format.space_after = Pt(6)
            run = p.add_run(para_clean)
            run.font.name = 'Times New Roman'
            run.font.size = Pt(12)

    def add_img(img_path, caption, width=Inches(6.2)):
        if Path(img_path).exists():
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_before = Pt(8)
            p_img.paragraph_format.space_after = Pt(4)
            run = p_img.add_run()
            run.add_picture(str(img_path), width=width)

            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_before = Pt(2)
            p_cap.paragraph_format.space_after = Pt(10)
            run_cap = p_cap.add_run(caption)
            run_cap.font.name = 'Times New Roman'
            run_cap.font.size = Pt(9.5)
            run_cap.italic = True
            run_cap.font.color.rgb = RGBColor(0x47, 0x55, 0x69)

    # =========================================================================
    # SECTION 1: TITLE PAGE
    # =========================================================================
    p_t = doc.add_paragraph()
    p_t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_t.paragraph_format.space_before = Pt(24)
    p_t.paragraph_format.space_after = Pt(12)
    r_t = p_t.add_run(PROJECT_TITLE.upper())
    r_t.bold = True
    r_t.font.name = 'Times New Roman'
    r_t.font.size = Pt(17)
    r_t.font.color.rgb = RGBColor(0x1E, 0x1B, 0x4B)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_before = Pt(8)
    p_sub.paragraph_format.space_after = Pt(24)
    r_sub = p_sub.add_run(f"A Project Report Submitted in Partial Fulfillment of the Requirements\nfor the Degree of\n{DEGREE_NAME}")
    r_sub.font.name = 'Times New Roman'
    r_sub.font.size = Pt(11)
    r_sub.italic = True
    r_sub.font.color.rgb = RGBColor(0x47, 0x55, 0x69)

    p_by = doc.add_paragraph()
    p_by.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_by.paragraph_format.space_after = Pt(4)
    r_by = p_by.add_run("Submitted By:")
    r_by.font.name = 'Times New Roman'
    r_by.font.size = Pt(11)
    r_by.bold = True

    p_st = doc.add_paragraph()
    p_st.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_st.paragraph_format.space_after = Pt(20)
    r_st = p_st.add_run(f"{STUDENT_NAME}\nUSN: {STUDENT_USN}")
    r_st.font.name = 'Times New Roman'
    r_st.font.size = Pt(12.5)
    r_st.bold = True
    r_st.font.color.rgb = RGBColor(0x1E, 0x1B, 0x4B)

    p_gui = doc.add_paragraph()
    p_gui.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_gui.paragraph_format.space_after = Pt(4)
    r_gui = p_gui.add_run("Under the Guidance of:")
    r_gui.font.name = 'Times New Roman'
    r_gui.font.size = Pt(11)
    r_gui.bold = True

    p_gt = doc.add_paragraph()
    p_gt.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_gt.paragraph_format.space_after = Pt(28)
    r_gt = p_gt.add_run(f"{GUIDE_NAME}\n{GUIDE_DESIGNATION}\n{DEPT_NAME}")
    r_gt.font.name = 'Times New Roman'
    r_gt.font.size = Pt(11.5)

    p_col = doc.add_paragraph()
    p_col.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_col.paragraph_format.space_after = Pt(4)
    r_col = p_col.add_run(f"{DEPT_NAME}\n{COLLEGE_NAME}\nAffiliated to {UNIVERSITY_NAME}\nAcademic Year: {ACADEMIC_YEAR}")
    r_col.font.name = 'Times New Roman'
    r_col.font.size = Pt(11)
    r_col.bold = True
    r_col.font.color.rgb = RGBColor(0x33, 0x41, 0x55)

    doc.add_page_break()

    # =========================================================================
    # SECTION 2: CERTIFICATE PAGE
    # =========================================================================
    add_h1("CERTIFICATE")
    add_body(CERTIFICATE_TEXT)

    p_sig = doc.add_paragraph()
    p_sig.paragraph_format.space_before = Pt(36)
    p_sig.paragraph_format.space_after = Pt(12)
    p_sig.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r_sig = p_sig.add_run(
        f"_________________________\t\t\t_________________________\n"
        f"Signature of Faculty Guide\t\t\tSignature of Head of Department\n"
        f"({GUIDE_NAME})\t\t\t(Dr. {HOD_NAME})\n\n\n"
        f"_________________________\t\t\t_________________________\n"
        f"Signature of Principal\t\t\tInstitution Seal Placeholder\n"
        f"(Dr. {PRINCIPAL_NAME})"
    )
    r_sig.font.name = 'Times New Roman'
    r_sig.font.size = Pt(10.5)

    doc.add_page_break()

    # =========================================================================
    # SECTION 3: DECLARATION
    # =========================================================================
    add_h1("DECLARATION")
    add_body(DECLARATION_TEXT)

    p_dec_sig = doc.add_paragraph()
    p_dec_sig.paragraph_format.space_before = Pt(40)
    p_dec_sig.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_ds = p_dec_sig.add_run(
        f"_________________________\n"
        f"{STUDENT_NAME}\n"
        f"USN: {STUDENT_USN}\n"
        f"Date: 24th November 2026\n"
        f"Place: {COLLEGE_NAME}"
    )
    r_ds.font.name = 'Times New Roman'
    r_ds.font.size = Pt(11)

    doc.add_page_break()

    # =========================================================================
    # SECTION 4: ACKNOWLEDGEMENT
    # =========================================================================
    add_h1("ACKNOWLEDGEMENT")
    add_body(ACKNOWLEDGEMENT_TEXT)

    doc.add_page_break()

    # =========================================================================
    # SECTION 5: ABSTRACT
    # =========================================================================
    add_h1("ABSTRACT")
    add_body(ABSTRACT_TEXT)

    doc.add_page_break()

    # =========================================================================
    # SECTION 6: TABLE OF CONTENTS
    # =========================================================================
    add_h1("TABLE OF CONTENTS")
    create_styled_table(
        doc,
        ["Sl No.", "Chapter / Section Title", "Page No."],
        TABLE_OF_CONTENTS_DATA,
        [Inches(0.9), Inches(4.6), Inches(1.0)],
        [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER]
    )

    doc.add_page_break()

    # =========================================================================
    # SECTION 7: LIST OF FIGURES
    # =========================================================================
    add_h1("LIST OF FIGURES")
    create_styled_table(
        doc,
        ["Figure No.", "Figure Caption / Title", "Page No."],
        LIST_OF_FIGURES_DATA,
        [Inches(1.2), Inches(4.3), Inches(1.0)],
        [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER]
    )

    # =========================================================================
    # SECTION 8: LIST OF TABLES
    # =========================================================================
    add_h1("LIST OF TABLES")
    create_styled_table(
        doc,
        ["Table No.", "Table Caption / Description", "Page No."],
        LIST_OF_TABLES_DATA,
        [Inches(1.2), Inches(4.3), Inches(1.0)],
        [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER]
    )

    doc.add_page_break()

    # =========================================================================
    # SECTIONS 9 TO 16: INTRODUCTION TO SCOPE
    # =========================================================================
    add_h1("9. Introduction")
    add_body(SECTIONS_TEXT["9_introduction"])

    add_h1("10. Background and Overview of Generative AI")
    add_body(SECTIONS_TEXT["10_background_genai"])

    add_h1("11. Problem Statement")
    add_body(SECTIONS_TEXT["11_problem_statement"])

    add_h1("12. Objectives of the Project")
    add_body(SECTIONS_TEXT["12_objectives"])

    add_h1("13. Existing System")
    add_body(SECTIONS_TEXT["13_existing_system"])

    add_h1("14. Limitations of Existing Systems")
    add_body(SECTIONS_TEXT["14_limitations_existing"])

    add_h1("15. Proposed System")
    add_body(SECTIONS_TEXT["15_proposed_system"])

    add_h1("16. Scope of the Project")
    add_body(SECTIONS_TEXT["16_scope"])

    doc.add_page_break()

    # =========================================================================
    # SECTIONS 17 TO 20: LITERATURE REVIEW TO TECHNOLOGIES USED
    # =========================================================================
    add_h1("17. Literature Review")
    add_body(SECTIONS_TEXT["17_literature_review"])

    add_h1("18. System Requirements")
    add_body(SECTIONS_TEXT["18_system_requirements"])

    add_h1("19. Hardware and Software Requirements")
    add_body(SECTIONS_TEXT["19_hardware_software_reqs"])

    add_h2("Table 1: Hardware Specifications")
    create_styled_table(
        doc,
        ["Hardware Component", "Minimum / Recommended Specification", "Operational Purpose"],
        HARDWARE_TABLE_ROWS,
        [Inches(1.8), Inches(2.6), Inches(2.1)],
        [WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT]
    )

    add_h2("Table 2: Software Specifications and Libraries")
    create_styled_table(
        doc,
        ["Software Component", "Version / Platform", "Role and Technical Function"],
        SOFTWARE_TABLE_ROWS,
        [Inches(1.8), Inches(2.4), Inches(2.3)],
        [WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT]
    )

    add_h1("20. Technologies Used")
    add_body(SECTIONS_TEXT["20_technologies_used"])

    doc.add_page_break()

    # =========================================================================
    # SECTIONS 21 TO 23: ARCHITECTURE, METHODOLOGY, RAG
    # =========================================================================
    add_h1("21. System Architecture")
    add_body(SECTIONS_TEXT["21_system_architecture"])
    add_img(DOCS_DIR / "UniMate_Architecture_Diagram.png", "Figure 1: UniMate Multi-Tier System Architecture Diagram")

    add_h1("22. Detailed Methodology")
    add_body(SECTIONS_TEXT["22_detailed_methodology"])

    add_h1("23. Retrieval-Augmented Generation (RAG)")
    add_body(SECTIONS_TEXT["23_rag_framework"])
    add_img(DOCS_DIR / "UniMate_RAG_Workflow.png", "Figure 2: Retrieval-Augmented Generation (RAG) Ingestion and Query Workflow")

    doc.add_page_break()

    # =========================================================================
    # SECTIONS 24 TO 28: LLM INTEGRATION TO DATABASE DESIGN
    # =========================================================================
    add_h1("24. Large Language Model Integration")
    add_body(SECTIONS_TEXT["24_llm_integration"])

    add_h1("25. Embedding Generation and Semantic Search")
    add_body(SECTIONS_TEXT["25_embedding_semantic_search"])

    add_h1("26. Vector Database and Document Retrieval")
    add_body(SECTIONS_TEXT["26_vector_db_retrieval"])

    add_h1("27. PDF Processing and Text Extraction")
    add_body(SECTIONS_TEXT["27_pdf_processing"])

    add_h1("28. Database Design")
    add_body(SECTIONS_TEXT["28_database_design"])

    doc.add_page_break()

    # =========================================================================
    # SECTIONS 29 TO 33: MODULES, FRONTEND, BACKEND, API, WORKFLOW
    # =========================================================================
    add_h1("29. Detailed Explanation of Every Implemented Module")
    add_body(SECTIONS_TEXT["29_implemented_modules"])

    add_h1("30. Frontend Implementation")
    add_body(SECTIONS_TEXT["30_frontend_implementation"])

    add_h1("31. Backend Implementation")
    add_body(SECTIONS_TEXT["31_backend_implementation"])

    add_h1("32. API Documentation")
    add_body(SECTIONS_TEXT["32_api_documentation"])

    add_h2("Table 4: FastAPI REST API Endpoints Specification")
    create_styled_table(
        doc,
        ["HTTP", "Endpoint Path", "Request Model", "Response Model", "Description"],
        API_TABLE_ROWS,
        [Inches(0.7), Inches(1.9), Inches(1.4), Inches(1.1), Inches(1.4)],
        [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT]
    )

    add_h1("33. System Workflow")
    add_body(SECTIONS_TEXT["33_system_workflow"])

    doc.add_page_break()

    # =========================================================================
    # SECTIONS 34 TO 35: UML & DFD DIAGRAMS
    # =========================================================================
    add_h1("34. UML Diagrams")
    add_body(SECTIONS_TEXT["34_uml_diagrams"])
    add_img(DOCS_DIR / "UniMate_UML_Diagrams.png", "Figure 3: Unified UML Representation (Use Case, Sequence, DFD Level 1, Database ER)", width=Inches(6.4))

    add_h1("35. Data Flow Diagrams")
    add_body(SECTIONS_TEXT["35_dfd_diagrams"])

    doc.add_page_break()

    # =========================================================================
    # SECTION 36: SCREENSHOTS OF ACTUAL APPLICATION
    # =========================================================================
    add_h1("36. Screenshots of the Actual Application")
    add_body(SECTIONS_TEXT["36_screenshots_narrative"])

    add_img(SCREENSHOTS_DIR / "screenshot_1_dashboard.png", "Figure 4: Application Screenshot: Live University Dashboard Module", width=Inches(5.8))
    add_img(SCREENSHOTS_DIR / "screenshot_2_documents.png", "Figure 5: Application Screenshot: Document Library and Multi-PDF Upload Manager", width=Inches(5.8))
    add_img(SCREENSHOTS_DIR / "screenshot_3_chatbot.png", "Figure 6: Application Screenshot: AI University Chatbot with Document-Filtered Retrieval", width=Inches(5.8))
    add_img(SCREENSHOTS_DIR / "screenshot_4_summarizer.png", "Figure 7: Application Screenshot: Academic Document Summarizer Interface", width=Inches(5.8))
    add_img(SCREENSHOTS_DIR / "screenshot_5_quiz.png", "Figure 8: Application Screenshot: Intelligent Quiz and Assessment Generator", width=Inches(5.8))
    add_img(SCREENSHOTS_DIR / "screenshot_6_study_planner.png", "Figure 9: Application Screenshot: Personalized Weekly Study Planner Interface", width=Inches(5.8))
    add_img(SCREENSHOTS_DIR / "screenshot_7_analytics.png", "Figure 10: Application Screenshot: Academic Analytics and Performance Metrics", width=Inches(5.8))
    add_img(SCREENSHOTS_DIR / "screenshot_8_genai_concepts.png", "Figure 11: Application Screenshot: Interactive GenAI Concepts and RAG Explainer", width=Inches(5.8))

    doc.add_page_break()

    # =========================================================================
    # SECTIONS 37 TO 40: TESTING, EVALUATION, RESULTS
    # =========================================================================
    add_h1("37. Testing Methodology")
    add_body(SECTIONS_TEXT["37_testing_methodology"])

    add_h1("38. Test Cases and Results")
    add_body(SECTIONS_TEXT["38_test_cases_narrative"])

    add_h2("Table 5: Automated Pytest Execution and Verification Matrix (25 Test Cases)")
    create_styled_table(
        doc,
        ["Test ID", "Feature", "Input Condition", "Expected Output", "Actual Result", "Status"],
        TEST_CASES_DATA,
        [Inches(0.9), Inches(1.1), Inches(1.3), Inches(1.3), Inches(1.3), Inches(0.6)],
        [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER]
    )

    add_h1("39. Performance Evaluation")
    add_body(SECTIONS_TEXT["39_performance_evaluation"])

    add_h2("Table 6: Latency and Performance Benchmark Metrics")
    create_styled_table(
        doc,
        ["Subsystem / Operation", "Benchmark Latency / Consumption", "Evaluation Context"],
        PERFORMANCE_METRICS_ROWS,
        [Inches(2.4), Inches(2.3), Inches(1.8)],
        [WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT]
    )

    add_h1("40. Results and Discussion")
    add_body(SECTIONS_TEXT["40_results_discussion"])

    doc.add_page_break()

    # =========================================================================
    # SECTIONS 41 TO 45: ADVANTAGES TO CONCLUSION
    # =========================================================================
    add_h1("41. Advantages")
    add_body(SECTIONS_TEXT["41_advantages"])

    add_h1("42. Limitations")
    add_body(SECTIONS_TEXT["42_limitations"])

    add_h1("43. Applications")
    add_body(SECTIONS_TEXT["43_applications"])

    add_h1("44. Future Enhancements")
    add_body(SECTIONS_TEXT["44_future_enhancements"])

    add_h1("45. Conclusion")
    add_body(SECTIONS_TEXT["45_conclusion"])

    doc.add_page_break()

    # =========================================================================
    # SECTION 46: REFERENCES
    # =========================================================================
    add_h1("46. References")
    for ref_num, ref_text in SECTIONS_TEXT["46_references"]:
        p_ref = doc.add_paragraph()
        p_ref.paragraph_format.left_indent = Inches(0.4)
        p_ref.paragraph_format.first_line_indent = Inches(-0.4)
        p_ref.paragraph_format.space_after = Pt(4)
        p_ref.paragraph_format.line_spacing = 1.15
        r_num = p_ref.add_run(f"[{ref_num}] ")
        r_num.bold = True
        r_num.font.name = 'Times New Roman'
        r_num.font.size = Pt(10.5)
        r_txt = p_ref.add_run(ref_text)
        r_txt.font.name = 'Times New Roman'
        r_txt.font.size = Pt(10.5)

    doc.add_page_break()

    # =========================================================================
    # SECTION 47: APPENDIX – SOURCE CODE SNIPPETS
    # =========================================================================
    add_h1("47. Appendix – Important Source Code Snippets")
    for listing_title, listing_code in SECTIONS_TEXT["47_appendix_code"]:
        add_h2(listing_title)
        tbl_code = doc.add_table(rows=1, cols=1)
        tbl_code.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl_code.rows[0].cells[0]
        cell.width = Inches(6.5)
        set_cell_background(cell, "F1F5F9")
        set_cell_margins(cell, top=100, bottom=100, left=150, right=150)
        p_code = cell.paragraphs[0]
        p_code.paragraph_format.space_before = Pt(0)
        p_code.paragraph_format.space_after = Pt(0)
        p_code.paragraph_format.line_spacing = 1.05
        run_code = p_code.add_run(listing_code)
        run_code.font.name = 'Courier New'
        run_code.font.size = Pt(8.5)
        run_code.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)

        p_sp = doc.add_paragraph()
        p_sp.paragraph_format.space_after = Pt(6)

    doc.save(str(output_path))
    print(f"Final project report DOCX successfully written to: {output_path}")


# -------------------------------------------------------------
# NUMBERED CANVAS FOR REPORTLAB PDF
# -------------------------------------------------------------
class ProjectReportNumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(ProjectReportNumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(ProjectReportNumberedCanvas, self).showPage()
        super(ProjectReportNumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        # Do not draw headers/footers on cover page (page 1)
        if self._pageNumber == 1:
            return

        self.saveState()
        self.setFont("Times-Roman", 8.5)
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setFillColor(colors.HexColor("#475569"))

        # Running Header
        self.setLineWidth(0.5)
        self.line(54, 750, 558, 750)
        self.drawString(54, 755, "UniMate: Final Year Project Report — Generative AI & Large Language Models")

        # Running Footer
        self.line(54, 45, 558, 45)
        self.drawString(54, 33, f"Candidate: {STUDENT_NAME} (USN: {STUDENT_USN})")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 33, page_str)

        self.restoreState()


# -------------------------------------------------------------
# BUILD FINAL PROJECT REPORT PDF
# -------------------------------------------------------------
def build_final_project_report_pdf(output_path):
    print("Generating UniMate_Final_Project_Report.pdf...")
    pdf_doc = SimpleDocTemplate(
        str(output_path),
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom Typography Styles
    style_cover_title = ParagraphStyle(
        'CoverTitle',
        fontName='Times-Bold',
        fontSize=17,
        leading=21,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#1e1b4b'),
        spaceAfter=14
    )

    style_cover_sub = ParagraphStyle(
        'CoverSub',
        fontName='Times-Italic',
        fontSize=10.5,
        leading=14,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#475569'),
        spaceAfter=20
    )

    style_cover_author = ParagraphStyle(
        'CoverAuthor',
        fontName='Times-Bold',
        fontSize=12,
        leading=16,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#1e1b4b'),
        spaceAfter=18
    )

    style_cover_meta = ParagraphStyle(
        'CoverMeta',
        fontName='Times-Roman',
        fontSize=10.5,
        leading=14,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#334155'),
        spaceAfter=6
    )

    style_h1 = ParagraphStyle(
        'ReportH1',
        fontName='Times-Bold',
        fontSize=13,
        leading=16,
        textColor=colors.HexColor('#1e1b4b'),
        spaceBefore=14,
        spaceAfter=5,
        keepWithNext=True
    )

    style_h2 = ParagraphStyle(
        'ReportH2',
        fontName='Times-Bold',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor('#334155'),
        spaceBefore=9,
        spaceAfter=4,
        keepWithNext=True
    )

    style_body = ParagraphStyle(
        'ReportBody',
        fontName='Times-Roman',
        fontSize=10,
        leading=14,
        alignment=TA_JUSTIFY,
        textColor=colors.HexColor('#1e293b'),
        spaceAfter=6
    )

    style_caption = ParagraphStyle(
        'ReportCaption',
        fontName='Times-Italic',
        fontSize=8.5,
        leading=11,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#64748b'),
        spaceBefore=4,
        spaceAfter=10,
        keepWithNext=False
    )

    style_table_hdr = ParagraphStyle(
        'TableHdr',
        fontName='Times-Bold',
        fontSize=8.5,
        leading=11,
        alignment=TA_CENTER,
        textColor=colors.white
    )

    style_table_cell = ParagraphStyle(
        'TableCell',
        fontName='Times-Roman',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor('#1e293b')
    )

    style_table_cell_center = ParagraphStyle(
        'TableCellCenter',
        fontName='Times-Roman',
        fontSize=8,
        leading=10.5,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#1e293b')
    )

    style_code = ParagraphStyle(
        'CodeStyle',
        fontName='Courier',
        fontSize=7,
        leading=9,
        textColor=colors.HexColor('#0f172a')
    )

    story = []

    # Helper for adding paragraphs
    def add_p(text):
        for para in text.split("\n\n"):
            p_clean = para.strip()
            if p_clean:
                story.append(Paragraph(clean_xml(p_clean), style_body))

    # Helper for adding images
    def add_pdf_img(img_path, caption, w=6.4*inch, h=3.4*inch):
        if Path(img_path).exists():
            story.append(Spacer(1, 4))
            story.append(Image(str(img_path), width=w, height=h))
            story.append(Paragraph(clean_xml(caption), style_caption))

    # Helper for building PDF tables
    def build_report_table(headers, data, col_widths, center_cols=None):
        center_cols = center_cols or []
        table_rows = []
        hdr_row = [Paragraph(f"<b>{clean_xml(h)}</b>", style_table_hdr) for h in headers]
        table_rows.append(hdr_row)

        for row in data:
            row_cells = []
            for idx, val in enumerate(row):
                st = style_table_cell_center if idx in center_cols else style_table_cell
                row_cells.append(Paragraph(clean_xml(str(val)), st))
            table_rows.append(row_cells)

        t = Table(table_rows, colWidths=col_widths, repeatRows=1)
        t_style = [
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e1b4b')),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ]
        for r_idx in range(1, len(table_rows)):
            bg = colors.HexColor('#f8fafc') if r_idx % 2 == 1 else colors.white
            t_style.append(('BACKGROUND', (0, r_idx), (-1, r_idx), bg))
        t.setStyle(TableStyle(t_style))
        story.append(Spacer(1, 4))
        story.append(t)
        story.append(Spacer(1, 8))

    # =========================================================================
    # SECTION 1: TITLE PAGE
    # =========================================================================
    story.append(Spacer(1, 20))
    story.append(Paragraph(PROJECT_TITLE.upper(), style_cover_title))
    story.append(Spacer(1, 10))
    story.append(Paragraph(f"A Project Report Submitted in Partial Fulfillment of the Requirements<br/>for the Degree of<br/><b>{DEGREE_NAME}</b>", style_cover_sub))
    story.append(Spacer(1, 15))
    story.append(Paragraph("<b>Submitted By:</b>", style_cover_meta))
    story.append(Paragraph(f"<b>{STUDENT_NAME}</b><br/>USN: <b>{STUDENT_USN}</b>", style_cover_author))
    story.append(Spacer(1, 15))
    story.append(Paragraph("<b>Under the Guidance of:</b>", style_cover_meta))
    story.append(Paragraph(f"<b>{GUIDE_NAME}</b>, {GUIDE_DESIGNATION}<br/>{DEPT_NAME}", style_cover_author))
    story.append(Spacer(1, 20))
    story.append(Paragraph(f"<b>{DEPT_NAME}</b><br/><b>{COLLEGE_NAME}</b><br/>Affiliated to {UNIVERSITY_NAME}<br/>Academic Year: {ACADEMIC_YEAR}", style_cover_meta))
    story.append(PageBreak())

    # =========================================================================
    # SECTION 2: CERTIFICATE PAGE
    # =========================================================================
    story.append(Paragraph("CERTIFICATE", style_h1))
    add_p(CERTIFICATE_TEXT)
    story.append(Spacer(1, 40))
    sig_data = [
        [Paragraph(f"_________________________<br/>Signature of Faculty Guide<br/>({GUIDE_NAME})", style_table_cell),
         Paragraph(f"_________________________<br/>Signature of Head of Department<br/>(Dr. {HOD_NAME})", style_table_cell)],
        [Paragraph(f"<br/><br/>_________________________<br/>Signature of Principal<br/>(Dr. {PRINCIPAL_NAME})", style_table_cell),
         Paragraph("<br/><br/>_________________________<br/>Institution Seal Placeholder", style_table_cell)]
    ]
    sig_table = Table(sig_data, colWidths=[3.2*inch, 3.2*inch])
    sig_table.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP'), ('GRID', (0, 0), (-1, -1), 0, colors.transparent)]))
    story.append(sig_table)
    story.append(PageBreak())

    # =========================================================================
    # SECTION 3: DECLARATION
    # =========================================================================
    story.append(Paragraph("DECLARATION", style_h1))
    add_p(DECLARATION_TEXT)
    story.append(Spacer(1, 30))
    dec_meta = Paragraph(
        f"<b>{STUDENT_NAME}</b><br/>USN: {STUDENT_USN}<br/>Date: 24th November 2026<br/>Place: {COLLEGE_NAME}",
        style_body
    )
    story.append(dec_meta)
    story.append(PageBreak())

    # =========================================================================
    # SECTION 4: ACKNOWLEDGEMENT
    # =========================================================================
    story.append(Paragraph("ACKNOWLEDGEMENT", style_h1))
    add_p(ACKNOWLEDGEMENT_TEXT)
    story.append(PageBreak())

    # =========================================================================
    # SECTION 5: ABSTRACT
    # =========================================================================
    story.append(Paragraph("ABSTRACT", style_h1))
    add_p(ABSTRACT_TEXT)
    story.append(PageBreak())

    # =========================================================================
    # SECTION 6: TABLE OF CONTENTS
    # =========================================================================
    story.append(Paragraph("TABLE OF CONTENTS", style_h1))
    build_report_table(
        ["Sl No.", "Chapter / Section Title", "Page No."],
        TABLE_OF_CONTENTS_DATA,
        [0.8*inch, 4.6*inch, 1.0*inch],
        center_cols=[0, 2]
    )
    story.append(PageBreak())

    # =========================================================================
    # SECTION 7 & 8: LIST OF FIGURES & TABLES
    # =========================================================================
    story.append(Paragraph("LIST OF FIGURES", style_h1))
    build_report_table(
        ["Figure No.", "Figure Caption / Title", "Page No."],
        LIST_OF_FIGURES_DATA,
        [1.2*inch, 4.2*inch, 1.0*inch],
        center_cols=[0, 2]
    )
    story.append(Spacer(1, 10))

    story.append(Paragraph("LIST OF TABLES", style_h1))
    build_report_table(
        ["Table No.", "Table Caption / Description", "Page No."],
        LIST_OF_TABLES_DATA,
        [1.2*inch, 4.2*inch, 1.0*inch],
        center_cols=[0, 2]
    )
    story.append(PageBreak())

    # =========================================================================
    # SECTIONS 9 TO 16: INTRODUCTION TO SCOPE
    # =========================================================================
    story.append(Paragraph("9. Introduction", style_h1))
    add_p(SECTIONS_TEXT["9_introduction"])

    story.append(Paragraph("10. Background and Overview of Generative AI", style_h1))
    add_p(SECTIONS_TEXT["10_background_genai"])

    story.append(Paragraph("11. Problem Statement", style_h1))
    add_p(SECTIONS_TEXT["11_problem_statement"])

    story.append(Paragraph("12. Objectives of the Project", style_h1))
    add_p(SECTIONS_TEXT["12_objectives"])

    story.append(Paragraph("13. Existing System", style_h1))
    add_p(SECTIONS_TEXT["13_existing_system"])

    story.append(Paragraph("14. Limitations of Existing Systems", style_h1))
    add_p(SECTIONS_TEXT["14_limitations_existing"])

    story.append(Paragraph("15. Proposed System", style_h1))
    add_p(SECTIONS_TEXT["15_proposed_system"])

    story.append(Paragraph("16. Scope of the Project", style_h1))
    add_p(SECTIONS_TEXT["16_scope"])
    story.append(PageBreak())

    # =========================================================================
    # SECTIONS 17 TO 20: LITERATURE REVIEW TO TECHNOLOGIES
    # =========================================================================
    story.append(Paragraph("17. Literature Review", style_h1))
    add_p(SECTIONS_TEXT["17_literature_review"])

    story.append(Paragraph("18. System Requirements", style_h1))
    add_p(SECTIONS_TEXT["18_system_requirements"])

    story.append(Paragraph("19. Hardware and Software Requirements", style_h1))
    add_p(SECTIONS_TEXT["19_hardware_software_reqs"])

    story.append(Paragraph("<b>Table 1: Hardware Specifications</b>", style_h2))
    build_report_table(
        ["Hardware Component", "Specification", "Operational Purpose"],
        HARDWARE_TABLE_ROWS,
        [1.8*inch, 2.5*inch, 2.1*inch]
    )

    story.append(Paragraph("<b>Table 2: Software Specifications and Libraries</b>", style_h2))
    build_report_table(
        ["Software Component", "Version / Platform", "Role and Technical Function"],
        SOFTWARE_TABLE_ROWS,
        [1.8*inch, 2.3*inch, 2.3*inch]
    )

    story.append(Paragraph("20. Technologies Used", style_h1))
    add_p(SECTIONS_TEXT["20_technologies_used"])
    story.append(PageBreak())

    # =========================================================================
    # SECTIONS 21 TO 23: ARCHITECTURE, METHODOLOGY, RAG
    # =========================================================================
    story.append(Paragraph("21. System Architecture", style_h1))
    add_p(SECTIONS_TEXT["21_system_architecture"])
    add_pdf_img(DOCS_DIR / "UniMate_Architecture_Diagram.png", "Figure 1: UniMate Multi-Tier System Architecture Diagram", w=6.4*inch, h=3.6*inch)

    story.append(Paragraph("22. Detailed Methodology", style_h1))
    add_p(SECTIONS_TEXT["22_detailed_methodology"])

    story.append(Paragraph("23. Retrieval-Augmented Generation (RAG)", style_h1))
    add_p(SECTIONS_TEXT["23_rag_framework"])
    add_pdf_img(DOCS_DIR / "UniMate_RAG_Workflow.png", "Figure 2: Retrieval-Augmented Generation (RAG) Ingestion and Query Workflow", w=6.4*inch, h=3.6*inch)
    story.append(PageBreak())

    # =========================================================================
    # SECTIONS 24 TO 28: LLM INTEGRATION TO DATABASE DESIGN
    # =========================================================================
    story.append(Paragraph("24. Large Language Model Integration", style_h1))
    add_p(SECTIONS_TEXT["24_llm_integration"])

    story.append(Paragraph("25. Embedding Generation and Semantic Search", style_h1))
    add_p(SECTIONS_TEXT["25_embedding_semantic_search"])

    story.append(Paragraph("26. Vector Database and Document Retrieval", style_h1))
    add_p(SECTIONS_TEXT["26_vector_db_retrieval"])

    story.append(Paragraph("27. PDF Processing and Text Extraction", style_h1))
    add_p(SECTIONS_TEXT["27_pdf_processing"])

    story.append(Paragraph("28. Database Design", style_h1))
    add_p(SECTIONS_TEXT["28_database_design"])
    story.append(PageBreak())

    # =========================================================================
    # SECTIONS 29 TO 33: MODULES, FRONTEND, BACKEND, API, WORKFLOW
    # =========================================================================
    story.append(Paragraph("29. Detailed Explanation of Every Implemented Module", style_h1))
    add_p(SECTIONS_TEXT["29_implemented_modules"])

    story.append(Paragraph("30. Frontend Implementation", style_h1))
    add_p(SECTIONS_TEXT["30_frontend_implementation"])

    story.append(Paragraph("31. Backend Implementation", style_h1))
    add_p(SECTIONS_TEXT["31_backend_implementation"])

    story.append(Paragraph("32. API Documentation", style_h1))
    add_p(SECTIONS_TEXT["32_api_documentation"])

    story.append(Paragraph("<b>Table 4: FastAPI REST API Endpoints Specification</b>", style_h2))
    build_report_table(
        ["HTTP", "Path", "Request", "Response", "Description"],
        API_TABLE_ROWS,
        [0.7*inch, 1.9*inch, 1.3*inch, 1.1*inch, 1.4*inch],
        center_cols=[0]
    )

    story.append(Paragraph("33. System Workflow", style_h1))
    add_p(SECTIONS_TEXT["33_system_workflow"])
    story.append(PageBreak())

    # =========================================================================
    # SECTIONS 34 TO 35: UML & DFD DIAGRAMS
    # =========================================================================
    story.append(Paragraph("34. UML Diagrams", style_h1))
    add_p(SECTIONS_TEXT["34_uml_diagrams"])
    add_pdf_img(DOCS_DIR / "UniMate_UML_Diagrams.png", "Figure 3: Unified UML Representation (Use Case, Sequence, DFD Level 1, Database ER)", w=6.4*inch, h=4.4*inch)

    story.append(Paragraph("35. Data Flow Diagrams", style_h1))
    add_p(SECTIONS_TEXT["35_dfd_diagrams"])
    story.append(PageBreak())

    # =========================================================================
    # SECTION 36: SCREENSHOTS OF ACTUAL APPLICATION
    # =========================================================================
    story.append(Paragraph("36. Screenshots of the Actual Application", style_h1))
    add_p(SECTIONS_TEXT["36_screenshots_narrative"])

    add_pdf_img(SCREENSHOTS_DIR / "screenshot_1_dashboard.png", "Figure 4: Application Screenshot: Live University Dashboard Module", w=5.8*inch, h=3.85*inch)
    add_pdf_img(SCREENSHOTS_DIR / "screenshot_2_documents.png", "Figure 5: Application Screenshot: Document Library and Multi-PDF Upload Manager", w=5.8*inch, h=3.85*inch)
    add_pdf_img(SCREENSHOTS_DIR / "screenshot_3_chatbot.png", "Figure 6: Application Screenshot: AI University Chatbot with Document-Filtered Retrieval", w=5.8*inch, h=3.85*inch)
    add_pdf_img(SCREENSHOTS_DIR / "screenshot_4_summarizer.png", "Figure 7: Application Screenshot: Academic Document Summarizer Interface", w=5.8*inch, h=3.85*inch)
    add_pdf_img(SCREENSHOTS_DIR / "screenshot_5_quiz.png", "Figure 8: Application Screenshot: Intelligent Quiz and Assessment Generator", w=5.8*inch, h=3.85*inch)
    add_pdf_img(SCREENSHOTS_DIR / "screenshot_6_study_planner.png", "Figure 9: Application Screenshot: Personalized Weekly Study Planner Interface", w=5.8*inch, h=3.85*inch)
    add_pdf_img(SCREENSHOTS_DIR / "screenshot_7_analytics.png", "Figure 10: Application Screenshot: Academic Analytics and Performance Metrics", w=5.8*inch, h=3.85*inch)
    add_pdf_img(SCREENSHOTS_DIR / "screenshot_8_genai_concepts.png", "Figure 11: Application Screenshot: Interactive GenAI Concepts and RAG Explainer", w=5.8*inch, h=3.85*inch)
    story.append(PageBreak())

    # =========================================================================
    # SECTIONS 37 TO 40: TESTING, EVALUATION, RESULTS
    # =========================================================================
    story.append(Paragraph("37. Testing Methodology", style_h1))
    add_p(SECTIONS_TEXT["37_testing_methodology"])

    story.append(Paragraph("38. Test Cases and Results", style_h1))
    add_p(SECTIONS_TEXT["38_test_cases_narrative"])

    story.append(Paragraph("<b>Table 5: Automated Pytest Execution and Verification Matrix (25 Test Cases)</b>", style_h2))
    build_report_table(
        ["Test ID", "Feature", "Input Condition", "Expected Output", "Actual Result", "Status"],
        TEST_CASES_DATA,
        [0.8*inch, 1.0*inch, 1.3*inch, 1.4*inch, 1.4*inch, 0.5*inch],
        center_cols=[0, 5]
    )

    story.append(Paragraph("39. Performance Evaluation", style_h1))
    add_p(SECTIONS_TEXT["39_performance_evaluation"])

    story.append(Paragraph("<b>Table 6: Latency and Performance Benchmark Metrics</b>", style_h2))
    build_report_table(
        ["Subsystem / Operation", "Benchmark Latency / Consumption", "Evaluation Context"],
        PERFORMANCE_METRICS_ROWS,
        [2.3*inch, 2.3*inch, 1.8*inch]
    )

    story.append(Paragraph("40. Results and Discussion", style_h1))
    add_p(SECTIONS_TEXT["40_results_discussion"])
    story.append(PageBreak())

    # =========================================================================
    # SECTIONS 41 TO 45: ADVANTAGES TO CONCLUSION
    # =========================================================================
    story.append(Paragraph("41. Advantages", style_h1))
    add_p(SECTIONS_TEXT["41_advantages"])

    story.append(Paragraph("42. Limitations", style_h1))
    add_p(SECTIONS_TEXT["42_limitations"])

    story.append(Paragraph("43. Applications", style_h1))
    add_p(SECTIONS_TEXT["43_applications"])

    story.append(Paragraph("44. Future Enhancements", style_h1))
    add_p(SECTIONS_TEXT["44_future_enhancements"])

    story.append(Paragraph("45. Conclusion", style_h1))
    add_p(SECTIONS_TEXT["45_conclusion"])
    story.append(PageBreak())

    # =========================================================================
    # SECTION 46: REFERENCES
    # =========================================================================
    story.append(Paragraph("46. References", style_h1))
    for ref_num, ref_text in SECTIONS_TEXT["46_references"]:
        story.append(Paragraph(f"<b>[{ref_num}]</b> {clean_xml(ref_text)}", style_body))
    story.append(PageBreak())

    # =========================================================================
    # SECTION 47: APPENDIX – SOURCE CODE SNIPPETS
    # =========================================================================
    story.append(Paragraph("47. Appendix – Important Source Code Snippets", style_h1))
    for listing_title, listing_code in SECTIONS_TEXT["47_appendix_code"]:
        story.append(Paragraph(f"<b>{listing_title}</b>", style_h2))
        story.append(Preformatted(listing_code, style_code))
        story.append(Spacer(1, 8))

    # Build the document
    pdf_doc.build(story, canvasmaker=ProjectReportNumberedCanvas)
    print(f"Final project report PDF successfully written to: {output_path}")


if __name__ == "__main__":
    docx_file = DOCS_DIR / "UniMate_Final_Project_Report.docx"
    pdf_file = DOCS_DIR / "UniMate_Final_Project_Report.pdf"

    build_final_project_report_docx(docx_file)
    build_final_project_report_pdf(pdf_file)

    print("\n--- FINAL PROJECT REPORT GENERATION COMPLETED ---")
    if docx_file.exists():
        print(f"DOCX: {docx_file.name} ({docx_file.stat().st_size / 1024:.1f} KB)")
    if pdf_file.exists():
        print(f"PDF:  {pdf_file.name} ({pdf_file.stat().st_size / (1024*1024):.2f} MB)")

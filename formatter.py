"""
Carry-On Confidence — DOCX formatter.

Takes the content dict produced by generator.generate_worksheet() and renders
it into two DOCX files: the student worksheet and (if applicable) an answer key.
Pure presentation layer — no LLM calls, no data fetching.
"""

import os
import re
import datetime
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

_KEYWORD_SEPARATOR = "______________________________________________________________________________________________"


def _add_paragraph(doc, text="", bold=False, italic=False, size=12, alignment=None):
    """Shared helper. Adds a paragraph with a single run. Returns the paragraph."""
    para = doc.add_paragraph()
    run = para.add_run(text)
    run.bold = bold
    run.italic = italic
    run.font.size = Pt(size)
    if alignment is not None:
        para.alignment = alignment
    return para


def _render_keyword_page(doc, page_content):
    """Parses 3 keyword blocks from page_content and renders them into doc."""
    blocks = page_content.split(_KEYWORD_SEPARATOR)
    blocks = [b.strip() for b in blocks if b.strip()]

    for block in blocks[:3]:
        lines = [l for l in block.splitlines() if l.strip()]

        for line in lines:
            stripped = line.strip()

            if stripped.startswith("**") and stripped.endswith("**") and stripped.count("**") == 2:
                # Word + POS line: **word (pos)**
                text = stripped[2:-2]
                _add_paragraph(doc, text, bold=True, size=12)

            elif stripped.startswith("**English:**"):
                definition = stripped[len("**English:**"):].strip()
                para = doc.add_paragraph()
                bold_run = para.add_run("English: ")
                bold_run.bold = True
                bold_run.font.size = Pt(12)
                plain_run = para.add_run(definition)
                plain_run.font.size = Pt(12)

            elif stripped.startswith("**Korean:**"):
                definition = stripped[len("**Korean:**"):].strip()
                para = doc.add_paragraph()
                bold_run = para.add_run("Korean: ")
                bold_run.bold = True
                bold_run.font.size = Pt(12)
                plain_run = para.add_run(definition)
                plain_run.font.size = Pt(12)

            elif stripped.startswith("**Synonyms:**"):
                synonyms = stripped[len("**Synonyms:**"):].strip()
                para = doc.add_paragraph()
                bold_run = para.add_run("Synonyms: ")
                bold_run.bold = True
                bold_run.font.size = Pt(12)
                plain_run = para.add_run(synonyms)
                plain_run.font.size = Pt(12)

            elif stripped.startswith("**My sentence:**"):
                para = doc.add_paragraph()
                bold_run = para.add_run("My sentence: ")
                bold_run.bold = True
                bold_run.font.size = Pt(12)

        # Two writing blank lines
        _add_paragraph(doc, "_" * 100)
        _add_paragraph(doc, "_" * 100)

        # Spacing between blocks
        _add_paragraph(doc)

    doc.add_page_break()


def format_worksheet(content: dict, level: int, level_config: dict, topic: str, location: str, _doc=None) -> str:
    """Public entry point. Renders Page 1 of the worksheet into a Document."""
    doc = _doc if _doc is not None else Document()

    # 2. Title image
    title_img = os.path.join(os.path.dirname(__file__), "assets", "carry-on-title.png")
    try:
        para = doc.add_paragraph()
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = para.add_run()
        run.add_picture(title_img, width=Inches(6.78))
    except Exception:
        _add_paragraph(doc, "Carry-On Confidence", bold=True, size=24, alignment=WD_ALIGN_PARAGRAPH.CENTER)
        _add_paragraph(doc, "Fake It Till You Make the Flight", italic=True, size=14, alignment=WD_ALIGN_PARAGRAPH.CENTER)

    # 3. Level line
    para = doc.add_paragraph()
    bold_run = para.add_run("Level: ")
    bold_run.bold = True
    bold_run.font.size = Pt(12)
    plain_run = para.add_run(level_config["cefr"] + " — " + level_config["label"])
    plain_run.font.size = Pt(12)

    # 4. Name field
    para = doc.add_paragraph()
    bold_run = para.add_run("Name: ")
    bold_run.bold = True
    bold_run.font.size = Pt(12)
    plain_run = para.add_run("_" * 40)
    plain_run.font.size = Pt(12)

    # 5. Date field
    today = datetime.datetime.now().strftime("%B %d, %Y").replace(" 0", " ")
    para = doc.add_paragraph()
    bold_run = para.add_run("Date: ")
    bold_run.bold = True
    bold_run.font.size = Pt(12)
    plain_run = para.add_run(today)
    plain_run.font.size = Pt(12)

    # 6. Section heading
    _add_paragraph(doc, "Let's Talk!", bold=True, size=14)

    # 7. Small talk questions
    for line in content["page1"].splitlines():
        stripped = line.strip()
        if stripped:
            _add_paragraph(doc, stripped, size=12)
            _add_paragraph(doc, "_" * 100, size=12)

    # 8. Page break
    doc.add_page_break()

    return None


if __name__ == "__main__":
    import sys

    MOCK_PAGE = """**boarding pass (noun)**
**English:** The document you need to get on the plane.
**Korean:** 비행기 탑승을 위해 필요한 서류입니다.
**Synonyms:** ticket · pass · travel document
**My sentence:** ______________________________

______________________________________________________________________________________________
**luggage (noun)**
**English:** The bags and suitcases you travel with.
**Korean:** 여행할 때 가지고 다니는 가방과 짐입니다.
**Synonyms:** baggage · suitcase · bags
**My sentence:** ______________________________

______________________________________________________________________________________________
**itinerary (noun)**
**English:** A detailed plan of your trip including dates and destinations.
**Korean:** 날짜와 목적지가 포함된 여행 계획서입니다.
**Synonyms:** schedule · plan · route
**My sentence:** ______________________________

______________________________________________________________________________________________"""

    # Test 1 — _add_paragraph()
    try:
        doc1 = Document()
        para = _add_paragraph(doc1, "Test bold paragraph", bold=True, size=14)
        assert para.runs[0].text == "Test bold paragraph", "Text mismatch"
        assert para.runs[0].bold is True, "Expected bold"
        print("PASS: _add_paragraph")
    except Exception as e:
        print("FAIL: _add_paragraph —", e)
        sys.exit(1)

    # Test 2 — _render_keyword_page()
    try:
        doc2 = Document()
        _render_keyword_page(doc2, MOCK_PAGE)
        all_text = " ".join(p.text for p in doc2.paragraphs)
        assert "boarding pass" in all_text, "Expected 'boarding pass' in paragraphs"
        assert "비행기 탑승" in all_text, "Expected Korean text in paragraphs"
        print("PASS: _render_keyword_page")
    except Exception as e:
        print("FAIL: _render_keyword_page —", e)
        sys.exit(1)

    # Test 3 — format_worksheet() Page 1
    try:
        mock_content = {
            "page1": "What is your favourite travel memory?\nWhere do you want to travel next?\nHave you ever had a travel disaster?"
        }
        mock_level_config = {"cefr": "B2", "label": "Upper Intermediate"}
        test_doc = Document()
        format_worksheet(mock_content, 6, mock_level_config, "airport", "tokyo", _doc=test_doc)
        all_text = " ".join(p.text for p in test_doc.paragraphs)
        assert "Let's Talk!" in all_text, "Expected 'Let's Talk!' in paragraphs"
        assert "What is your favourite travel memory?" in all_text, "Expected question in paragraphs"
        assert "B2" in all_text, "Expected 'B2' in paragraphs"
        print("PASS: format_worksheet Page 1")
    except Exception as e:
        print("FAIL: format_worksheet Page 1 —", e)
        sys.exit(1)

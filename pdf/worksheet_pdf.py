from html import escape
from pathlib import Path

from weasyprint import HTML

PURPLE = "#6C4CCF"
DARK = "#252136"
LIGHT = "#F1ECFA"
BORDER = "#E2D9F5"
MUTED = "#756F82"

BASE_DIR = Path(__file__).resolve().parent.parent
FONT_PATH = BASE_DIR / "assets" / "fonts" / "NotoNaskhArabic-Regular.ttf"


def _e(value):
    return escape(str(value or ""), quote=True).replace("\n", "<br>")


def _is_rtl_text(text):
    return any("\u0600" <= ch <= "\u06ff" or "\ufb50" <= ch <= "\ufdff" or "\ufe70" <= ch <= "\ufeff" for ch in str(text or ""))


def _direction_class(text):
    return "rtl" if _is_rtl_text(text) else "ltr"


def _page_css():
    return f"""
    @page {{
        size: A4;
        margin: 16mm 18mm 20mm 18mm;
        @bottom-left {{
            content: 'SUNBEAMS | Spread the Light';
            font-family: Arial, sans-serif;
            font-size: 8pt;
            color: #777777;
            border-top: 0.5pt solid {PURPLE};
            padding-top: 3mm;
        }}
        @bottom-right {{
            content: 'Page ' counter(page);
            font-family: Arial, sans-serif;
            font-size: 8pt;
            color: #777777;
            border-top: 0.5pt solid {PURPLE};
            padding-top: 3mm;
        }}
    }}

    @font-face {{
        font-family: 'Noto Naskh Urdu';
        src: url('{FONT_PATH.as_uri()}');
        font-weight: normal;
        font-style: normal;
    }}

    * {{ box-sizing: border-box; }}
    body {{
        font-family: 'Noto Naskh Urdu', Arial, sans-serif;
        color: {DARK};
        font-size: 10.5pt;
        line-height: 1.55;
        margin: 0;
    }}
    .center {{ text-align: center; }}
    .brand {{ color: {PURPLE}; font-family: Arial, sans-serif; font-size: 18pt; font-weight: 700; margin: 0; }}
    .tagline {{ color: {MUTED}; font-family: Arial, sans-serif; font-size: 9pt; margin: 1mm 0 3mm; }}
    .title {{ color: {PURPLE}; font-size: 17pt; font-weight: 700; margin: 0 0 5mm; }}
    .meta {{ width: 100%; border-collapse: collapse; margin-bottom: 5mm; font-size: 9pt; }}
    .meta td {{ border: 0.6pt solid #D9D3E2; padding: 2.5mm; vertical-align: middle; }}
    .meta tr:first-child td {{ background: {LIGHT}; font-weight: 600; }}
    .instructions {{ border-left: 3pt solid {PURPLE}; background: #FAF8FD; padding: 3mm 4mm; margin-bottom: 5mm; }}
    .section {{ color: {DARK}; font-size: 11.5pt; font-weight: 700; margin: 4mm 0 2mm; }}
    .question {{ margin: 0 0 2mm; page-break-inside: avoid; }}
    .option {{ margin: 0 0 1.5mm; }}
    .answer-line {{ color: #888888; letter-spacing: 0.2pt; margin: 1.5mm 0; }}
    .rtl {{ direction: rtl; text-align: right; }}
    .ltr {{ direction: ltr; text-align: left; }}
    .urdu-block {{ font-family: 'Noto Naskh Urdu', Arial, sans-serif; }}
    .no-break {{ page-break-inside: avoid; }}
    """


def build_worksheet_pdf(worksheet, meta):
    path = "/tmp/sunbeams_worksheet.pdf"
    meta = meta or {}

    title = worksheet.get("title", "Worksheet")
    instructions = worksheet.get("instructions", "Answer all questions carefully.")
    questions = worksheet.get("questions", [])
    total_marks = sum(int(q.get("marks", 1) or 1) for q in questions)
    body_rtl = _is_rtl_text(title) or _is_rtl_text(instructions) or any(_is_rtl_text(q.get("question", "")) for q in questions)

    question_html = []
    for idx, q in enumerate(questions, 1):
        qtext = q.get("question", "")
        qdir = _direction_class(qtext)
        question_html.append(f'<div class="question no-break {qdir}">')
        question_html.append(f'<div><strong>{idx}.</strong> {_e(qtext)}</div>')

        if q.get("type") == "mcq":
            for letter, option in zip("ABCD", q.get("options", [])):
                question_html.append(f'<div class="option"><strong>{letter}.</strong> {_e(option)}</div>')
        elif q.get("type") == "true_false":
            question_html.append('<div class="option"><strong>True</strong> &nbsp;&nbsp;&nbsp;&nbsp; <strong>False</strong></div>')
        elif q.get("type") == "matching":
            question_html.append('<div class="answer-line">____________________________________________________________</div>')
        else:
            lines = 2 if q.get("type") == "short_answer" else 1
            for _ in range(lines):
                question_html.append('<div class="answer-line">________________________________________________________________________________</div>')
        question_html.append('</div>')

    html = f"""
    <!doctype html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>{_page_css()}</style>
    </head>
    <body>
        <div class="center">
            <div class="brand">SUNBEAMS</div>
            <div class="tagline">Spread the Light</div>
            <div class="title {_direction_class(title)}">{_e(title)}</div>
        </div>

        <table class="meta">
            <tr>
                <td>Subject: {_e(meta.get('subject', ''))}</td>
                <td>Grade: {_e(meta.get('grade', ''))}</td>
                <td>Difficulty: {_e(meta.get('difficulty', ''))}</td>
            </tr>
            <tr>
                <td>Name: ______________________________</td>
                <td>Section: __________</td>
                <td>Date: __________</td>
            </tr>
            <tr>
                <td>Total Marks: {total_marks}</td>
                <td>Time: {_e(meta.get('time_limit', 'No limit'))}</td>
                <td>Roll No: __________</td>
            </tr>
        </table>

        <div class="instructions {_direction_class(instructions)}">
            {"<strong>ہدایات:</strong>" if body_rtl else "<strong>Instructions:</strong>"} {_e(instructions)}
        </div>

        {''.join(question_html)}
    </body>
    </html>
    """

    HTML(string=html, base_url=str(BASE_DIR)).write_pdf(path)
    return path

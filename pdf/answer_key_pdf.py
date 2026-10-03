from html import escape
from pathlib import Path

from weasyprint import HTML

PURPLE = "#6C4CCF"
DARK = "#252136"
MUTED = "#777777"

BASE_DIR = Path(__file__).resolve().parent.parent
FONT_PATH = BASE_DIR / "assets" / "fonts" / "NotoNaskhArabic-Regular.ttf"


def _e(value):
    return escape(str(value or ""), quote=True).replace("\n", "<br>")


def _is_rtl_text(text):
    return any("\u0600" <= ch <= "\u06ff" or "\ufb50" <= ch <= "\ufdff" or "\ufe70" <= ch <= "\ufeff" for ch in str(text or ""))


def _direction_class(text):
    return "rtl" if _is_rtl_text(text) else "ltr"


def _css():
    return f"""
    @page {{
        size: A4;
        margin: 18mm 18mm 20mm 18mm;
        @bottom-left {{
            content: 'SUNBEAMS | Teacher Answer Key';
            font-family: Arial, sans-serif;
            font-size: 8pt;
            color: {MUTED};
            padding-top: 3mm;
        }}
        @bottom-right {{
            content: 'Page ' counter(page);
            font-family: Arial, sans-serif;
            font-size: 8pt;
            color: {MUTED};
            padding-top: 3mm;
        }}
    }}
    @font-face {{
        font-family: 'Noto Naskh Urdu';
        src: url('{FONT_PATH.as_uri()}');
        font-weight: normal;
        font-style: normal;
    }}
    body {{ font-family: 'Noto Naskh Urdu', Arial, sans-serif; color: {DARK}; font-size: 10.5pt; line-height: 1.55; }}
    .center {{ text-align: center; }}
    .brand {{ color: {PURPLE}; font-family: Arial, sans-serif; font-size: 18pt; font-weight: 700; margin: 0; }}
    .title {{ color: {PURPLE}; font-size: 17pt; font-weight: 700; margin: 1mm 0 6mm; }}
    .worksheet-title {{ font-size: 11pt; margin-bottom: 5mm; }}
    .answer {{ margin-bottom: 4mm; page-break-inside: avoid; }}
    .explanation {{ font-size: 9pt; color: #555555; margin-top: 1mm; }}
    .rtl {{ direction: rtl; text-align: right; }}
    .ltr {{ direction: ltr; text-align: left; }}
    """


def build_answer_key_pdf(worksheet, meta):
    path = "/tmp/sunbeams_answer_key.pdf"
    title = worksheet.get("title", "Worksheet")
    parts = []
    for idx, q in enumerate(worksheet.get("questions", []), 1):
        answer = q.get("answer", "")
        explanation = q.get("explanation", "")
        direction = _direction_class(answer or explanation or q.get("question", ""))
        text = f'<strong>{idx}.</strong> {_e(answer)}'
        if explanation:
            text += f'<div class="explanation">Explanation: {_e(explanation)}</div>'
        parts.append(f'<div class="answer {direction}">{text}</div>')

    html = f"""
    <!doctype html>
    <html>
    <head><meta charset="utf-8"><style>{_css()}</style></head>
    <body>
        <div class="center">
            <div class="brand">SUNBEAMS</div>
            <div class="title">Teacher Answer Key</div>
        </div>
        <div class="worksheet-title {_direction_class(title)}">{_e(title)}</div>
        {''.join(parts)}
    </body>
    </html>
    """
    HTML(string=html, base_url=str(BASE_DIR)).write_pdf(path)
    return path

"""DOCX -> PDF via Mammoth (DOCX->HTML) + xhtml2pdf (HTML->PDF).

Trade-off: pure Python, fits the 256MB VM, but complex formatting (text boxes,
exotic fonts, advanced layout) may be simplified. Good for text-heavy documents.
"""
import io

import mammoth
from xhtml2pdf import pisa


DEFAULT_CSS = """
@page {
    size: A4;
    margin: 2cm;
}
body {
    font-family: Helvetica, Arial, sans-serif;
    font-size: 11pt;
    line-height: 1.4;
}
h1 { font-size: 20pt; margin-top: 1em; }
h2 { font-size: 16pt; margin-top: 0.9em; }
h3 { font-size: 14pt; margin-top: 0.8em; }
h4, h5, h6 { font-size: 12pt; margin-top: 0.7em; }
p { margin: 0.5em 0; }
table {
    border-collapse: collapse;
    margin: 0.8em 0;
    width: 100%;
}
th, td {
    border: 1px solid #999;
    padding: 4pt 6pt;
}
th { background-color: #eee; }
ul, ol { margin: 0.5em 0 0.5em 1.5em; }
li { margin: 0.2em 0; }
img { max-width: 100%; }
"""


def docx_to_pdf(docx_bytes: bytes) -> bytes:
    """Convert DOCX bytes to PDF bytes. Raises RuntimeError on failure."""
    html_result = mammoth.convert_to_html(io.BytesIO(docx_bytes))
    body_html = html_result.value

    full_html = (
        "<!DOCTYPE html>"
        "<html><head><meta charset='utf-8'>"
        f"<style>{DEFAULT_CSS}</style>"
        "</head><body>"
        f"{body_html}"
        "</body></html>"
    )

    out = io.BytesIO()
    status = pisa.CreatePDF(src=io.StringIO(full_html), dest=out, encoding="utf-8")
    if status.err:
        raise RuntimeError(f"xhtml2pdf failed with {status.err} errors")
    return out.getvalue()

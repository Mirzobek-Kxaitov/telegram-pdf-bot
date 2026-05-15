import io
import zipfile
from typing import List

import fitz
from pypdf import PdfReader, PdfWriter

from config import PDF_RENDER_DPI


def get_pdf_page_count(pdf_bytes: bytes) -> int:
    reader = PdfReader(io.BytesIO(pdf_bytes))
    return len(reader.pages)


def pdf_to_images(pdf_bytes: bytes, dpi: int = PDF_RENDER_DPI) -> List[bytes]:
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    try:
        return [page.get_pixmap(dpi=dpi).tobytes("jpeg") for page in doc]
    finally:
        doc.close()


def images_to_zip(images: List[bytes], prefix: str = "page") -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for i, img_bytes in enumerate(images, 1):
            zf.writestr(f"{prefix}_{i:03d}.jpg", img_bytes)
    return buf.getvalue()


def merge_pdfs(pdf_bytes_list: List[bytes]) -> bytes:
    writer = PdfWriter()
    try:
        for pdf_bytes in pdf_bytes_list:
            reader = PdfReader(io.BytesIO(pdf_bytes))
            for page in reader.pages:
                writer.add_page(page)
        out = io.BytesIO()
        writer.write(out)
        return out.getvalue()
    finally:
        writer.close()


def split_pdf_each_page(pdf_bytes: bytes) -> List[bytes]:
    reader = PdfReader(io.BytesIO(pdf_bytes))
    result = []
    for page in reader.pages:
        writer = PdfWriter()
        writer.add_page(page)
        out = io.BytesIO()
        writer.write(out)
        result.append(out.getvalue())
        writer.close()
    return result


def parse_page_ranges(range_str: str, max_pages: int) -> List[List[int]]:
    """Parse '1-3, 5, 7-9' into list of 0-based page index groups."""
    if not range_str.strip():
        raise ValueError("Bo'sh diapazon")

    groups: List[List[int]] = []
    parts = [p.strip() for p in range_str.replace(" ", "").split(",") if p.strip()]

    for part in parts:
        if "-" in part:
            try:
                start_str, end_str = part.split("-", 1)
                start, end = int(start_str), int(end_str)
            except ValueError:
                raise ValueError(f"Noto'g'ri format: {part}")
            if start < 1 or end > max_pages or start > end:
                raise ValueError(
                    f"Noto'g'ri diapazon: {part} (PDF da {max_pages} ta sahifa bor)"
                )
            groups.append(list(range(start - 1, end)))
        else:
            try:
                page = int(part)
            except ValueError:
                raise ValueError(f"Noto'g'ri format: {part}")
            if page < 1 or page > max_pages:
                raise ValueError(
                    f"Noto'g'ri sahifa: {part} (PDF da {max_pages} ta sahifa bor)"
                )
            groups.append([page - 1])

    return groups


def split_pdf_by_ranges(pdf_bytes: bytes, groups: List[List[int]]) -> List[bytes]:
    reader = PdfReader(io.BytesIO(pdf_bytes))
    result = []
    for indices in groups:
        writer = PdfWriter()
        for idx in indices:
            writer.add_page(reader.pages[idx])
        out = io.BytesIO()
        writer.write(out)
        result.append(out.getvalue())
        writer.close()
    return result

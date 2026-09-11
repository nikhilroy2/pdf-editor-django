import io
import os
from pathlib import Path
from pypdf import PdfReader, PdfWriter
from fpdf import FPDF
from django.conf import settings

# Path to font directory
FONT_DIR = Path(settings.BASE_DIR) / 'app1' / 'fonts'
FONT_PATH = FONT_DIR / 'kalpurush.ttf'
if not FONT_PATH.exists():
    FONT_PATH = FONT_DIR / 'Kalpurush.ttf'


class PDFWatermarkService:

    @staticmethod
    def _hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
        """Converts '#FF0000' or '#F00' to RGB tuple (255, 0, 0)."""
        hex_str = hex_color.lstrip('#')
        if len(hex_str) == 3:
            hex_str = ''.join([c * 2 for c in hex_str])
        return (
            int(hex_str[0:2], 16),
            int(hex_str[2:4], 16),
            int(hex_str[4:6], 16)
        )

    @staticmethod
    def _create_watermark_page(
        width_pt: float,
        height_pt: float,
        text: str,
        position: str,
        opacity: float,
        r: int, g: int, b: int
    ) -> bytes:
        """
        Creates a single-page transparent PDF overlay with the exact
        dimensions of the target page.
        """
        pdf = FPDF(unit="pt", format=(width_pt, height_pt))
        
        # Check if text contains non-ASCII characters (e.g. Bangla)
        is_unicode = any(ord(c) > 127 for c in text)
        if is_unicode and FONT_PATH.exists():
            pdf.set_text_shaping(use_shaping_engine=True, script="beng", language="ben")
            pdf.add_font("CustomFont", fname=str(FONT_PATH))
            font_name = "CustomFont"
        else:
            font_name = "Helvetica"

        pdf.add_page()

        # Dynamic font sizing based on page size and position
        if position == 'center':
            font_size = min(width_pt, height_pt) * 0.08  # ~45-60pt on standard A4
        else:
            font_size = min(width_pt, height_pt) * 0.04  # ~20-28pt for corners/headers

        pdf.set_font(font_name, style="B" if font_name == "Helvetica" else "", size=font_size)
        text_width = pdf.get_string_width(text)
        margin = 36.0  # 0.5 inch margin

        # Calculate (x, y) coordinates based on requested position
        if position == 'top-left':
            x = margin
            y = margin + font_size
        elif position == 'top-center':
            x = (width_pt - text_width) / 2
            y = margin + font_size
        elif position == 'top-right':
            x = width_pt - text_width - margin
            y = margin + font_size
        elif position == 'center':
            x = (width_pt - text_width) / 2
            y = (height_pt / 2) + (font_size / 3)
        elif position == 'bottom-left':
            x = margin
            y = height_pt - margin
        elif position == 'bottom-center':
            x = (width_pt - text_width) / 2
            y = height_pt - margin
        elif position == 'bottom-right':
            x = width_pt - text_width - margin
            y = height_pt - margin
        else:
            x = (width_pt - text_width) / 2
            y = (height_pt / 2) + (font_size / 3)

        # Apply transparency & render watermark
        with pdf.local_context(fill_opacity=opacity, stroke_opacity=opacity):
            pdf.set_text_color(r, g, b)

            if position == 'center':
                # Apply 45-degree diagonal rotation for classic center watermark look
                cx = width_pt / 2
                cy = height_pt / 2
                pdf.rotate(45, cx, cy)
                pdf.text(x, y, text)
                pdf.rotate(0)  # Reset rotation
            else:
                pdf.text(x, y, text)

        return bytes(pdf.output())

    @classmethod
    def apply_watermark(
        cls,
        file_obj,
        text: str,
        position: str = 'center',
        opacity: float = 0.25,
        color: str = '#FF0000'
    ) -> bytes:
        """
        Stamps the requested watermark onto every page of the uploaded PDF.
        Returns the output PDF as bytes.
        """
        r, g, b = cls._hex_to_rgb(color)
        reader = PdfReader(file_obj)
        writer = PdfWriter()

        for page in reader.pages:
            width_pt = float(page.mediabox.width)
            height_pt = float(page.mediabox.height)

            # 1. Generate an overlay PDF matching this specific page's size
            watermark_bytes = cls._create_watermark_page(
                width_pt=width_pt,
                height_pt=height_pt,
                text=text,
                position=position,
                opacity=opacity,
                r=r, g=g, b=b
            )

            # 2. Merge overlay onto original page
            watermark_reader = PdfReader(io.BytesIO(watermark_bytes))
            watermark_page = watermark_reader.pages[0]
            page.merge_page(watermark_page)

            writer.add_page(page)

        # 3. Write resulting PDF to in-memory bytes buffer
        output_buffer = io.BytesIO()
        writer.write(output_buffer)
        return output_buffer.getvalue()

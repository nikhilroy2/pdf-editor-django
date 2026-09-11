import io
import os
from pathlib import Path
import requests
from pypdf import PdfReader
from deep_translator import MyMemoryTranslator
from fpdf import FPDF
from django.conf import settings

# Path to font directory
FONT_DIR = Path(settings.BASE_DIR) / 'app1' / 'fonts'

MYMEMORY_LANG_MAP = {
    'en': 'english',
    'bn': 'bengali',
}


class BanglaPDF(FPDF):
    """Custom FPDF class configuring HarfBuzz Bengali text shaping and fonts."""
    def __init__(self, target_lang='bn', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.target_lang = target_lang

        # 1. CRITICAL: Explicitly specify Bengali script & language for HarfBuzz
        if target_lang == 'bn':
            self.set_text_shaping(use_shaping_engine=True, script="beng", language="ben")

        self.add_page()

        # 2. Register and set Unicode font
        if target_lang == 'bn':
            # Case-insensitive search for kalpurush font in fonts directory
            font_file = FONT_DIR / 'kalpurush.ttf'
            if not font_file.exists():
                font_file = FONT_DIR / 'Kalpurush.ttf'
            if not font_file.exists():
                for f in FONT_DIR.glob('*.ttf'):
                    font_file = f
                    break

            self.add_font("BanglaFont", fname=str(font_file))
            self.set_font("BanglaFont", size=12)
        else:
            self.set_font("Helvetica", size=11)


class PDFTranslationService:

    @staticmethod
    def extract_text(file_obj) -> str:
        """
        Extracts text while preserving headings and paragraph boundaries.
        """
        reader = PdfReader(file_obj)
        pages_text = []
        for page in reader.pages:
            t = page.extract_text()
            if t:
                pages_text.append(t.strip())

        full_text = "\n\n".join(pages_text)

        # Parse lines and reconstruct distinct paragraphs/titles
        lines = full_text.splitlines()
        paragraphs = []
        current_p = []

        for line in lines:
            line_str = line.strip()
            if not line_str:
                if current_p:
                    paragraphs.append(" ".join(current_p))
                    current_p = []
            else:
                # Detect standalone title/heading (short line not ending in comma)
                if len(line_str) < 50 and not line_str.endswith((',', ';')) and not current_p:
                    paragraphs.append(line_str)
                else:
                    current_p.append(line_str)
                    # Detect paragraph break on full sentence stops
                    if line_str.endswith(('.', '?', '!', '।', ':')):
                        paragraphs.append(" ".join(current_p))
                        current_p = []

        if current_p:
            paragraphs.append(" ".join(current_p))

        return "\n\n".join(p for p in paragraphs if p.strip())

    @staticmethod
    def _translate_google_gtx(text: str, source_lang: str, target_lang: str) -> str:
        """
        Translates text using Google's direct JSON endpoint.
        """
        url = "https://translate.googleapis.com/translate_a/single"
        params = {
            "client": "gtx",
            "sl": "auto" if source_lang == "auto" else source_lang,
            "tl": target_lang,
            "dt": "t",
            "q": text,
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }

        response = requests.get(url, params=params, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data and isinstance(data, list) and len(data) > 0 and isinstance(data[0], list):
                translated = "".join(part[0] for part in data[0] if part and part[0])
                if "500.That’s an error" not in translated and "Error 500" not in translated:
                    return translated
        return ""

    @staticmethod
    def translate_text(text: str, source_lang: str, target_lang: str) -> str:
        """
        Translates each paragraph individually to preserve layout.
        """
        if not text.strip():
            return ""

        mymemory_translator = None
        try:
            m_src = MYMEMORY_LANG_MAP.get(source_lang, source_lang)
            m_tgt = MYMEMORY_LANG_MAP.get(target_lang, target_lang)
            mymemory_translator = MyMemoryTranslator(source=m_src, target=m_tgt)
        except Exception:
            pass

        # Split into distinct paragraphs
        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
        translated_paragraphs = []

        for para in paragraphs:
            clean_para = " ".join(para.split())
            if not clean_para:
                continue

            translated = ""

            # 1. Primary: Google JSON API
            try:
                translated = PDFTranslationService._translate_google_gtx(
                    clean_para, source_lang=source_lang, target_lang=target_lang
                )
            except Exception:
                translated = ""

            # 2. Fallback: MyMemory Translator
            if not translated and mymemory_translator:
                try:
                    res = mymemory_translator.translate(clean_para)
                    if res and "500.That’s an error" not in res:
                        translated = res
                except Exception:
                    pass

            # 3. Fallback: Original text
            if not translated:
                translated = clean_para

            translated_paragraphs.append(translated)

        return "\n\n".join(translated_paragraphs)

    @staticmethod
    def generate_pdf(text: str, target_lang: str) -> bytes:
        """
        Generates a styled PDF maintaining title and paragraph structure.
        """
        pdf = BanglaPDF(target_lang=target_lang)

        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]

        for i, para in enumerate(paragraphs):
            # First item is treated as Document Title (larger & centered)
            if i == 0 and len(para) < 60:
                pdf.set_font_size(15)
                pdf.multi_cell(w=0, h=9, text=para, align="C")
                pdf.ln(6)
                pdf.set_font_size(12)  # Reset to body font size
            else:
                pdf.multi_cell(w=0, h=7.5, text=para)
                pdf.ln(5)  # Spacing between paragraphs

        return bytes(pdf.output())

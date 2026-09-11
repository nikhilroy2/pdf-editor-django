# Design & Technical Overview

### 1. Libraries & Architecture
- **Architecture**: 3-tier design (API Views → Service Layer → Models).
- **`pypdf`**: Extracts raw text from PDFs and merges watermark overlays onto pages.
- **`fpdf2`**: Generates clean output PDFs and transparent watermarks (`fill_opacity`).
- **`uharfbuzz`**: Python bindings for HarfBuzz to render complex Indic script ligatures.
- **`requests` / `deep-translator`**: Uses Google's direct JSON endpoint with `MyMemoryTranslator` fallback.
- **Bootstrap 5**: Simple, responsive UI with zero custom CSS.

### 2. Handling Bangla Unicode Text
- **Challenge**: Bengali requires glyph reordering (vowels like `ি` and `ে` render before consonants) and dynamic ligatures (যুক্তবর্ণ like `ক্ষ`, `দ্ধ`).
- **Solution**: Embedded `kalpurush.ttf` and enabled HarfBuzz shaping in `fpdf2`:
  ```python
  pdf.set_text_shaping(use_shaping_engine=True, script="beng", language="ben")
  ```

### 3. Known Limitations
- **Formatting Loss**: Extracts plain text only; original PDF fonts, colors, bold styles, images, and tables are not retained.
- **No OCR**: Does not support scanned/image-only PDFs (requires an OCR engine like Tesseract).
- **Public API Quotas**: Relies on free translation endpoints (high-volume production requires a paid Google/Azure API key).

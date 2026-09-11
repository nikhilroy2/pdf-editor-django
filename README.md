# PDF Editor & Translator (Django + REST Framework)

A web application and REST API built with Django, Django REST Framework, `fpdf2`, `pypdf`, and `uharfbuzz` for:
1. **PDF Translation**: Translates text in PDF documents between English and Bangla (বাংলা), rendering complex Bengali ligatures (যুক্তবর্ণ) using OpenType HarfBuzz shaping.
2. **PDF Watermarking**: Stamps customizable text watermarks across all pages of uploaded PDFs with configurable position, opacity, and hex color.
3. **Simple Web UI**: Clean Bootstrap 5 interfaces for both translation and watermarking.

---

## 📋 Table of Contents
- [Prerequisites](#-prerequisites)
- [Setup & Installation](#-setup--installation)
- [Running the Development Server](#-running-the-development-server)
- [Web User Interfaces](#-web-user-interfaces)
- [API Reference](#-api-reference)
  - [1. PDF Translation](#1-pdf-translation)
  - [2. PDF Watermark](#2-pdf-watermark)
- [Testing with Postman](#-testing-with-postman)
  - [Option A: One-Click Collection Import (Recommended)](#option-a-one-click-collection-import-recommended)
  - [Option B: Manual Request Setup in Postman](#option-b-manual-request-setup-in-postman)
- [Generating Test Sample PDFs](#-generating-test-sample-pdfs)
- [Troubleshooting & Tips](#-troubleshooting--tips)

---

## 🔧 Prerequisites

- **Python**: Version `3.10` or higher
- **pip**: Python package manager
- **Postman**: (Optional) For testing the REST endpoints

---

## 🚀 Setup & Installation

### 1. Clone or Open the Project
Open your terminal in the project directory:
```bash
cd c:\NIKHIL_DEV_PROJECTS\PRACTICE\pdf_editor
```

### 2. Create and Activate a Virtual Environment
- **Windows (PowerShell):**
  ```powershell
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  ```
- **Windows (Command Prompt):**
  ```cmd
  python -m venv venv
  .\venv\Scripts\activate.bat
  ```
- **macOS / Linux:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### 3. Install Dependencies
Install all required packages:
```bash
pip install django djangorestframework pypdf fpdf2 uharfbuzz deep-translator requests
```

*(Or freeze into your requirements file: `pip install -r requirements.txt`)*

> [!IMPORTANT]
> **`uharfbuzz`** is required for HarfBuzz complex text shaping so that Bengali vowels (হ্রস্ব-ই কার `ি`, একার `ে`) and joint letters (যুক্তবর্ণ) render properly without breaking.

### 4. Verify Fonts
Ensure the Bengali TrueType font is present in the `app1/fonts/` folder:
```
app1/
└── fonts/
    └── kalpurush.ttf
```

### 5. Apply Database Migrations
Run migrations to set up SQLite tables for tracking translation and watermark jobs:
```bash
python manage.py makemigrations
python manage.py migrate
```

---

## ▶️ Running the Development Server

Start the Django local development server:
```bash
python manage.py runserver
```

The server will start at: **`http://127.0.0.1:8000/`**

---

## 🌐 Web User Interfaces

Both tools have clean, Bootstrap 5 interfaces:

| Tool | URL | Description |
|---|---|---|
| **PDF Translator** | `http://127.0.0.1:8000/` | Upload a PDF, choose translation direction (EN ↔ BN), and automatically download the translated PDF. |
| **PDF Watermark** | `http://127.0.0.1:8000/watermark` | Upload a PDF, set custom text, pick from 7 positions, set opacity, pick colors, and download the stamped PDF. |

---

## 🔌 API Reference

### 1. PDF Translation
Translates text between English and Bangla and returns a new PDF.

- **URL:** `/api/translate-pdf/`
- **Method:** `POST`
- **Content-Type:** `multipart/form-data`

#### Request Parameters:
| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| `file` | File (`.pdf`) | **Yes** | — | Source PDF file to translate |
| `source_language` | String | No | `en` | Source language (`en` or `bn`) |
| `target_language` | String | No | `bn` | Target language (`bn` or `en`) |

#### Successful Response:
- **Status:** `200 OK`
- **Content-Type:** `application/pdf`
- **Body:** Binary stream of the newly translated `.pdf` file.

---

### 2. PDF Watermark
Stamps text watermarks onto all pages of the uploaded PDF with custom opacity and styling.

- **URL:** `/api/editor/pdf/watermark` *(also accessible via `/editor/pdf/watermark`)*
- **Method:** `POST`
- **Content-Type:** `multipart/form-data`

#### Request Parameters:
| Field | Type | Required | Allowed Values | Description |
|---|---|---|---|---|
| `file` | File (`.pdf`) | **Yes** | Valid `.pdf` | Source PDF document |
| `text` | String | **Yes** | Any string | Watermark text (e.g. `"CONFIDENTIAL"`, `"DRAFT"`, or `"গোপনীয়"`) |
| `position` | String | **Yes** | `top-left`, `top-center`, `top-right`, `center`, `bottom-left`, `bottom-center`, `bottom-right` | Placement on the page |
| `opacity` | Float | **Yes** | `0.0` to `1.0` (e.g. `0.25`) | Transparency level (`0.0` = invisible, `1.0` = solid) |
| `color` | String | **Yes** | Hex color (e.g. `"#FF0000"`, `"#0055FF"`) | Color of the watermark text |

#### Successful Response:
- **Status:** `200 OK`
- **Content-Type:** `application/pdf`
- **Header:** `Content-Disposition: attachment; filename="watermarked_<original_name>.pdf"`
- **Body:** Binary stream of the watermarked PDF.

---

## 📬 Testing with Postman

### Option A: One-Click Collection Import (Recommended)

A ready-to-use Postman Collection file **[`pdf_editor_postman_collection.json`](./pdf_editor_postman_collection.json)** is included in the project root.

1. Open **Postman**.
2. Click the **Import** button (top-left).
3. Drag and drop the file `pdf_editor_postman_collection.json` or browse to select it.
4. You will see a collection named **`PDF Editor & Translator API`** containing:
   - `1. Translate PDF (English to Bangla)`
   - `2. Translate PDF (Bangla to English)`
   - `3. Watermark PDF (Center Diagonal)`
   - `4. Watermark PDF (Top-Right Header)`
5. Under the **Body** tab of each request, click **Select File** for the `file` key, choose any sample `.pdf`, and click **Send**.

---

### Option B: Manual Request Setup in Postman

#### Testing Endpoint 1: PDF Translation
1. **Method:** Set to `POST`
2. **URL:** `http://127.0.0.1:8000/api/translate-pdf/`
3. **Body:**
   - Select **`form-data`**
   - Add the following keys:
     - `file`: Hover over key field, change type dropdown from **Text** to **File**, and select a PDF.
     - `source_language`: `en` (Text)
     - `target_language`: `bn` (Text)
4. **Sending & Downloading:**
   - Next to the blue **Send** button, click the small arrow dropdown and choose **"Send and Download"**.
   - Save the returned file as `translated.pdf` and open it to verify the translation.

#### Testing Endpoint 2: PDF Watermark
1. **Method:** Set to `POST`
2. **URL:** `http://127.0.0.1:8000/api/editor/pdf/watermark`
3. **Body:**
   - Select **`form-data`**
   - Add keys:
     - `file` (type: **File**): Choose your test PDF
     - `text` (type: **Text**): `CONFIDENTIAL`
     - `position` (type: **Text**): `center`
     - `opacity` (type: **Text**): `0.25`
     - `color` (type: **Text**): `#FF0000`
4. **Sending & Downloading:**
   - Click the arrow beside **Send** -> select **"Send and Download"**.
   - Save the file as `watermarked.pdf` and open it.

---

## 📄 Generating Test Sample PDFs

To generate ready-to-test sample PDFs (both English and Bangla), run:

```bash
python sample_pdf.py
```

This creates 6 sample files in the project root:
- `sample_en_technology.pdf` (English - Technology)
- `sample_en_environment.pdf` (English - Environment)
- `sample_en_education.pdf` (English - Education)
- `sample_bn_history.pdf` (Bangla - History)
- `sample_bn_tourism.pdf` (Bangla - Tourism)
- `sample_bn_science.pdf` (Bangla - Science)

Use any of these files to test translation and watermarking in Postman or via the browser UI.

---

## 🛠️ Troubleshooting & Tips

- **Bengali text looks disjointed or broken:**
  Ensure you installed `uharfbuzz`:
  ```bash
  pip install --upgrade uharfbuzz fpdf2
  ```
- **Postman response shows binary characters:**
  In Postman, use **"Send and Download"** (arrow next to Send) instead of regular "Send" so Postman saves the response as a valid `.pdf` file.
- **Path syntax errors on Windows:**
  In `models.py`, ensure file paths use `%Y/%m/%d/` and NOT `%Y/%n/%d/` (`%n` creates an illegal newline on Windows).
- **Google Translator 500 error:**
  The service uses Google's direct JSON endpoint with an automatic fallback to `MyMemoryTranslator`. Ensure your machine has an active internet connection.

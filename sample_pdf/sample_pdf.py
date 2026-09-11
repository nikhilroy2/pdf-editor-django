import os
from pathlib import Path
from fpdf import FPDF

BASE_DIR = Path(__file__).resolve().parent
FONT_PATH = BASE_DIR / 'app1' / 'fonts' / 'kalpurush.ttf'
if not FONT_PATH.exists():
    FONT_PATH = BASE_DIR / 'app1' / 'fonts' / 'Kalpurush.ttf'


def create_english_pdf(filename: str, title: str, paragraphs: list[str]):
    """Generates an English sample PDF."""
    pdf = FPDF()
    pdf.add_page()

    # Title
    pdf.set_font("Helvetica", style="B", size=16)
    pdf.cell(0, 10, text=title, align="C")
    pdf.ln(12)

    # Paragraphs
    pdf.set_font("Helvetica", size=12)
    for para in paragraphs:
        pdf.multi_cell(0, 7.5, text=para)
        pdf.ln(5)

    pdf.output(filename)
    print(f"[+] Created: {filename}")


def create_bangla_pdf(filename: str, title: str, paragraphs: list[str]):
    """Generates a Bangla sample PDF with HarfBuzz complex text shaping."""
    pdf = FPDF()
    # Enable Bengali text shaping
    pdf.set_text_shaping(use_shaping_engine=True, script="beng", language="ben")
    pdf.add_font("BanglaFont", fname=str(FONT_PATH))
    pdf.add_page()

    # Title
    pdf.set_font("BanglaFont", size=16)
    pdf.cell(0, 10, text=title, align="C")
    pdf.ln(12)

    # Paragraphs
    pdf.set_font("BanglaFont", size=12)
    for para in paragraphs:
        pdf.multi_cell(0, 7.5, text=para)
        pdf.ln(5)

    pdf.output(filename)
    print(f"[+] Created: {filename}")


def generate_all_samples():
    print("Generating sample PDFs for testing...\n")

    # ==============================================================
    # 3 English PDFs (for testing English -> Bangla translation)
    # ==============================================================

    # 1. Technology & AI
    create_english_pdf(
        filename="sample_en_technology.pdf",
        title="The Future of Artificial Intelligence",
        paragraphs=[
            "Artificial intelligence is rapidly reshaping industries across the globe. From automated healthcare diagnosis to smart transportation systems, intelligent algorithms are solving complex challenges with remarkable speed and accuracy.",
            "Machine learning models can process vast amounts of unstructured data, allowing researchers to discover new scientific insights and create tools that enhance human productivity in ways never seen before.",
            "As these technologies continue to advance, ensuring ethical implementation and transparent decision-making will remain critical for building trust among society."
        ]
    )

    # 2. Climate & Nature
    create_english_pdf(
        filename="sample_en_environment.pdf",
        title="Preserving Global Water Resources",
        paragraphs=[
            "Freshwater is one of the most vital natural resources supporting life and agriculture on our planet. Growing populations and changing global weather patterns are placing unprecedented pressure on lakes, rivers, and underground aquifers.",
            "Sustainable water conservation requires efficient irrigation practices, active restoration of natural wetlands, and widespread adoption of modern recycling technologies.",
            "Communities around the world must collaborate to safeguard water security for future generations."
        ]
    )

    # 3. Education & Innovation
    create_english_pdf(
        filename="sample_en_education.pdf",
        title="Modern Digital Education",
        paragraphs=[
            "Online learning platforms and interactive classrooms have revolutionized access to knowledge. Students from remote regions can now learn from world-renowned educators through digital devices connected to the internet.",
            "Personalized learning tools analyze student performance in real time, adapting lesson plans to meet individual needs and ensuring that no learner is left behind.",
            "Investments in digital infrastructure and digital literacy are essential steps toward building an equitable educational ecosystem."
        ]
    )

    # ==============================================================
    # 3 Bangla PDFs (for testing Bangla -> English translation)
    # ==============================================================

    # 1. History & Culture (ইতিহাস ও সংস্কৃতি)
    create_bangla_pdf(
        filename="sample_bn_history.pdf",
        title="বাংলাদেশের সমৃদ্ধ ইতিহাস ও সংস্কৃতি",
        paragraphs=[
            "বাংলাদেশ দক্ষিণ এশিয়ার একটি অনন্য সুন্দর দেশ যা সমৃদ্ধ সাংস্কৃতিক ঐতিহ্য এবং গৌরবময় ইতিহাসে ভরপুর। ১৯৭১ সালের মহান মুক্তিযুদ্ধের মাধ্যমে বীর বাঙালিরা স্বাধীনতার রক্তিম সূর্য ছিনিয়ে এনেছিল।",
            "বাংলা ভাষা আন্দোলন আমাদের জাতীয় চেতনার মূল ভিত্তি। ১৯৫২ সালের একুশে ফেব্রুয়ারি মাতৃভাষার জন্য আত্মত্যাগের স্মৃতি আজ আন্তর্জাতিক মাতৃভাষা দিবস হিসেবে বিশ্বজুড়ে পালিত হয়।",
            "এদেশের ঐতিহ্যবাহী লোকশিল্প, বাউল গান এবং উৎসবমুখর সামাজিক পরিবেশ মানুষের পারস্পরিক ভ্রাতৃত্ব ও সৌহার্দ্যকে দৃঢ় করে।"
        ]
    )

    # 2. Tourism & Sundarbans (সুন্দরবন ও পর্যটন)
    create_bangla_pdf(
        filename="sample_bn_tourism.pdf",
        title="সুন্দরবন: পৃথিবীর বৃহত্তম ম্যানগ্রোভ বন",
        paragraphs=[
            "সুন্দরবন বাংলাদেশের দক্ষিণ-পশ্চিমাঞ্চলে অবস্থিত একটি বিশ্ব ঐতিহ্যবাহী স্থান। এটি পৃথিবীর বৃহত্তম অবিচ্ছিন্ন জোয়ার-ভাটার ম্যানগ্রোভ বনভূমি হিসেবে পরিচিত।",
            "এই গহিন অরণ্য রয়েল বেঙ্গল টাইগারের প্রাকৃতিক আবাসস্থল। তাছাড়া হরিণ, লবণাক্ত জলের কুমির এবং বহু প্রজাতির বিরল পাখি এই বনাঞ্চলে বাস করে।",
            "উপকূলীয় পরিবেশের ভারসাম্য রক্ষা এবং প্রাকৃতিক দুর্যোগ থেকে উপকূলবাসীকে সুরক্ষিত রাখতে সুন্দরবন এক প্রাকৃতিক প্রাচীর হিসেবে কাজ করে।"
        ]
    )

    # 3. Science & Daily Life (বিজ্ঞান ও প্রযুক্তি)
    create_bangla_pdf(
        filename="sample_bn_science.pdf",
        title="দৈনন্দিন জীবনে বিজ্ঞানের ভূমিকা",
        paragraphs=[
            "আধুনিক যুগে বিজ্ঞান ও প্রযুক্তি মানবজীবনের প্রতিটি ক্ষেত্রে গভীর পরিবর্তন এনেছে। চিকিৎসা, যোগাযোগ এবং শিক্ষার ক্ষেত্রে নতুন উদ্ভাবন মানুষের জীবনকে আগের চেয়ে অনেক সহজ ও গতিশীল করেছে।",
            "স্মার্টফোন এবং ইন্টারনেট সংযোগের মাধ্যমে বিশ্বের যেকোনো প্রান্তের খবর মুহূর্তের মধ্যে আমাদের হাতের মুঠোয় পৌঁছে যাচ্ছে। ডিজিটাল ব্যাংকিং অর্থনৈতিক লেনদেনকে করেছে দ্রুত ও নিরাপদ।",
            "ভবিষ্যত প্রজন্মের জন্য টেকসই ও নিরাপদ পৃথিবী গড়তে পরিবেশবান্ধব সবুজ প্রযুক্তির প্রসার বৃদ্ধি করা অত্যন্ত জরুরি।"
        ]
    )

    print("\nAll 6 test PDFs generated successfully!")


if __name__ == "__main__":
    generate_all_samples()

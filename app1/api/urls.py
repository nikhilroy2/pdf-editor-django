from django.urls import path
from . import views
from .views import TranslatePDFView, PDFWatermarkView
urlpatterns = [
    path('translate-pdf/', TranslatePDFView.as_view(), name="translate_pdf"),
    path('editor/pdf/watermark', PDFWatermarkView.as_view(), name="pdf_watermark"),
]
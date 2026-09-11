from django.urls import path
from . import views
from .views import TranslatePDFView
urlpatterns = [
    path('translate-pdf/', TranslatePDFView.as_view(), name="translate_pdf"),
]
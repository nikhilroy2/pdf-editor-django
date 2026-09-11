from django.urls import path
from . import views
urlpatterns = [
    path('translate-pdf', views.TranslatePDF, name="translate_pdf")
]
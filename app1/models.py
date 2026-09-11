from django.db import models
import uuid

# Create your models here.

class PDFTranslation(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        PROCESSING = 'PROCESSING', 'Processing'
        COMPLETED = 'COMPLETED', 'Completed'
        FAILED = 'FAILED', 'Failed'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    original_file = models.FileField(
        upload_to='pdfs/original/%Y/%m/%d/',
        help_text="The source PDF uploaded by the user"
    )
    translated_file = models.FileField(
        upload_to='pdfs/translated/%Y/%m/%d/',
        blank=True,
        null=True,
        help_text="The newly generated translated PDF"
    )

    source_language = models.CharField(max_length=10, default="en")
    target_language = models.CharField(max_length=10, default="bn")

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    error_message = models.TextField(blank=True, null=True)

    extracted_text = models.TextField(blank=True, null=True)
    translated_text = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "PDF translation"
        verbose_name_plural = 'PDF Translations'
    def __str__(self):
        return f"{self.id} | {self.source_language} -> {self.target_language}"
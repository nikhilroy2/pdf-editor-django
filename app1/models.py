from django.db import models
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator
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



class PDFWatermark(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        PROCESSING = 'PROCESSING', 'Processing'
        COMPLETED = 'COMPLETED', 'Completed'
        FAILED = 'FAILED', 'Failed'
    class Position(models.TextChoices):
        TOP_LEFT = 'top-left', 'Top Left'
        TOP_CENTER = 'top-center', 'Top Center'
        TOP_RIGHT = 'top-right', 'Top Right'
        CENTER = 'center', 'Center'
        BOTTOM_LEFT = 'bottom-left', 'Bottom Left'
        BOTTOM_CENTER = 'bottom-center', 'Bottom Center'
        BOTTOM_RIGHT = 'bottom-right', 'Bottom Right'
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # 1. Source and Output Files
    original_file = models.FileField(
        upload_to='pdfs/watermark/original/%Y/%m/%d/',
        help_text="Source PDF uploaded by user"
    )
    watermarked_file = models.FileField(
        upload_to='pdfs/watermark/output/%Y/%m/%d/',
        blank=True,
        null=True,
        help_text="Newly generated watermarked PDF"
    )
    # 2. Watermark Style & Configuration Options
    text = models.CharField(
        max_length=255,
        help_text='Watermark text, e.g. "CONFIDENTIAL"'
    )
    position = models.CharField(
        max_length=20,
        choices=Position.choices,
        default=Position.CENTER,
        help_text="Position on page"
    )
    opacity = models.FloatField(
        default=0.25,
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        help_text="Opacity between 0.0 and 1.0"
    )
    color = models.CharField(
        max_length=7,
        default='#FF0000',
        help_text='Hex color, e.g. "#FF0000"'
    )
    # 3. Processing Status & Diagnostics
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    error_message = models.TextField(blank=True, null=True)
    # 4. Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ["-created_at"]
        verbose_name = "PDF Watermark"
        verbose_name_plural = "PDF Watermarks"
    def __str__(self):
        return f"{self.id} | {self.text} ({self.position})"
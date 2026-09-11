from django.core.files.base import ContentFile
from django.http import HttpResponse
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView

from app1.models import PDFTranslation
from app1.services.pdf_service import PDFTranslationService
from .serializers import PDFTranslationSerializer


class TranslatePDFView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        # 1. Validate incoming multipart request
        serializer = PDFTranslationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        uploaded_file = serializer.validated_data['file']
        source_lang = serializer.validated_data['source_language'].strip().lower()
        target_lang = serializer.validated_data['target_language'].strip().lower()

        # 2. Create initial database tracking record
        translation_record = PDFTranslation.objects.create(
            original_file=uploaded_file,
            source_language=source_lang,
            target_language=target_lang,
            status=PDFTranslation.Status.PROCESSING
        )

        try:
            # 3. Extract text from uploaded PDF
            extracted_text = PDFTranslationService.extract_text(uploaded_file)
            if not extracted_text.strip():
                translation_record.status = PDFTranslation.Status.FAILED
                translation_record.error_message = "No readable text found. (Scanned image PDFs require OCR)."
                translation_record.save()
                return Response(
                    {"error": "No readable text found in PDF. Note: scanned/image PDFs require OCR."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            translation_record.extracted_text = extracted_text

            # 4. Translate text
            translated_text = PDFTranslationService.translate_text(
                text=extracted_text,
                source_lang=source_lang,
                target_lang=target_lang
            )
            translation_record.translated_text = translated_text

            # 5. Generate newly translated PDF
            pdf_bytes = PDFTranslationService.generate_pdf(
                text=translated_text,
                target_lang=target_lang
            )

            # 6. Save translated PDF file into database record
            filename = f"translated_{target_lang}_{uploaded_file.name}"
            translation_record.translated_file.save(filename, ContentFile(pdf_bytes), save=False)
            translation_record.status = PDFTranslation.Status.COMPLETED
            translation_record.save()

            # 7. Return the new PDF as a downloadable attachment
            response = HttpResponse(pdf_bytes, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            response['X-Translation-Id'] = str(translation_record.id)
            return response

        except Exception as e:
            translation_record.status = PDFTranslation.Status.FAILED
            translation_record.error_message = str(e)
            translation_record.save()
            return Response(
                {"error": f"Failed to translate PDF: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

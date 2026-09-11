from rest_framework import serializers


class PDFTranslationSerializer(serializers.Serializer):
    file = serializers.FileField(required=True)
    source_language = serializers.CharField(max_length=10, required=False, default='en')
    target_language = serializers.CharField(max_length=10, required=False, default='bn')

    def validate_file(self, value):
        # Ensure the uploaded file has a .pdf extension
        if not value.name.lower().endswith('.pdf'):
            raise serializers.ValidationError("Only PDF files (.pdf) are supported.")
        return value




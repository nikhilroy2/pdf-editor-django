import re
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



POSITION_CHOICES = [
    'top-left', 'top-center', 'top-right',
    'center',
    'bottom-left', 'bottom-center', 'bottom-right'
]



class PDFWatermarkSerializer(serializers.Serializer):
    file = serializers.FileField(required=True)
    text = serializers.CharField(max_length=255, required=True)
    position = serializers.ChoiceField(choices=POSITION_CHOICES, default='center')
    opacity = serializers.FloatField(min_value=0.0, max_value=1.0, default=0.25)
    color = serializers.CharField(max_length=7, default='#FF0000')
    def validate_file(self, value):
        if not value.name.lower().endswith('.pdf'):
            raise serializers.ValidationError("Only PDF files (.pdf) are supported.")
        return value
    def validate_color(self, value):
        # Validate hex color (#RGB or #RRGGBB)
        if not re.match(r'^#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})$', value):
            raise serializers.ValidationError('Color must be a valid hex code (e.g. "#FF0000" or "#F00").')
        return value
from rest_framework import serializers
from .models import Camera, Recording

class RecordingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recording
        fields = '__all__'

class CameraSerializer(serializers.ModelSerializer):
    recordings = RecordingSerializer(many=True, read_only=True)

    class Meta:
        model = Camera
        fields = '__all__'

from django.contrib import admin
from .models import Camera, Recording

@admin.register(Camera)
class CameraAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'url')
    search_fields = ('name',)

@admin.register(Recording)
class RecordingAdmin(admin.ModelAdmin):
    list_display = ('camera', 'start_time', 'end_time', 'recording_url')
    list_filter = ('camera', 'start_time', 'end_time')
    search_fields = ('camera__name',)

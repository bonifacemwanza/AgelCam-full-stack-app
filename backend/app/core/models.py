from django.db import models

class Camera(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    url = models.URLField()

    def __str__(self):
        return self.name

class Recording(models.Model):
    camera = models.ForeignKey(Camera, related_name='recordings', on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    recording_url = models.URLField()

    def __str__(self):
        return f"Recording for {self.camera.name} from {self.start_time} to {self.end_time}"

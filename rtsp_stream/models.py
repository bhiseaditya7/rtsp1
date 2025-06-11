from django.db import models
import uuid
# Create your models here.
class Streams(models.Model):
    streamid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    stream_url = models.URLField()
    stream_name = models.CharField(max_length=20,null=True)
    # stream_description = models.CharField(max_length=250, null=True)
    face_detection_flag = models.BooleanField(default=False)
    # confidence_threshold= models.FloatField()

class Detection(models.Model):
    detection_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    detect_timestamp = models.DateTimeField(null=True, blank=True)
    stream_ref = models.URLField(null=True, blank=True)
    confidence_score = models.FloatField(null=True, blank=True)
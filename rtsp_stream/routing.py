from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/metadata/$', consumers.FFmpegMetadataConsumer.as_asgi()),
    re_path(r'ws/faces/$', consumers.FaceMetadataConsumer1.as_asgi()),
    # re_path(r'ws/faces/(?P<stream_id>\w+)/$', consumers.FaceMetadataConsumer1.as_asgi()),
]


from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/metadata/$', consumers.FFmpegMetadataConsumer.as_asgi()),
    re_path(r'ws/faces/$', consumers.FaceMetadataConsumer.as_asgi()),
]

# websocket_urlpatterns = [
#     re_path(r"ws/metadata/$", consumers.FaceMetadataConsumer.as_asgi()),
# ]
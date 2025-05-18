# """
# ASGI config for project_stream project.

# It exposes the ASGI callable as a module-level variable named ``application``.

# For more information on this file, see
# https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
# """

# import os

# from django.core.asgi import get_asgi_application
# from channels.routing import ProtocolTypeRouter, URLRouter
# from django.urls import path
# from rtsp_stream.consumers import TestConsumer

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_stream.settings')

# #application = get_asgi_application()

# ws_patters=[
#     path('ws/test/', TestConsumer)
# ]

# application = ProtocolTypeRouter({
#     'websocket': URLRouter(ws_patters)
# })



import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
import rtsp_stream.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_stream.settings')

import os
import shutil
from pathlib import Path

# Clear ffmpeg_outputs directory at startup
def clear_ffmpeg_outputs():
    output_dir = Path(__file__).resolve().parent.parent / 'ffmpeg_outputs'
    if output_dir.exists():
        shutil.rmtree(output_dir)
        output_dir.mkdir()

clear_ffmpeg_outputs()

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            rtsp_stream.routing.websocket_urlpatterns
        )
    ),
})
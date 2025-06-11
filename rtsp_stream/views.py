from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import subprocess
import os
import uuid
from rest_framework.response import Response
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
# Create your views here.
from .serializers import UserRegistrationSerializer, SignInSerializer
from rest_framework import status,viewsets
from rest_framework import permissions
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication

import cv2
from mtcnn_cv2 import MTCNN
import threading
import asyncio
import websockets
import json

import os
import sys

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from .models import Streams,Detection
from .serializers import StreamSerializer
from datetime import datetime



os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;tcp"
=======
#         return Response({
#             "message": "Streaming started",
#             "hls_url": f"https://rtsp1.onrender.com/ffmpeg_outputs/index.m3u8"
#         })



class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]
    # parser_classes =[]

    @method_decorator(ratelimit(key='ip', rate='5/m', method='POST', block=True))

    def post(self, request):
        # validate and de-serialize incoming user data
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            # Save user instance to the database
            serializer.save()
            return Response({"message": "User Registered Successfully"}, status=status.HTTP_201_CREATED)
        # if serializer is invalid, return validation errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class SignInView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = SignInSerializer(data= request.data, context={'request':request})

        if serializer.is_valid():
            user = serializer.validated_data

            refresh = RefreshToken.for_user(user)
            return Response(
                {'refresh':str(refresh), 'access':str(refresh.access_token)}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StartStreamView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.face_flag = False
        self.stream_obj = None

        self.detect_obj=None

    def post(self, request):
        rtsp_url = request.data.get("rtsp_url")
        print("RTSP URL received:", rtsp_url)
        name =  rtsp_url.rsplit('/', 1)[1]

        if not rtsp_url:
            return Response({"error": "No RTSP URL provided"}, status=status.HTTP_400_BAD_REQUEST)

        stream_id = str(uuid.uuid4())[:8]
        output_dir = f"./ffmpeg_outputs"
        # output_dir = f"./ffmpeg_outputs/{stream_id}"
        os.makedirs(output_dir, exist_ok=True)

        output_path = f"{output_dir}/index.m3u8"

        command = [
            "/usr/bin/ffmpeg",
            "-rtsp_transport", "tcp",
            "-i", rtsp_url,
            "-fflags", "flush_packets",
            "-max_delay", "2",
            "-flags", "+global_header",
            "-hls_time", "2",
            "-hls_list_size", "3",
            "-vcodec", "copy",
            "-y", output_path
        ]

        subprocess.Popen(command)
        print("[FFMPEG] Streaming command started for:", stream_id)

        # Create DB entry now (we'll update face flag later)
        self.stream_obj = Streams.objects.create(stream_url=rtsp_url,stream_name=name)
        self.detect_obj = Detection.objects.create(stream_ref = rtsp_url)

        # Start face detection thread
        try:
            threading.Thread(target=self.run_mtcnn, args=(rtsp_url,), daemon=True).start()
            print("[Thread] MTCNN face detection started.")
        except Exception as e:
            print("[Thread ERROR] Failed to start MTCNN thread:", e)

        return Response({
            "message": "Streaming started",
            "stream_id": stream_id,
            # "hls_url": f"http://127.0.0.1:8000/ffmpeg_outputs/{stream_id}/index.m3u8",
            "hls_url": f"https://rtsp1.onrender.com/ffmpeg_outputs/index.m3u8",
            # "ws_url": f"ws://127.0.0.1:8000/ws/faces/1"
            "ws_url": f"wss://rtsp1.onrender.com/ws/faces/1"
            
        })

    def run_mtcnn(self, rtsp_url):
        print("[MTCNN] Starting face detection for:", rtsp_url)
        cap = cv2.VideoCapture(rtsp_url, cv2.CAP_FFMPEG)
        detector = MTCNN()
        channel_layer = get_channel_layer()

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("[MTCNN] Frame read failed.")
                break

            results = detector.detect_faces(frame)
            face_data = []

            for face in results:
                x, y, w, h = face['box']
                face_data.append({
                    'x': x,
                    'y': y,
                    'width': w,
                    'height': h,
                    'confidence': face['confidence']
                })

            #Only update database once when a face is confidently detected
            if not self.face_flag and any(item['confidence'] > 0.8 for item in face_data):
                self.face_flag = True
                a = any(item['confidence'] > 0.8 for item in face_data)
                # a=0.9
                timestamp=datetime.now()

                print("[MTCNN] High-confidence face detected!")
                if self.stream_obj:
                    self.stream_obj.face_detection_flag = True
                    self.stream_obj.save()
                if self.detect_obj:
                    self.detect_obj.detect_timestamp = timestamp
                    self.detect_obj.confidence_score = a
                    self.detect_obj.save()

            #Continue sending face data to WebSocket
            if channel_layer:
                try:
                    async_to_sync(channel_layer.group_send)(
                        "face_group",  # make this dynamic if needed
                        {
                            "type": "send_face_data",
                            "data": face_data,
                            "frame_width": frame.shape[1],
                            "frame_height": frame.shape[0]
                        }
                    )
                except Exception as e:
                    print("[WebSocket ERROR]:", e)

        cap.release()
        print("[MTCNN] Video stream ended.")

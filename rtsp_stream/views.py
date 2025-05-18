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

class StartStreamView(APIView):
    def post(self, request):
        rtsp_url = request.data.get("rtsp_url")
        if not rtsp_url:
            return Response({"error": "No RTSP URL provided"}, status=400)

        # stream_id = str(uuid.uuid4())[:8]
        output_dir = f"./ffmpeg_outputs"
        os.makedirs(output_dir, exist_ok=True)

        output_path = f"{output_dir}/index.m3u8"
#ffmpeg -i rtsp://localhost:8554/live.stream -fflags flush_packets -max_delay 2 -flags +global_header -hls_time 2 -hls_list_size 3 -vcodec copy -y ./index.m3u8

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

        return Response({
            "message": "Streaming started",
            "hls_url": f"http://localhost:8000/ffmpeg_outputs/index.m3u8"
        })


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


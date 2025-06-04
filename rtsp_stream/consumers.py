import asyncio
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class FFmpegMetadataConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        # self.process = await asyncio.create_subprocess_exec(
        #     '/usr/bin/ffmpeg',
        #     '-i', 'rtsp://172.26.48.1:8554/live.stream',  # or replace dynamically
        #     '-an', '-vf', 'fps=10', '-f', 'null', '-',
        #     stderr=asyncio.subprocess.PIPE
        # )
        #newly added
        self.process = await asyncio.create_subprocess_exec(
            '/usr/bin/ffmpeg',
            '-i', 'rtsp://13.203.201.207:8554/mystream1',  # or replace dynamically
            '-an', '-vf', 'fps=10', '-f', 'null', '-',
            stderr=asyncio.subprocess.PIPE
        )
        await self.accept()    #newly added
        await self.send(json.dumps({"status": "Connected to FFmpeg Metadata WebSocket"})) #newly added
        asyncio.create_task(self.stream_metadata())

    async def disconnect(self, close_code):
        if hasattr(self, 'process'):
            self.process.kill()

    async def stream_metadata(self):
        while True:
            line = await self.process.stderr.readline()
            if not line:
                break
            line = line.decode('utf-8')

            await self.send(json.dumps({"ffmpeg_log": line}))#newly added
            
            if "frame=" in line:
                meta = self.parse_line(line)
                if meta:
                    await self.send(json.dumps(meta))

    def parse_line(self, line):
        parts = line.strip().split()
        return {k: v for part in parts if '=' in part for k, v in [part.split('=', 1)]} 
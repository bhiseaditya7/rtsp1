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

            '-i', 'rtsp://admin:admin123@49.248.155.178:555/cam/realmonitor?channel=1&subtype=0',  # or replace dynamically
            '-an', '-vf', 'fps=10', '-f', 'null', '-',
            stderr=asyncio.subprocess.PIPE
        )
        await self.send(text_data=json.dumps({'status':'connected12'}))

#             '-i', 'rtsp://13.203.201.207:8554/mystream1',  # or replace dynamically
#             '-an', '-vf', 'fps=10', '-f', 'null', '-',
#             stderr=asyncio.subprocess.PIPE
#         )
#         await self.accept()    #newly added
#         await self.send(json.dumps({"status": "Connected to FFmpeg Metadata WebSocket"})) #newly added

        asyncio.create_task(self.stream_metadata())
        await self.send(text_data=json.dumps({'status':'connected15'}))

    async def disconnect(self, close_code):
        if hasattr(self, 'process'):
            self.process.kill()

    async def stream_metadata(self):
        while True:
            line = await self.process.stderr.readline()
            print("1212121212121212")
            if not line:
                break
            line = line.decode('utf-8')

            await self.send(json.dumps({"ffmpeg_log": line}))#newly added
            
            if "frame=" in line:
                meta = self.parse_line(line)
                if meta:
                    await self.send(text_data=json.dumps({'status':'connecte'}))
                    await self.send(json.dumps(meta))

    def parse_line(self, line):
        parts = line.strip().split()
        return {k: v for part in parts if '=' in part for k, v in [part.split('=', 1)]} 
    

class FaceMetadataConsumer1(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("face_group", self.channel_name)
        await self.accept()
        await self.send(text_data=json.dumps({'status':'connected11'}))

        # await self.send(text_data=json.dumps({
        #     "type": "faces",
        #     "data": event["data"]
        # }))
        # await self.send(text_data=json.dumps(text_data))
        # self.stream_id = self.scope["url_route"]["kwargs"]["stream_id"]
        # self.group_name = f"face_group_{self.stream_id}"

        # await self.channel_layer.group_add(self.group_name, self.channel_name)
        # await self.accept()
        # await self.send(text_data=json.dumps({'status': f'connected to {self.group_name}'}))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("face_group", self.channel_name)
        await self.send(text_data=json.dumps({'status':'disonnected'}))

    async def receive(self, text_data):
        # optional: receive from frontend if needed
        print("Received from frontend:", text_data)

    async def send_face_data(self, event):
        await self.send(text_data=json.dumps({
            "type": "facess",
            "data": event["data"],
            "frame_width": event["frame_width"],
            "frame_height": event["frame_height"]
            # "confindence1": event["confidence"]
        }))
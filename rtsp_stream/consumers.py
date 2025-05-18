# from channels.generic.websocket import WebsocketConsumer
# from asgiref.sync import async_to_sync
# import json

# class TestConsumer(WebsocketConsumer):

#     # def connect(self):
#     #     self.room_name ="test_connection"
#     #     self.room_group_name = "test_consumer_group"
#     #     async_to_sync(self.channel_layer.group_add)(
#     #         self.room_name, self.room_group_name
#     #     )
#     #     self.accept()
#     #     self.send(text_data=json.dumps({'status': 'sonnection sent'}))

#     def connect(self):
#         self.room_group_name = "test_consumer_group"

#         # Join group
#         async_to_sync(self.channel_layer.group_add)(
#             self.room_group_name,
#             self.channel_name
#         )

#         self.accept()
#         self.send(text_data=json.dumps({'status': 'connection sent'}))

#     def receive(self):
#         pass

#     def disconnect(self, code):
#         pass
#         #return super().disconnect(code)

# from channels.generic.websocket import AsyncWebsocketConsumer
# import json

# class TestConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()
#         await self.send(text_data=json.dumps({'message': ' new Connected'}))

#     async def disconnect(self, *args, **kwargs):
#         print("disconneted")
        

#     async def receive(self, text_data):
#         print(text_data)
#         self.send(text_data=json.dumps({'message': ' message received'}))
        
#         # data = json.loads(text_data)
#         # message = data.get('message', '')
#         # await self.send(text_data=json.dumps({'reply': f"Echo: {message}"}))

# class TestConsumer1(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()
#         await self.send(text_data=json.dumps({'message': ' new Connected'}))

#     async def disconnect(self, *args, **kwargs):
#         print("disconneted")
        

#     async def receive(self, text_data):
#         print(text_data)
#         self.send(text_data=json.dumps({'message': ' message received'}))



# import asyncio
# import json
# import subprocess
# from channels.generic.websocket import AsyncWebsocketConsumer

# class FFmpegMetadataConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()
#         await self.send(text_data=json.dumps({'message': ' new Connected11'}))
#         # self.process = await asyncio.create_subprocess_exec(
#         #     'ffmpeg',
#         #     '-i', 'http://pendelcam.kip.uni-heidelberg.de/mjpg/video.mjpg',
#         #     '-an',
#         #     '-vf', 'fps=30',
#         #     '-f', 'mp4',
#         #     'output.mp4',
#         #     stderr=asyncio.subprocess.PIPE
#         # )
#         self.process = await asyncio.create_subprocess_exec(
#             '/usr/bin/ffmpeg',  # <-- replace this with the full path to ffmpeg
#             '-i', 'http://pendelcam.kip.uni-heidelberg.de/mjpg/video.mjpg',
#             '-an',
#             '-vf', 'fps=30',
#             '-f', 'mp4',
#             'output.mp4',
#             stderr=asyncio.subprocess.PIPE
#         )
#         # y
#         asyncio.create_task(self.stream_metadata())

#     async def disconnect(self, close_code):
#         if self.process:
#             self.process.kill()

#     async def stream_metadata(self):
#         while True:
#             line = await self.process.stderr.readline()
#             if not line:
#                 break
#             line = line.decode('utf-8')
#             print("RAW LINE:", line)
#             if "frame=" in line:
#                 # Extract frame metadata
#                 data = self.parse_line(line)
#                 if data:
#                     await self.send(json.dumps(data))

#     def parse_line(self, line):
#         parts = line.strip().split()
#         meta = {}
#         for part in parts:
#             if '=' in part:
#                 k, v = part.split('=', 1)
#                 meta[k] = v
#         print("meta data is:",meta)
#         return meta


# import asyncio
# import json
# from channels.generic.websocket import AsyncWebsocketConsumer

# class FFmpegMetadataConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()
#         self.process = await asyncio.create_subprocess_exec(
#             '/usr/bin/ffmpeg',
#             '-i', 'http://webcam.mchcares.com/mjpg/video.mjpg?timestamp=1566232173730',
#             '-an',
#             '-vf', 'fps=10',
#             '-f', 'null',
#             '-',
#             stderr=asyncio.subprocess.PIPE
#         )
#         asyncio.create_task(self.stream_metadata())

#     async def disconnect(self, close_code):
#         if self.process:
#             self.process.kill()

#     async def stream_metadata(self):
#         while True:
#             line = await self.process.stderr.readline()
#             if not line:
#                 break
#             line = line.decode('utf-8')
#             print("so line are",line)
#             if "frame=" in line:
#                 meta = self.parse_line(line)
#                 if meta:
#                     await self.send(json.dumps(meta))

#     def parse_line(self, line):
#         parts = line.strip().split()
#         meta = {}
#         for part in parts:
#             if '=' in part:
#                 k, v = part.split('=', 1)
#                 meta[k] = v
#         print("meta data is: ", meta)
#         return meta

# consumers.py
# import asyncio
# import json
# from channels.generic.websocket import AsyncWebsocketConsumer

# class FFmpegMetadataConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()

#         self.process = await asyncio.create_subprocess_exec(
#             '/usr/bin/ffmpeg',  # Use full path if needed, e.g. '/usr/bin/ffmpeg'
#             '-rtsp_transport', 'tcp',
#             '-i', 'rtsp://localhost:8554/live.stream',
#             '-an',
#             '-vf', 'fps=10',
#             '-f', 'null',
#             '-',
#             stderr=asyncio.subprocess.PIPE
#         )

#         asyncio.create_task(self.stream_metadata())

#     async def disconnect(self, close_code):
#         if hasattr(self, 'process') and self.process:
#             self.process.kill()

#     async def stream_metadata(self):
#         while True:
#             line = await self.process.stderr.readline()
#             if not line:
#                 break
#             line = line.decode('utf-8')
#             print("line is :", line)
#             if "frame=" in line:
#                 meta = self.parse_line(line)
#                 if meta:
#                     await self.send(json.dumps(meta))


#     def parse_line(self, line):
#         parts = line.strip().split()
#         meta = {}
#         for part in parts:
#             if '=' in part:
#                 k, v = part.split('=', 1)
#                 meta[k] = v
#         return meta

import asyncio
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class FFmpegMetadataConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.process = await asyncio.create_subprocess_exec(
            '/usr/bin/ffmpeg',
            '-i', 'rtsp://172.26.48.1:8554/live.stream',  # or replace dynamically
            '-an', '-vf', 'fps=10', '-f', 'null', '-',
            stderr=asyncio.subprocess.PIPE
        )
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
            
            if "frame=" in line:
                meta = self.parse_line(line)
                if meta:
                    await self.send(json.dumps(meta))

    def parse_line(self, line):
        parts = line.strip().split()
        return {k: v for part in parts if '=' in part for k, v in [part.split('=', 1)]} 
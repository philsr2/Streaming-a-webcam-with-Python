# version 0.1
#
import cv2
import asyncio
import websockets
import time

vid = cv2.VideoCapture(0)
count = 0

async def send_frames():
    global count
    #
    # change the uri to where you'll run server.py
    #
    uri = "ws://localhost:5000"

    async with websockets.connect(uri) as websocket:
        while True:
            start = time.time()
            ret, frame = vid.read()
            if not ret:
                print("camera error")
                break
            _, jpg = cv2.imencode(".jpg",frame,[cv2.IMWRITE_JPEG_QUALITY, 25])
            await websocket.send(jpg.tobytes())
            print("sent frame", count)
            count += 1
            # throttle to ~30 FPS
            elapsed = time.time() - start
            await asyncio.sleep(max(0, (1/30) - elapsed))
#
asyncio.run(send_frames())

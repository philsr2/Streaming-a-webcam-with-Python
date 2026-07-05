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
            #
            # added this line to downsize my frames
            # thinking of putting multiple cameras on one page
            #
            # frame2=cv2.resize(frame,(320,240),interpolation=cv2.INTER_AREA)
            
            if not ret:
                print("camera error")
                break
            _, jpg = cv2.imencode(".jpg",frame,[cv2.IMWRITE_JPEG_QUALITY, 25])
            # 
            # with a reduced image size, increasing the quality up to 50 didn't change
            # the bandwidth much - cpu usage on my old 8 core machine stayed about 20%
            #
            #  _, jpg = cv2.imencode(".jpg",frame,[cv2.IMWRITE_JPEG_QUALITY, 50])
            
            await websocket.send(jpg.tobytes())
            print("sent frame", count)
            count += 1
            # throttle to ~30 FPS
            elapsed = time.time() - start
            await asyncio.sleep(max(0, (1/30) - elapsed))
#
asyncio.run(send_frames())

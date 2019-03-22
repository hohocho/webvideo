import asyncio

import cv2


class Webcam:
    def __init__(self, webcamId=0):
        self.webcam = cv2.VideoCapture(webcamId)
        self.webcam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.webcam.set(cv2.CAP_PROP_FRAME_WIDTH, 960)

    async def frames(self):

        while True:
            ret, img = self.webcam.read()

            yield cv2.imencode('.jpg', img)[1].tobytes()
            await asyncio.sleep(0.001)

    async def stream(self, rsp):
        async for frame in self.frames():
            await rsp.write(
                b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'
            )


def findWebcam():
    count = 0
    for i in range(5):
        cap = cv2.VideoCapture(i)
        ret = cap.isOpened()
        if ret:
            count += 1
            cap.release()
        else:
            break

    return count

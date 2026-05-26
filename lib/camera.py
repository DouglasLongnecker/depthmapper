import cv2
from threading import Lock, Thread

class Camera:
    def __init__(self, pipeline, id):
        self.camera = cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER)
        self.lock = Lock()
        self.grabbed = False
        self.frame = None
        self.stopped = False

        # Start thread for frame capture
        self.thread = Thread(target=self.thread, name='video ' + str(id), args=())
        self.thread.daemon = True
        self.thread.start()

    def isOpened(self):
        return self.camera.isOpened()

    def stop(self):
        self.stopped = True
        self.thread.join()

    def read(self):
        with self.lock:
            if not self.grabbed or self.frame is None or self.frame.size == 0:
                return (False, None)

            return (True, self.frame.copy())

    def thread(self):
        while self.stopped == False:
            grabbed, frame = self.camera.read()
            with self.lock:
                self.grabbed = grabbed and frame is not None and frame.size > 0
                self.frame = frame if self.grabbed else None

        self.camera.release()
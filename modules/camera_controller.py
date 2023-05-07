import os
from picamera import PiCamera
import time

class CameraController:
    def __init__(self, image_folder="images"):
        self.camera = PiCamera()
        self.image_folder = image_folder
        if not os.path.exists(self.image_folder):
            os.makedirs(self.image_folder)

    def take_picture(self, filename=None):
        if filename is None:
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            filename = f"{self.image_folder}/{timestamp}.jpg"
        self.camera.capture(filename)
        return filename


from picamera import PiCamera
from time import sleep


def f():
    camera = PiCamera()

    camera.start_preview()
    sleep(5)
    camera.stop_preview()

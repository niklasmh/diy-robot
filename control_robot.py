from time import sleep
import RPi.GPIO as GPIO


motors = [
    [17, 18, 27, 22],
    [16, 26, 20, 21],
]

time = 0.001


def setup():
    GPIO.setmode(GPIO.BCM)
    for motor in motors:
        for pin in motor:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, False)


steps = [
    [0],
    [1, 0],
    [1],
    [2, 1],
    [2],
    [3, 2],
    [3],
    [0, 3],
]


def degToSteps(deg):
    return deg * 260 / 180


def up(degrees, motor, time=time):
    for _ in range(degToSteps(degrees)):
        for step in steps:
            for pin in step:
                GPIO.output(motors[motor][pin], True)
            sleep(time)
            for pin in step:
                GPIO.output(motors[motor][pin], False)


def down(degrees, motor, time=time):
    for _ in range(degToSteps(degrees)):
        for step in steps[::-1]:
            for pin in step:
                GPIO.output(motors[motor][pin], True)
            sleep(time)
            for pin in step:
                GPIO.output(motors[motor][pin], False)

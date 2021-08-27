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
    [3],
    [3, 2],
    [2],
    [2, 1],
    [1],
    [1, 0],
    [0],
    [0, 3],
]


def up(count, motor, time=time):
    for _ in range(count):
        for step in steps:
            for pin in step:
                GPIO.output(motors[motor][pin], True)
            sleep(time)
            for pin in step:
                GPIO.output(motors[motor][pin], False)


def down(count, motor, time=time):
    for _ in range(count):
        for step in steps[::-1]:
            for pin in step:
                GPIO.output(motors[motor][pin], True)
            sleep(time)
            for pin in step:
                GPIO.output(motors[motor][pin], False)

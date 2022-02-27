from math import *
from time import sleep
import asyncio
import RPi.GPIO as GPIO

from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory
factory = PiGPIOFactory()


motors = [
    [17, 18, 27, 22],
    [16, 26, 20, 21],
]
jointPins = [14, 15, 23]
joints = []

for pin in jointPins:
    joints.append(
        Servo(pin, min_pulse_width=0.5/1000,
              max_pulse_width=2.5/1000, pin_factory=factory)
    )

# TODO: Create a planner that can interpolate between joint positions

time = 0.02 / 10
maxDegPerSec = 60 / 0.14


def degToTime(deg):
    return max(0.1, (0.14 / 60) * deg * 1.5)


def degToSteps(deg):
    return int(deg * 260 / 180)


def degToPos(deg):
    return -deg / 135


def setup():
    GPIO.setmode(GPIO.BCM)

    # for motor in motors:
    #    for pin in motor:
    #        GPIO.setup(pin, GPIO.OUT)
    #        GPIO.output(pin, False)


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


async def up(degrees, motor, time=time):
    for _ in range(degToSteps(degrees)):
        for step in steps:
            for pin in step:
                GPIO.output(motors[motor][pin], True)
            await asyncio.sleep(time)
            for pin in step:
                GPIO.output(motors[motor][pin], False)


async def down(degrees, motor, time=time):
    for _ in range(degToSteps(degrees)):
        for step in steps[::-1]:
            for pin in step:
                GPIO.output(motors[motor][pin], True)
            await asyncio.sleep(time)
            for pin in step:
                GPIO.output(motors[motor][pin], False)


prev_degree = 0


async def set_joint_position(degree, joint, time=time):
    global prev_degree

    print("Deg:", degree, degToPos(degree))
    joints[joint].value = degToPos(degree)

    dt = degToTime(abs(degree - prev_degree))
    print("Wait:", dt)
    await asyncio.sleep(dt)

    prev_degree = degree


prev_degrees = [0, 0, 0]


def set_joint_positions(degrees, time=time):
    global prev_degrees
    #max_degrees = max(degrees)

    for progress in range(1, 101, 10):
        p = progress / 100
        for i, (end_degree, joint) in enumerate(zip(degrees, joints)):
            prev_degree = prev_degrees[i]
            degree = prev_degree + (end_degree - prev_degree) * p
            joint.value = degToPos(degree)
        sleep(time)

    prev_degrees = degrees

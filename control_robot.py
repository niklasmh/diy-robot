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

time = 0.02
prevDegrees = 0
maxDegPerSec = 60 / 0.14


def degToTime(deg):
    return max(0.1, (0.14 / 60) * deg * 1.5)


def degToSteps(deg):
    return int(deg * 260 / 180)


def degToPos(deg):
    return deg / 135


def setup():
    global prevDegrees
    prevDegrees = 0
    GPIO.setmode(GPIO.BCM)

    for joint in joints:
        joint.value = 0

    for i in range(0, 0):
        # for i in range(0, 10000):
        for j, joint in enumerate(joints):
            hz = 0.02
            joint.value = sin(i / 0.125 * hz + j)*0.5
            sleep(hz)

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


async def set_joint_position(degrees, joint, time=time):
    global prevDegrees

    print("Deg:", degrees, degToPos(degrees))
    joints[joint].value = degToPos(degrees)

    dt = degToTime(abs(degrees - prevDegrees))
    print("Wait:", dt)
    await asyncio.sleep(dt)

    prevDegrees = degrees


def set_joint_positions(degrees, time=time):
    for degree, joint in zip(degrees, joints):
        joint.value = degToPos(degree)
    sleep(time)

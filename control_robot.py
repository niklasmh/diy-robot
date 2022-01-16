from math import *
from time import sleep
import asyncio
import RPi.GPIO as GPIO


motors = [
    [17, 18, 27, 22],
    [16, 26, 20, 21],
]
jointPins = [14, 15, 23]
joints = []

# TODO: Create a planner that can interpolate between joint positions

time = 0.001
prevDegrees = 0
maxDegPerSec = 60 / 0.14

def degToTime(deg):
    return max(0.1, (0.14 / 60) * deg * 1.5)


def degToSteps(deg):
    return int(deg * 260 / 180)


def degToDC(deg):
    return min(12, max(2, 2 + (135 + deg) * 10 / 270))


def setup():
    global prevDegrees
    prevDegrees = 0
    GPIO.setmode(GPIO.BCM)

    for pin in jointPins:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.HIGH)
        joints.append(GPIO.PWM(pin, 50)) # 50 - 330Hz

    for joint in joints:
        joint.start(degToDC(0))
        sleep(0.3)
        joint.ChangeDutyCycle(0)

    for i in range(0, 1):
    #for i in range(0, 10000):
        for j, joint in enumerate(joints):
            hz = 0.02
            joint.ChangeDutyCycle(degToDC(90 * sin(i / 0.125 * hz + j)*0.5))
            sleep(hz)

    for joint in joints:
        joint.start(degToDC(0))
        sleep(0.3)
        joint.ChangeDutyCycle(0)

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

    print("Deg:", degrees, degToDC(degrees))
    joints[joint].ChangeDutyCycle(degToDC(degrees))

    dt = degToTime(abs(degrees - prevDegrees))
    print("Wait:", dt)
    await asyncio.sleep(dt)

    joints[joint].ChangeDutyCycle(0)

    prevDegrees = degrees

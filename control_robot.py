from time import sleep
import RPi.GPIO as GPIO


motors = [
    [17, 18, 27, 22],
    [16, 26, 20, 21],
]

motor = 1

time = 0.001


def setup():
    GPIO.setmode(GPIO.BCM)
    for motor in motors:
        for pin in motor:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, False)


def step1(motor):
    GPIO.output(motors[motor][3], True)
    sleep(time)
    GPIO.output(motors[motor][3], False)


def step2(motor):
    GPIO.output(motors[motor][3], True)
    GPIO.output(motors[motor][2], True)
    sleep(time)
    GPIO.output(motors[motor][3], False)
    GPIO.output(motors[motor][2], False)


def step3(motor):
    GPIO.output(motors[motor][2], True)
    sleep(time)
    GPIO.output(motors[motor][2], False)


def step4(motor):
    GPIO.output(motors[motor][1], True)
    GPIO.output(motors[motor][2], True)
    sleep(time)
    GPIO.output(motors[motor][1], False)
    GPIO.output(motors[motor][2], False)


def step5(motor):
    GPIO.output(motors[motor][1], True)
    sleep(time)
    GPIO.output(motors[motor][1], False)


def step6(motor):
    GPIO.output(motors[motor][0], True)
    GPIO.output(motors[motor][1], True)
    sleep(time)
    GPIO.output(motors[motor][0], False)
    GPIO.output(motors[motor][1], False)


def step7(motor):
    GPIO.output(motors[motor][0], True)
    sleep(time)
    GPIO.output(motors[motor][0], False)


def step8(motor):
    GPIO.output(motors[motor][3], True)
    GPIO.output(motors[motor][0], True)
    sleep(time)
    GPIO.output(motors[motor][3], False)
    GPIO.output(motors[motor][0], False)


def left(step, motor):
    for i in range(step):
        # os.system('clear')
        step1(motor)
        step2(motor)
        step3(motor)
        step4(motor)
        step5(motor)
        step6(motor)
        step7(motor)
        step8(motor)
        print("step left: ", i)


def right(step, motor):
    for i in range(step):
        # os.system('clear')
        step8(motor)
        step7(motor)
        step6(motor)
        step5(motor)
        step4(motor)
        step3(motor)
        step2(motor)
        step1(motor)
        print("step right: ", i)


GPIO.cleanup()

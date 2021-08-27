from time import sleep
import RPi.GPIO as GPIO


motors = [
    [17, 18, 27, 22],
    [16, 20, 26, 21],
]

motor = 1

time = 0.001


def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(motors[motor][0], GPIO.OUT)
    GPIO.setup(motors[motor][1], GPIO.OUT)
    GPIO.setup(motors[motor][2], GPIO.OUT)
    GPIO.setup(motors[motor][3], GPIO.OUT)
    GPIO.output(motors[motor][0], False)
    GPIO.output(motors[motor][1], False)
    GPIO.output(motors[motor][2], False)
    GPIO.output(motors[motor][3], False)


def Step1():
    GPIO.output(motors[motor][3], True)
    sleep(time)
    GPIO.output(motors[motor][3], False)


def Step2():
    GPIO.output(motors[motor][3], True)
    GPIO.output(motors[motor][2], True)
    sleep(time)
    GPIO.output(motors[motor][3], False)
    GPIO.output(motors[motor][2], False)


def Step3():
    GPIO.output(motors[motor][2], True)
    sleep(time)
    GPIO.output(motors[motor][2], False)


def Step4():
    GPIO.output(motors[motor][1], True)
    GPIO.output(motors[motor][2], True)
    sleep(time)
    GPIO.output(motors[motor][1], False)
    GPIO.output(motors[motor][2], False)


def Step5():
    GPIO.output(motors[motor][1], True)
    sleep(time)
    GPIO.output(motors[motor][1], False)


def Step6():
    GPIO.output(motors[motor][0], True)
    GPIO.output(motors[motor][1], True)
    sleep(time)
    GPIO.output(motors[motor][0], False)
    GPIO.output(motors[motor][1], False)


def Step7():
    GPIO.output(motors[motor][0], True)
    sleep(time)
    GPIO.output(motors[motor][0], False)


def Step8():
    GPIO.output(motors[motor][3], True)
    GPIO.output(motors[motor][0], True)
    sleep(time)
    GPIO.output(motors[motor][3], False)
    GPIO.output(motors[motor][0], False)


def left(step):
    for i in range(step):
        # os.system('clear')
        Step1()
        Step2()
        Step3()
        Step4()
        Step5()
        Step6()
        Step7()
        Step8()
        print("Step left: ", i)


def right(step):
    for i in range(step):
        # os.system('clear')
        Step8()
        Step7()
        Step6()
        Step5()
        Step4()
        Step3()
        Step2()
        Step1()
        print("Step right: ", i)


GPIO.cleanup()

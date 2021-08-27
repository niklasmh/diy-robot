from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

IN1 = 17
IN2 = 18
IN3 = 27
IN4 = 22

time = 0.001

GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)
GPIO.output(IN1, False)
GPIO.output(IN2, False)
GPIO.output(IN3, False)
GPIO.output(IN4, False)


def Step1():
    GPIO.output(IN4, True)
    sleep(time)
    GPIO.output(IN4, False)


def Step2():
    GPIO.output(IN4, True)
    GPIO.output(IN3, True)
    sleep(time)
    GPIO.output(IN4, False)
    GPIO.output(IN3, False)


def Step3():
    GPIO.output(IN3, True)
    sleep(time)
    GPIO.output(IN3, False)


def Step4():
    GPIO.output(IN2, True)
    GPIO.output(IN3, True)
    sleep(time)
    GPIO.output(IN2, False)
    GPIO.output(IN3, False)


def Step5():
    GPIO.output(IN2, True)
    sleep(time)
    GPIO.output(IN2, False)


def Step6():
    GPIO.output(IN1, True)
    GPIO.output(IN2, True)
    sleep(time)
    GPIO.output(IN1, False)
    GPIO.output(IN2, False)


def Step7():
    GPIO.output(IN1, True)
    sleep(time)
    GPIO.output(IN1, False)


def Step8():
    GPIO.output(IN4, True)
    GPIO.output(IN1, True)
    sleep(time)
    GPIO.output(IN4, False)
    GPIO.output(IN1, False)


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

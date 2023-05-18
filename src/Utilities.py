#########################################
# classes for interacting with hardware #
#########################################

import RPi.GPIO as GPIO

class Servo:
    def __init__(self, PWM_pin: int, freq: float):
        GPIO.setmode(GPIO.BCM)
        self.__pwm_pin   = PWM_pin
        self.__frequency = freq
        GPIO.setup(self.__pwm_pin, GPIO.OUT)
        self.__sig = GPIO.PWM(self.__pwm_pin, self.__frequency)
        self.__currentPulse = 0.

    def start(self): 
        self.__sig.start(1.5 / (1 / self.__frequency * 1000) * 100)
        self.__currentPulse = 1.5 / (1 / self.__frequency * 1000 * 100)

    def setPulse(self, pulse: float):  # pulse in ms, should lie between [1 ms, 2 ms]
        if pulse > 2: pulse = 2
        elif pulse < 1: pulse = 1

        pulse /= (1 / self.__frequency * 1000)
        pulse *= 100
        
        if pulse != self.__currentPulse:
            self.__sig.ChangeDutyCycle(pulse)
            self.__currentPulse = pulse
            print("New servo pulse: ", pulse)

    def stop(self):
        self.__sig.stop()
        self.__currentPulse = 0

    def __del__(self):
        self.stop()

class Motor:
    def __init__(self, PWM_pin: int):
        GPIO.setmode(GPIO.BCM)
        self.__pwm_pin   = PWM_pin
        self.__frequency = 50
        GPIO.setup(self.__pwm_pin, GPIO.OUT)
        self.__sig = GPIO.PWM(self.__pwm_pin, self.__frequency)
        self.__currentPulse = 0

    def start(self): 
        self.__sig.start(0)
        self.__currentPulse = 0

    def setPulse(self, pulse: float):  # pulse in percents, between [0, 100]
        if pulse > 100: pulse = 100
        elif pulse < 0: pulse = 0
        
        if pulse != self.__currentPulse:
            self.__sig.ChangeDutyCycle(pulse)
            self.__currentPulse = pulse
            print("New motor pulse: ", pulse)

    def stop(self):
        self.__sig.stop()
        self.__currentPulse = 0

    def __del__(self):
        self.stop()

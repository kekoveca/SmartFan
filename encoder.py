import RPi.GPIO as GPIO
import Encoder
import time

encPins = [17, 27, 22]  # [S1->A, S2->B, key]
enc = Encoder.Encoder(encPins[0], encPins[1])
GPIO.setup(encPins[2], GPIO.IN)

servoPin = 23
frequency = 50
GPIO.setup(servoPin, GPIO.OUT)
servo = GPIO.PWM(servoPin, frequency)
servo.start(1.5/20)

try:
    while True:
        print(enc.read(), GPIO.input(encPins[2]))
        servo.ChangeDutyCycle(abs(enc.read()) % 500 / 100 + 5)
        #print(20 * (abs(enc.read()) % 500 / 100 + 5) / 100)
        time.sleep(0.001)
        
except KeyboardInterrupt:
    print("The program was stopped by the keyboard")
else:
    print("No exceptions")
finally:
    GPIO.cleanup()
    print("GPIO cleanup completed, your majesty!")

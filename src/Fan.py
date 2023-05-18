#########################################
# main class for controlling the device #
#########################################

import RPi.GPIO as GPIO
import Encoder
import time
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

from Utilities import Servo, Motor
import settings

class Fan:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        self.big_servo   = Servo(settings.BIG_SERVO_PIN, 50)
        self.small_servo = Servo(settings.SMALL_SERVO_PIN, 50)
        self.motor = Motor(settings.MOTOR_PIN)
        self.enc = Encoder.Encoder(settings.ENC_PINS["A"], settings.ENC_PINS["B"])
        GPIO.setup(settings.ENC_PINS["key"], GPIO.IN)
        GPIO.add_event_detect(settings.ENC_PINS["key"], GPIO.FALLING, callback=self.ChangeState, bouncetime=100)
        self.state = 0  # 0 - nothing, 1 - following
        self.camera = PiCamera()
        self.camera.resolution = (640, 480)
        self.camera.framerate = 32
        self.classifier = cv2.CascadeClassifier('src/haarcascade_frontalface_default.xml')
        #self.classifier = cv2.CascadeClassifier('src/faces.xml')
    
    def start(self):
        self.big_servo.start()
        self.small_servo.start()
        self.motor.start()

        horiz_pid, horiz_int = 0, 0
        vert_pid, vert_int   = 0, 0
        erro, prev_error     = (0, 0), (0, 0)
        target = (320, 240)

        rawCapture = PiRGBArray(self.camera, size=(640, 480))

        # allow the camera to warmup
        time.sleep(0.1)

        while True:
            # camera capture
            self.camera.capture(rawCapture, format="bgr", use_video_port=True)

            image = rawCapture.array

            # faces recognition
            bboxes = self.classifier.detectMultiScale(image)

            if len(bboxes) == 0: self.state = 0
            else:
                box = bboxes[0]
                # coordinates evaluation
                x, y, width, height = box
                x2, y2 = x + width, y + height
                # rectangles drawing
                cv2.rectangle(image, (x, y), (x2, y2), (0, 0, 255), 1)

                # PID regulation
                center = (x + width / 2, y + height / 2)
                error  = (target[0] - center[0], target[1] - center[1])

                horiz_int += error[0]
                if abs(horiz_int) > 1000: horiz_int = 1000 * abs(horiz_int) / horiz_int
                vert_int += error[1]
                if abs(vert_int) > 1000: vert_int = 1000 * abs(vert_int) / vert_int

                horiz_pid += settings.BIG_S_PID_COEFS[0] * error[0] + \
                    settings.BIG_S_PID_COEFS[1] * horiz_int + \
                    settings.BIG_S_PID_COEFS[1] * (error[0] - prev_error[0])

                vert_pid  += settings.SM_S_PID_COEFS[0] * error[1] + \
                    settings.SM_S_PID_COEFS[1] * vert_int + \
                    settings.SM_S_PID_COEFS[1] * (error[1] - prev_error[1])

                if horiz_pid > 1000: horiz_pid = 1000
                elif horiz_pid < 0: horiz_pid = 0
                if vert_pid > 1000: vert_pid = 1000
                elif vert_pid < 0: vert_pid = 0

                if self.state == 1:
                    #print(error[0], error[1])
                    print(horiz_pid, vert_pid)
                    self.big_servo.setPulse((horiz_pid + 1000) /  1000)
                    self.big_servo.setPulse((horiz_pid + 1000) /  1000)

                prev_error = error

	        # show the frame
            cv2.imshow("Frame", image)
            key = cv2.waitKey(1) & 0xFF

	        # clear the stream in preparation for the next frame
            rawCapture.truncate(0)

            # motor rotation speed reguation
            self.motor.setPulse(self.enc.read() // 10 * 2)


    def ChangeState(self, channel):
        if self.state == 0: self.state = 1
        print(self.state)

    def __del__(self):
        GPIO.cleanup()

    

# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

# previously learned model loading
classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#classifier = cv2.CascadeClassifier('faces.xml')

# allow the camera to warmup
time.sleep(0.1)

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
    image = frame.array

    # faces recognition
    bboxes = classifier.detectMultiScale(image)
    for box in bboxes:
        # coordinates evaluation
        x, y, width, height = box
        x2, y2 = x + width, y + height
        # rectangles drawing
        cv2.rectangle(image, (x, y), (x2, y2), (0, 0, 255), 1) 

	# show the frame
    cv2.imshow("Frame", image)
    key = cv2.waitKey(1) & 0xFF

	# clear the stream in preparation for the next frame
    rawCapture.truncate(0)

	# if the `q` key was pressed, break from the loop
    if key == ord("q"):
	    break
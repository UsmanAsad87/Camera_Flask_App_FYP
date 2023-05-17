import cv2
import numpy as np

cap = cv2.VideoCapture("http://admin:User@1234usman@192.168.0.108:8899/onvif/ptz")
# cap = cv2.VideoCapture("rtsp://admin:User@1234usman@192.168.0.108:554/cam/realmonitor?channel=1&subtype=0")


while True:
	_, frame = cap.read()
	 
	cv2.imshow("Frame",frame)
	key = cv2.waitKey(1)

	if  key == 27:		
		break

cap.release()
cv2.destroAllWindows()
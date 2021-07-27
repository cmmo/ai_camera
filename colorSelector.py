from cv2 import cv2
import numpy as np
import uvc
 
frameWidth = 640
frameHeight = 480
# cap = cv2.VideoCapture('rtsp://tapotest:tapotest@172.16.51.56:554/stream2')
#cap = cv2.VideoCapture(0)
# if not (cap.isOpened()):
#     print("Could not open video device")
#     quit()
#cap.set(3, frameWidth)
#cap.set(4, frameHeight)
 
def empty(a):
    pass

dev_list = uvc.device_list()
cap = uvc.Capture(dev_list[0]["uid"])
controls_dict = dict([(c.display_name, c) for c in cap.controls])
controls_dict['Zoom absolute control'].value = 200
cap.frame_mode = (640, 480, 30)

cv2.namedWindow("HSV")
cv2.resizeWindow("HSV", 640, 240)
cv2.createTrackbar("HUE Min", "HSV", 93, 179, empty)
cv2.createTrackbar("HUE Max", "HSV", 113, 179, empty)
cv2.createTrackbar("SAT Min", "HSV", 57, 255, empty)
cv2.createTrackbar("SAT Max", "HSV", 118, 255, empty)
cv2.createTrackbar("VALUE Min", "HSV", 115, 255, empty)
cv2.createTrackbar("VALUE Max", "HSV", 255, 255, empty)
 
 
while True:
 
    #success, img = cap.read()
    img = cap.get_frame_robust()
    #imgHsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    imgHsv = cv2.cvtColor(img.bgr, cv2.COLOR_BGR2HSV)
 
    h_min = cv2.getTrackbarPos("HUE Min", "HSV")
    h_max = cv2.getTrackbarPos("HUE Max", "HSV")
    s_min = cv2.getTrackbarPos("SAT Min", "HSV")
    s_max = cv2.getTrackbarPos("SAT Max", "HSV")
    v_min = cv2.getTrackbarPos("VALUE Min", "HSV")
    v_max = cv2.getTrackbarPos("VALUE Max", "HSV")
    # print(h_min)
 
    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    mask = cv2.inRange(imgHsv, lower, upper)
    result = cv2.bitwise_and(img.bgr, img.bgr, mask=mask)
    #result = cv2.bitwise_and(img, img, mask=mask)
 
    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    hStack = np.hstack([img.bgr, mask, result])
    #hStack = np.hstack([img, mask, result])
    cv2.imshow('Horizontal Stacking', hStack)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
 
cap = None
cv2.destroyAllWindows()

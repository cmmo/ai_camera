from cv2 import cv2
import numpy as np
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import uvc
from gpiozero import *
import alarm
import logging
logging.disable(logging.WARNING)
# capture = cv2.VideoCapture('rtsp://tapotest:tapotest@172.16.51.56:554/stream2')
# capture = cv2.VideoCapture(0)
# if not (capture.isOpened()):
#     print("Could not open video device")
#     quit()
dev_list = uvc.device_list()
capture = uvc.Capture(dev_list[0]["uid"])
controls_dict = dict([(c.display_name, c) for c in capture.controls])
controls_dict['Zoom absolute control'].value = 150
capture.frame_mode = (640, 480, 30)


alarm.alarm_init()

#myColor = [93, 57, 115, 113, 118, 255] #product
myColor = [88, 173, 118, 94, 255, 255] #product
# myColor = [95, 0, 15, 179, 39, 111]
# myColor = [86, 64, 0, 121, 137, 113] #black
# myColor = [32, 92, 127, 73, 255, 255] #grass green
myColorValue =[21, 234, 24]
myPoints = []
#checkWidth = 235
checkWidth_left = 100
checkWidth_right = 200

# ret, img = capture.read()
frame = capture.get_frame_robust()
img = frame.bgr
hi, wi, _ = img .shape
polygon_left = Polygon([(0, 0), (0, checkWidth_left ), (hi, checkWidth_left), (hi, 0)])
polygon_right = Polygon([(0, wi-checkWidth_right), (0, wi), (hi, wi), (hi, wi-checkWidth_right)])

def findColor(img, myColor):
    imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    newPoints = []
    lower = np.array(myColor[0:3])
    upper = np.array(myColor[3:6])
    mask = cv2.inRange(imgHSV,lower,upper)
    getContours(mask)
    # cv2.circle(imgResult, (x,y), 10, myColorValue ,cv2.FILLED)
    # if x!=0 and y!=0:
    #     newPoints.append([x,y])

    return
    # cv2.imshow("img", mask)

def getContours(img):
    if alarm.alarm_manual_stopped:
        return

    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    x, y, w, h = 0,0,0,0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        box = []
        hi, wi, _ = imgResult.shape
        if area>5000:
            rect = cv2.minAreaRect(cnt)
            box = cv2.boxPoints(rect) # 4 corners of the rectangle
            box = np.int0(box)
            # cv2.drawContours(imgResult,[box],0,(0,0,255),2)

            cv2.drawContours(imgResult, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)
            x, y, w, h = cv2.boundingRect(approx)


            if (len(box) and containPoints(box)) or area == 0.0: 
             #print("Enter Error", len(box))
             #Error
                if alarm.pid != 0:    #alarm already run
                    pass
                else:
                    alarm.alarm_start()
                    cv2.putText(imgResult, "ALARM Start", (wi//2, hi//2), cv2.FONT_HERSHEY_COMPLEX, 2, (0,0,255), 4)
            else:
                #Normal
                #if len(box) != 0:
                #    print("Enter Normal", len(box)) 
                alarm.alarm_stop()
                cv2.putText(imgResult, "ALARM Stop", (wi//2, hi//2), cv2.FONT_HERSHEY_COMPLEX, 2, (0,255,0), 4)
        else:
           if alarm.pid != 0:    #alarm already run
                pass
           else:
                alarm.alarm_start()
                cv2.putText(imgResult, "ALARM Start", (wi//2, hi//2), cv2.FONT_HERSHEY_COMPLEX, 2, (0,0,255), 4)


def containPoints(box):
    for a in box:
        point = Point(a[1],a[0])
        if point.within(polygon_left):
            # print(point)
            return True

    for a in box:
        point = Point(a[1],a[0])
        if point.within(polygon_right):
            # print(point)
            return True

    return False

def drawOnCanvas(myPoints, myColorValue):
    for point in myPoints:
        cv2.circle(imgResult, (point[0],point[1]), 10, myColorValue ,cv2.FILLED)

while True:
    frame = capture.get_frame_robust()
    img = frame.bgr
    # ret, img = capture.read()
    imgResult = img.copy()

    findColor(img, myColor)
    # if len(myPoints)!=0:
    #     drawOnCanvas(myPoints, myColorValue)
    
    # imgFlip = cv2.flip(imgResult, 1)
    """Screen"""
    h, w, _ = imgResult.shape
    cv2.rectangle(imgResult,(0,0),(checkWidth_left,h),(0,0,255),2)   #left

    cv2.rectangle(imgResult,(w-checkWidth_right,0),(w,h),(0,0,255),2) #right

    imgResized = cv2.resize(imgResult,(1024,768))
    # print('Original:', imgResult.shape)
    # print('Resized:', imgResult.shape)
    # cv2.imshow('Result',imgResult)
    cv2.imshow('Result',imgResized)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    """Screen"""

capture = None
cv2.destroyAllWindows()

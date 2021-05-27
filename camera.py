from cv2 import cv2
import numpy as np
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import uvc

# capture = cv2.VideoCapture('rtsp://tapotest:tapotest@172.16.51.56:554/stream2')
# capture = cv2.VideoCapture(0)
# if not (capture.isOpened()):
#     print("Could not open video device")
#     quit()
dev_list = uvc.device_list()
capture = uvc.Capture(dev_list[0]["uid"])
controls_dict = dict([(c.display_name, c) for c in capture.controls])
controls_dict['Zoom absolute control'].value = 300
capture.frame_mode = (1920, 1080, 30)

myColor = [90, 201, 149, 96, 255, 255] #logi green
# myColor = [95, 0, 15, 179, 39, 111]
# myColor = [86, 64, 0, 121, 137, 113] #black
# myColor = [32, 92, 127, 73, 255, 255] #grass green
myColorValue =[21, 234, 24]
myPoints = []
checkWidth = 100

# ret, img = capture.read()
frame = capture.get_frame_robust()
img = frame.bgr
hi, wi, _ = img .shape
polygon_left = Polygon([(0, 0), (0, checkWidth), (hi, checkWidth), (hi, 0)])
polygon_right = Polygon([(0, wi-checkWidth), (0, wi), (hi, wi), (hi, wi-checkWidth)])

def findColor(img, myColor):
    imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    newPoints = []
    lower = np.array(myColor[0:3])
    upper = np.array(myColor[3:6])
    mask = cv2.inRange(imgHSV,lower,upper)
    x,y = getContours(mask)
    # cv2.circle(imgResult, (x,y), 10, myColorValue ,cv2.FILLED)
    # if x!=0 and y!=0:
    #     newPoints.append([x,y])

    return newPoints
    # cv2.imshow("img", mask)

def getContours(img):
    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    x, y, w, h = 0,0,0,0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        box = []
        if area>5000:
            rect = cv2.minAreaRect(cnt)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            # cv2.drawContours(imgResult,[box],0,(0,0,255),2)

            cv2.drawContours(imgResult, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)
            x, y, w, h = cv2.boundingRect(approx)

        hi, wi, _ = imgResult.shape
        if len(box) and containPoints(box): 
            cv2.putText(imgResult, "ALARM", (wi//2, hi//2), cv2.FONT_HERSHEY_COMPLEX, 2, (0,0,255), 4)
        # else:
        #     cv2.putText(imgResult, "OK", (wi//2, hi//2), cv2.FONT_HERSHEY_COMPLEX, 2, (0,255,0), 4)
        
    # if OKflag:
    # else:

    return x+w//2, y

def containPoints(box):
    for a in box:
        point = Point(a[1],a[0])
        if point.within(polygon_left):
            print(point)
            return True

    for a in box:
        point = Point(a[1],a[0])
        if point.within(polygon_right):
            print(point)
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

    newPoints = findColor(img, myColor)
    if len(newPoints)!=0:
        for newP in newPoints:
            myPoints.append(newP)
    # if len(myPoints)!=0:
    #     drawOnCanvas(myPoints, myColorValue)
    
    # imgFlip = cv2.flip(imgResult, 1)
    h, w, _ = imgResult.shape
    cv2.rectangle(imgResult,(0,0),(checkWidth,h),(0,0,255),2)

    cv2.rectangle(imgResult,(w-checkWidth,0),(w,h),(0,0,255),2)

    imgResized = cv2.resize(imgResult,(1366,768))
    # print('Original:', imgResult.shape)
    # print('Resized:', imgResult.shape)
    cv2.imshow('Result',imgResized)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

capture = None
cv2.destroyAllWindows()

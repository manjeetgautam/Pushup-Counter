import cv2
import time

import cvzone
from cvzone.PoseModule import PoseDetector
import numpy as np
frameWidth = 640
frameHeight = 500
cap = cv2.VideoCapture("pushup.mp4")

detector = PoseDetector()
ptime = 0
ctime = 0
color = (0,0,255)
dir =0
push_ups =0

while True:
    success, img = cap.read()
    img = cv2.resize(img, (frameWidth, frameHeight))
    img = detector.findPose(img,False)

    lmlst, bbox = detector.findPosition(img,draw=False)
    if lmlst:
        # print angle
        a1 = detector.findAngle(img,12,14,16,False)
        a2 = detector.findAngle(img,15,13,11,False)
        per_val1 = int(np.interp(a1,(85,165),(100,0)))
        per_val2 = int(np.interp(a2,(85,165),(100,0)))

        bar_val1 = int(np.interp(per_val1,(0,100),(40+350,40)))
        bar_val2 = int(np.interp(per_val2, (0, 100), (40 + 350, 40)))

        #  bar_val1 = int(np.interp(per_val1,(0,100),(40+350+40)))
        # print(per_val1)
        #  cv2.rectangle(img,(x,y),(x+w,y+h))
        cv2.rectangle(img,(570,bar_val1),(570+35,40+350),(color),cv2.FILLED)
        cv2.rectangle(img, (570, 40), (570 + 35, 40 + 350), (), 3)

        #bar 2
        cv2.rectangle(img, (35, bar_val2), (35 + 35, 40 + 350), (color), cv2.FILLED)
        cv2.rectangle(img, (35, 40), (35 + 35, 40 + 350), (), 3)

        # percentage counter
        cvzone.putTextRect(img,f'{per_val2} %',(35,25),1.1,2,colorT=(255,255,255),colorR=color,border=3,colorB=())
        cvzone.putTextRect(img,f'{per_val1} %',(570,25),1.1,2,colorT=(255,255,255),colorR=color,border=3,colorB=())

        if per_val1 == 100 and per_val2 == 100:
            if dir == 0:
                push_ups += 0.5
                dir = 1
                color = (0,255,0)
        elif per_val1 == 0 and per_val2 == 0:
            if dir == 1:
                push_ups += 0.5
                dir = 0
                color = (0,255,0)
        else:
            color = (0,0,255)
        #print(push_ups)
        cvzone.putTextRect(img,f'push_ups : {int (push_ups)}',(218,35),2,2,colorT=(255,255,255),colorR=(255,0,0),border=2,colorB=())

    cv2.imshow("Result", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
      break

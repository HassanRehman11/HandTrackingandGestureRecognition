import cv2
import numpy as np
import math
from pynput.mouse import Button,Controller
#import matplotlib.pyplot as plt
#import wx
mouse = Controller()
#app=wx.App(False)
#(sx,sy)=wx.GetDisplaySize()
(sx,sy)=(1600,900)
(camx,camy)=(320,400)
def nothing(x):
    pass
cv2.namedWindow('image')
cv2.createTrackbar('hl','image',0,255,nothing)
cv2.createTrackbar('sl','image',0,255,nothing)
cv2.createTrackbar('vl','image',0,255,nothing)
cv2.createTrackbar('hh','image',0,255,nothing)
cv2.createTrackbar('sh','image',0,255,nothing)
cv2.createTrackbar('vh','image',0,255,nothing)
cv2.createTrackbar('max','image',0,1000,nothing)
cv2.createTrackbar('ON/OFF','image',0,1,nothing)


cv2.setTrackbarPos('hl','image',39)
cv2.setTrackbarPos('sl','image',55)
cv2.setTrackbarPos('vl','image',85)

cv2.setTrackbarPos('hh','image',72)
cv2.setTrackbarPos('sh','image',144)
cv2.setTrackbarPos('vh','image',255)

cv2.setTrackbarPos('max','image',250)


pinchFlag=0
def get_frame(cap, scaling_factor):
   
    ret, frame = cap.read()
    
    frame = cv2.resize(frame, None, fx=scaling_factor,
            fy=scaling_factor, interpolation=cv2.INTER_AREA)

    return frame

if __name__=='__main__':
    cap = cv2.VideoCapture(1)
    scaling_factor = 0.5

    
    while True:
        hl = cv2.getTrackbarPos('hl','image')
        sl=cv2.getTrackbarPos('sl','image')
        vl =cv2.getTrackbarPos('vl','image')
        hh=cv2.getTrackbarPos('hh','image')
        sh=cv2.getTrackbarPos('sh','image')
        vh=cv2.getTrackbarPos('vh','image')
        maxar=cv2.getTrackbarPos('max','image')
        btn=cv2.getTrackbarPos('ON/OFF','image')
        
        fontface = cv2.FONT_HERSHEY_SIMPLEX
        fontscale = 3
        fontcolor = (0, 0, 255)

        frame = get_frame(cap, scaling_factor)
        frame = cv2.resize(frame,(320,400))
        
        
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        g = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        lower = np.array([hl,sl,vl])
        upper = np.array([hh,sh,vh])
        mask = cv2.inRange(hsv, lower, upper)
        res = cv2.bitwise_and(frame, frame, mask=mask)
        res2 = cv2.medianBlur(res, 5)
        gray = cv2.cvtColor(res2,cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray,(5,5),0)
        ret,thresh = cv2.threshold(blur,127,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        im2, conts, hierarchy = cv2.findContours(thresh.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
        if btn==1:
            try:
                if(len(conts)==2):
                    try:
                        if(pinchFlag==1):
                            pinchFlag=0
                            mouse.release(Button.left)
                        x1,y1,w1,h1=cv2.boundingRect(conts[0])
                        x2,y2,w2,h2=cv2.boundingRect(conts[1])
                        cv2.rectangle(frame,(x1,y1),(x1+w1,y1+h1),(255,0,0),2)
                        cv2.rectangle(frame,(x2,y2),(x2+w2,y2+h2),(255,0,0),2)
                        cx1=x1+w1/2
                        cy1=y1+h1/2
                        cx2=x2+w2/2
                        cy2=y2+h2/2
                        cx=int((cx1+cx2)/2)
                        cy=int((cy1+cy2)/2)
                        cv2.line(frame, (int(cx1),int(cy1)),(int(cx2),int(cy2)),(255,0,0),2)
                        cv2.circle(frame, (cx,cy),2,(0,0,255),2)
                        mouseLoc=(int(sx-(cx*sx/camx)), int(cy*sy/camy))
                        mouse.position=mouseLoc 
                        while mouse.position!=mouseLoc:
                            pass
                    except:
                        pass
                elif(len(conts)==1):
                    try:
                        x,y,w,h=cv2.boundingRect(conts[0])
                        if(pinchFlag==0):
                            pinchFlag=1
                            mouse.press(Button.left)
                        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
                        cx=int(x+w/2)
                        cy=int(y+h/2)
                        cv2.circle(frame,(cx,cy),int((w+h)/4),(0,0,255),2)
                        mouseLoc=(int(sx-(cx*sx/camx)), int(cy*sy/camy))
                        mouse.position=mouseLoc 
                        while mouse.position!=mouseLoc:
                            pass
                    except:
                        pass
            except:
                pass
      
        
        #cv2.imshow('Original image', thresh)
        #cv2.imshow('HSV', hsv)
        #cv2.imshow('Blur', mask)
        cv2.imshow('image', frame)
        
        
        c = cv2.waitKey(5)
        if c == 27:
            break

cv2.destroyAllWindows()

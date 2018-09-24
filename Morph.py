import cv2
import numpy as np

class Morph:
    @staticmethod
    def ImgMorph(frame,Lower,Upper):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower = np.array([Lower[0], Lower[1], Lower[2]])
        upper = np.array([Upper[0], Upper[1], Upper[2]])
        mask = cv2.inRange(hsv, lower, upper)
        res = cv2.bitwise_and(frame, frame, mask=mask)
        res2 = cv2.medianBlur(res, 5)
        gray = cv2.cvtColor(res2, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        ret, thresh = cv2.threshold(blur, 127, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        im2, contours, hierarchy = cv2.findContours(thresh.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
        return thresh
    
    @staticmethod
    def contour(retImg,cont):
        max_area=500
        for i in range(len(cont)):
            cnt = cont[i]
            area =cv2.contourArea(cnt)
            if(area>max_area):
                ci=i
            cnt=cont[ci]
            x1,y1,w1,h1 = cv2.boundingRect(cnt)
            cv2.rectangle(retImg, (x1, y1), (x1 + w1, y1 + h1), (0,0,0), 1)
            roi = retImg[y1:y1+h1, x1:x1+w1]
            return roi

    
   



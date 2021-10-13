import cv2
import numpy as np

def getContours(img,cThr=&#91;100,100],showCanny=False,minArea=1000,filter=0,draw =False):
    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray,(5,5),1)
    imgCanny = cv2.Canny(imgBlur,cThr&#91;0],cThr&#91;1])
    kernel = np.ones((5,5))
    imgDial = cv2.dilate(imgCanny,kernel,iterations=3)
    imgThre = cv2.erode(imgDial,kernel,iterations=2)
    if showCanny:cv2.imshow('Canny',imgThre)
    contours,hiearchy = cv2.findContours(imgThre,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    finalCountours = &#91;]
    for i in contours:
        area = cv2.contourArea(i)
        if area > minArea:
            peri = cv2.arcLength(i,True)
            approx = cv2.approxPolyDP(i,0.02*peri,True)
            bbox = cv2.boundingRect(approx)
            if filter > 0:
                if len(approx) == filter:
                    finalCountours.append(&#91;len(approx),area,approx,bbox,i])
            else:
                finalCountours.append(&#91;len(approx),area,approx,bbox,i])
    finalCountours = sorted(finalCountours,key = lambda x:x&#91;1] ,reverse= True)
    if draw:
        for con in finalCountours:
            cv2.drawContours(img,con&#91;4],-1,(0,0,255),3)
    return img, finalCountours

def reorder(myPoints):
    #print(myPoints.shape)
    myPointsNew = np.zeros_like(myPoints)
    myPoints = myPoints.reshape((4,2))
    add = myPoints.sum(1)
    myPointsNew&#91;0] = myPoints&#91;np.argmin(add)]
    myPointsNew&#91;3] = myPoints&#91;np.argmax(add)]
    diff = np.diff(myPoints,axis=1)
    myPointsNew&#91;1]= myPoints&#91;np.argmin(diff)]
    myPointsNew&#91;2] = myPoints&#91;np.argmax(diff)]
    return myPointsNew

def warpImg (img,points,w,h,pad=20):
    # print(points)
    points =reorder(points)
    pts1 = np.float32(points)
    pts2 = np.float32(&#91;&#91;0,0],&#91;w,0],&#91;0,h],&#91;w,h]])
    matrix = cv2.getPerspectiveTransform(pts1,pts2)
    imgWarp = cv2.warpPerspective(img,matrix,(w,h))
    imgWarp = imgWarp&#91;pad:imgWarp.shape&#91;0]-pad,pad:imgWarp.shape&#91;1]-pad]
    return imgWarp

def findDis(pts1,pts2):
    return ((pts2&#91;0]-pts1&#91;0])**2 + (pts2&#91;1]-pts1&#91;1])**2)**0.5
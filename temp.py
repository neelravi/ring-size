import numpy as np
import cv2

img = cv2.imread("testPalm.png")
hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV);
lower_hand = np.array([0,30,60])
upper_hand = np.array([20,150,255])

mask = cv2.inRange(hsv, lower_hand, upper_hand)

res = cv2.bitwise_and(img, img, mask=mask)

#"derp" wasn't needed in my code tho..
contours,hierarchy = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
for cnt in contours:
    hull = cv2.convexHull(cnt)
    cv2.drawContours(img,[cnt],0,(0,255,0),2)
    cv2.drawContours(img,[hull],0,(0,0,255),2)

cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
'''
Program to predict the ring size of a person from an image.
Written by: Ravindra Shinde v1.0 using opencv
v2.0 using tensorflow coming soon.
'''

import cv2
import numpy as np
from math import pi

### Some important info
# credit card width = 85.6 mm  (from international standards data)
# credit card height = 53.98 mm (from international standards data)

cc_width_mm = 85.6  # mm
cc_height_mm = 53.98 # mm

cc_width_pixels_array = np.array([403, 401, 402, 405, 404])
average_card_width_pixels = np.average(cc_width_pixels_array)
pixel_to_mm = cc_width_mm / average_card_width_pixels

def calc_distance(x1,y1,x2,y2):
    distance = round(np.sqrt((x1-x2)**2 + (y1-y2)**2))
    print("distance in pixels = ", distance)
    print("distance in mm = ", distance*pixel_to_mm)
    return distance*pixel_to_mm


# Create point matrix get coordinates of mouse click on image
point_matrix = np.zeros((2,2),int)

counter = 0
def mousePoints(event,x,y,flags,params):
    global counter
    # Left button mouse click event opencv
    if event == cv2.EVENT_LBUTTONDOWN:
        point_matrix[counter] = x,y
        counter = counter + 1

# Read image
img = cv2.imread('hand1.png')

hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV);
mask = cv2.imread('hand1.png',0)
res = cv2.bitwise_and(img, img, mask=mask)

#"derp" wasn't needed in my code tho..
contours,hierarchy = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
for cnt in contours:
    hull = cv2.convexHull(cnt)
    cv2.drawContours(img,[cnt],0,(0,255,0),2)
    cv2.drawContours(img,[hull],0,(0,0,255),2)

cv2.imshow('image',img)
cv2.imwrite('step1.jpg',img)

while counter<=2:
    for x in range (0,2):
        cv2.circle(img,(point_matrix[x][0],point_matrix[x][1]),3,(0,255,0),cv2.FILLED)

    if counter == 2:
        starting_x = point_matrix[0][0]
        starting_y = point_matrix[0][1]

        ending_x = point_matrix[1][0]
        ending_y = point_matrix[1][1]
        # Draw rectangle for area of interest
        #cv2.rectangle(img, (starting_x, starting_y), (ending_x, ending_y), (0, 255, 0), 3)
        cv2.line(img,(starting_x,starting_y),(ending_x,ending_y),(0,0,255),3)
        distance = calc_distance(starting_x,starting_y,ending_x,ending_y)
        cv2.putText(img, str(pi*distance) + ' mm (circum)', (starting_x,starting_y), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (127,0,255), 2)
        # Cropping image
        img_cropped = img[starting_y:ending_y, starting_x:ending_x]
        cv2.imshow("ROI", img_cropped)
        cv2.imwrite('step3.jpg',img_cropped)

    # Showing original image
    cv2.imshow("Original Image ", img)
    # Mouse click event on original image
    cv2.setMouseCallback("Original Image ", mousePoints)
    # Printing updated point matrix
    print(point_matrix)
    # Refreshing window all time
    cv2.waitKey(1)
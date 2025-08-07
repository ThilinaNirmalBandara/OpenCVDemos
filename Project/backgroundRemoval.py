import cv2
import numpy as np
import sys

video = cv2.VideoCapture(0)

success,refImage = video.read()
flag = 0

while(1):
    success,image = video.read()
    if flag == 0:
        refImage = image

    diff1 = cv2.subtract(image,refImage)
    diff2 = cv2.subtract(refImage,image)
    diff = diff1+diff2
    diff[abs(diff)<13.0]=0
    #gray
    gray = cv2.cvtColor(diff.astype(np.uint8), cv2.COLOR_BGR2GRAY)
    gray[np.abs(gray)<10]=0
    fgmask = gray.astype(np.uint8)
    fgmask[fgmask>0]=255
    fgimg = cv2.bitwise_and(image, image, mask = fgmask)
    kernel = np.ones((5,5), np.uint8)
    fgimgEroded = cv2.erode(fgimg,kernel,iterations=1)
    cv2.imshow("Edges",fgimgEroded)


    key = cv2.waitKey(5) & 0xff
    if ord('q') == key:
        break
    elif ord('b') == key:
        flag = 1
        print("Background captured")
    elif ord('c') == key:
        flag = 0
        print("Ready to capture new background")

cv2.destroyAllWindows()
video.release()

        


        

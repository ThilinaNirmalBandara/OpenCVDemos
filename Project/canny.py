import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while(1):
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    lowerRed = np.array([30,150,50])
    upperRed = np.array([255,255,180])

    mask = cv2.inRange(hsv, lowerRed, upperRed)
    result = cv2.bitwise_and(frame, frame, mask=mask)

    cv2.imshow("Red Masked Area", result)

    cv2.imshow("Original",frame)

    edges = cv2.Canny(frame, 100, 200)
    cv2.imshow("Edges", edges)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
cap.release()
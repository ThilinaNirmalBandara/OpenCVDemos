import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while(1):
    _, frame = cap.read()

    blur = cv2.GaussianBlur(frame,(15,15),cv2.BORDER_DEFAULT)

    cv2.imshow("Original",frame)
    cv2.imshow("Blur",blur)

    if cv2.waitKey(1) & 0xFF in [ord('q'), 27]:   # exit when either 'esc' or 'q' keys pressed
        break

cap.release()
cv2.destroyAllWindows()
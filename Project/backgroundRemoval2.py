import cv2
import numpy as np
import time

cap = cv2.VideoCapture(0)
flag = 0

# Read one frame initially to avoid crash
ret, refImage = cap.read()
if not ret:
    print("Failed to access the webcam.")
    exit()

font = cv2.FONT_HERSHEY_SIMPLEX
start_time = time.time()

# Desired display size (width x height)
DISPLAY_WIDTH = 640
DISPLAY_HEIGHT = 240

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame.")
        break

    if flag == 0:
        refImage = frame.copy()

    # Compute absolute difference
    diff = cv2.absdiff(frame, refImage)
    diff[diff < 13] = 0

    # Grayscale + thresholding
    gray = cv2.cvtColor(diff.astype(np.uint8), cv2.COLOR_BGR2GRAY)
    gray[gray < 10] = 0
    fgmask = np.where(gray > 10, 255, 0).astype(np.uint8)

    # Morphology (clean up noise)
    kernel = np.ones((5, 5), np.uint8)
    fgmask_eroded = cv2.erode(fgmask, kernel, iterations=1)

    # Extract moving objects from current frame
    fgimg = cv2.bitwise_and(frame, frame, mask=fgmask_eroded)

    # Add live overlay instructions to the original frame
    overlay = frame.copy()
    cv2.putText(overlay, "Press 'b' to set background", (10, 25), font, 0.6, (0, 255, 0), 2)
    cv2.putText(overlay, "Press 'c' to reset background", (10, 50), font, 0.6, (0, 255, 0), 2)
    cv2.putText(overlay, "Press 'q' to quit", (10, 75), font, 0.6, (0, 0, 255), 2)

    # Resize both frames to the same dimensions
    overlay_resized = cv2.resize(overlay, (DISPLAY_WIDTH, DISPLAY_HEIGHT))
    fgimg_resized = cv2.resize(fgimg, (DISPLAY_WIDTH, DISPLAY_HEIGHT))

    # Concatenate side by side
    combined = np.hstack((overlay_resized, fgimg_resized))

    # Show side-by-side output
    cv2.imshow("Original (Left) + Motion Detected (Right)", combined)

    # Key handling
    key = cv2.waitKey(5) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('b'):
        flag = 1
        print("[INFO] Background set.")
    elif key == ord('c'):
        flag = 0
        print("[INFO] Background will be reset.")

cap.release()
cv2.destroyAllWindows()

import cv2
import mediapipe
import pyautogui
import time


mpHands = mediapipe.solutions.hands.Hands()
mpDraw = mediapipe.solutions.drawing_utils
camera = cv2.VideoCapture(0)

screenWidth, screenHeight = pyautogui.size()

exitDist = 50
indexX = indexY = thumbX = thumbY = midX = midY = pinkyX = pinkyY = 0

prevMouseX, prevMouseY = 0, 0
smoothness = 0.2 

lastClickTime = 0
CLICK_COOLDOWN = 0.8  # seconds

dragging = False


while(1):
    _,frame = camera.read()
    frame = cv2.flip(frame,1)
    frameRGB = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    result = mpHands.process(frameRGB)

    if result.multi_hand_landmarks:
        for handLms in result.multi_hand_landmarks:
            mpDraw.draw_landmarks(frame,handLms)

            for id, lm in enumerate(handLms.landmark):
                h,w,_ = frame.shape

                if(id == 8 or id == 4 or id == 12 or id == 20):
                    cx,cy = int(lm.x*w), int(lm.y*h)
                    #print(f"Landmark {id}: ({cx},{cy})")
                    cv2.circle(frame,(cx,cy),10,(0,255,255))

                    if(id == 8):
                        targetMouseX  = int(screenWidth / w * cx)
                        targetMouseY = int(screenHeight / h * cy)

                        mouseX = int(prevMouseX + (targetMouseX - prevMouseX) * smoothness)
                        mouseY = int(prevMouseY + (targetMouseY- prevMouseY) * smoothness)
                        pyautogui.moveTo(mouseX,mouseY)

                        prevMouseX, prevMouseY = mouseX, mouseY
                        indexX = cx
                        indexY = cy

                    if(id == 4):
                        thumbX = cx
                        thumbY = cy

                    if(id == 12):
                        midX = cx
                        midY = cy

                    if(id == 20):
                        pinkyX = cx
                        pinkyY = cy

            dist = thumbY-pinkyY
            exitDist = thumbY-midY
            dragDist = ((thumbX - indexX)**2 + (thumbY - indexY)**2)**0.5
            
            print(dragDist)
             
            if dist < 20 and time.time() - lastClickTime > CLICK_COOLDOWN and exitDist > 20:
                pyautogui.click() 
                lastClickTime = time.time() 

            if dragDist < 25 and not dragging and dist > 20 and exitDist > 20:
                pyautogui.mouseDown()
                dragging = True

            if dragging:
                screenX = int(screenWidth / w * indexX)
                screenY = int(screenHeight / h * indexY)
                pyautogui.dragTo(screenX, screenY, duration=2, button='left')


            if dragDist > 30 and dragging:
                pyautogui.mouseUp()
                dragging = False

            if dist < 20 and exitDist < 20 :
                pyautogui.doubleClick()
                
               
                

    cv2.imshow("Original Video", frame)
    key = cv2.waitKey(1)
    if (key & 0xFF) == 27 or (exitDist< 10):
        break
camera.release()
cv2.destroyAllWindows()

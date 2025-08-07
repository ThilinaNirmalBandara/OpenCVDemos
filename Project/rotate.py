import cv2

def rotate(image):
    rows,cols = image.shape[:2]
    M = cv2.getRotationMatrix2D((cols/2,rows/2),90,1) # rotation ceter , angle, 
    dst = cv2.warpAffine(image,M,(cols,rows))
    return dst


image = cv2.imread("Project/Spark.jpg")
height = 476
width = 476
dim = (width,height)
image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
print("Image Dimensions",image.shape[:2])

while(1):
    image = rotate(image)
    cv2.imshow("Rotate",image)
    key = cv2.waitKey(500)
    if(key & 0xFF == ord('q')):
        cv2.destroyAllWindows()
        break
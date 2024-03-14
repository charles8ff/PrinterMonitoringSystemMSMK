import cv2 #for camera
import schedule 
import time
from threading import Thread #for the future

name = 'photo'
def take_photo(filename = name+ '.jpg'):
    # Initialize the camera
    cap = cv2.VideoCapture(0)  # 0 is usually the default camera
    
    # Check if the webcam is opened correctly
    if not cap.isOpened():
        raise IOError('Cannot open webcam')
    
    ret, frame = cap.read()
    cam = time.time()
    camTime = cam - start

    print('Camera open in : ' + str(camTime) + ' seconds') # ~90 s in desktop
    if ret:
        cv2.imwrite(filename, frame)
        print(f'Photo taken and saved as {filename}')
    else:
        print('Failed to take photo')
    
    # Release the camera
    cap.release()
    
start = time.time()
print(start)    
take_photo()

print('Success')
end = time.time()
excTime = end - start
print (end, excTime)
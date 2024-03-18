import cv2 #for camera #pip install opencv-python
from datetime import datetime
import schedule 
import time
from threading import Thread #for the future
import os

filename = 'photo'
def take_photo(filename = filename):
    # Initialize the camera
    cap = cv2.VideoCapture(0)
    # Check if the webcam is opened correctly
    if not cap.isOpened():
        raise IOError('Cannot open webcam')
    
    cam = time.time()
    camTime = cam - start
    print('Camera open in : ' + str(camTime)[:5] + ' seconds') # ~90 s in desktop
    
    ret, frame = cap.read()
    now =  datetime.now()
    filename = str(now.strftime('%Y%m%d_%H%M%S%f.jpg'))
    print(filename)
    if ret:
        cv2.imwrite(filename, frame)
        print(f'Photo taken and saved as {filename}')
    else:
        print('Failed to take photo')
    
    # Release the camera
    cap.release()
### TIMERS   
start = time.time()
print('Program started at timestamp: '+ str(start)) # my machine is slow


take_photo()

### TIMERS 
print('Success')
end = time.time()
excTime = end - start
print (str(excTime)[:5])
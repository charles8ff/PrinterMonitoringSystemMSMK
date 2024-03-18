import cv2 #for camera #pip install opencv-python
from datetime import datetime
import schedule 
import time
from threading import Thread #for the future
import os

chosen_res = [0, 0]

def set_resolution(cap, width, height):
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    
    
def take_photo(chosen_res, save_path ='./photos/'):
    # Check for path 
    os.makedirs(save_path, exist_ok = True)
    
    # Initialize the camera
    cap = cv2.VideoCapture(0)
    # Check if the webcam is opened correctly
    if not cap.isOpened():
        raise IOError('Cannot open webcam')
    
    set_resolution(cap, chosen_res[0], chosen_res[1])
    
    ### TIMERS
    cam = time.time()
    camTime = cam - start
    print(f'Camera open in : {str(camTime)[:5]} seconds') # ~90 s in desktop
    
    ret, frame = cap.read()
    now =  datetime.now()
    filename = str(now.strftime('%Y%m%d_%H%M%S.jpg'))
    full_path = os.path.join(save_path, filename)
    print(full_path)
    if ret:
        cv2.imwrite(full_path, frame)
        print(f'Photo taken and saved as {full_path}')
    else:
        print('Failed to take photo')
    
    # Release the camera
    cap.release()

### TIMERS   
start = time.time()
print(f'Program started at timestamp: {str(start)}') # my machine is slow

res = [1280, 720]
take_photo(res)

### TIMERS 
print('Success')
end = time.time()
excTime = end - start
print (str(excTime)[:5])
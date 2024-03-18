import cv2 #for camera #pip install opencv-python
from datetime import datetime, timezone
import schedule 
import time
from threading import Thread #for the future
import os

chosen_res = [0, 0]

res_options = {
    '1' : [1920, 1080],
    '2' : [1280, 720],
    '3' : [720, 480],
    '4' : [640, 360]
}

interval = 1 # in seconds?

def set_resolution(cap, width, height):
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

def set_interval():
    pass
    
def take_photo(chosen_res, save_path ='./photos/'):
    # Check for path 
    os.makedirs(save_path, exist_ok = True)
    
    # Initialize the camera
    cap = cv2.VideoCapture(0)
    # Check if the webcam is opened correctly
    if not cap.isOpened():
        raise IOError('Cannot open webcam')
    
    # Set values from chosen_res to the cv2 object
    set_resolution(cap, chosen_res[0], chosen_res[1])
    
    ### TIMERS
    cam = time.time()
    camTime = cam - start
    print(f'Camera open in : {str(camTime)[:7]} seconds') # ~90 s in desktop
    
    ret, frame = cap.read()
    now =  datetime.now(timezone.utc).isoformat()
    filename = now.replace(':', '-').replace('.', '-')
    filename += '.jpg'
    full_path = os.path.join(save_path, filename)

    if ret:
        cv2.imwrite(full_path, frame)
        print(f'Photo taken and saved at {full_path} with resolution {chosen_res[0]}x{chosen_res[1]}.')
    else:
        print('Failed to take photo.')
    
    # Release the camera
    cap.release()

def get_user_res(res_options):
    
    prompt = 'Choose a resolution between the options given:\n'
    for key, value in res_options.items():
        prompt += f'\t{key}): {value[0]} x {value[1]}\n'
    prompt += '\t>> '
    
    choice = input(prompt)
    
    while choice not in res_options:
        print('Chosen option not supported, please try again.\n')
        choice = input(prompt)

    return choice

### TIMERS   
start = time.time()
print(f'Program started at timestamp: {str(start)}') # my machine is slow


### Ask users
user_res = get_user_res(res_options)
res = res_options[user_res]
take_photo(res)

### TIMERS 
print('Success')
end = time.time()
excTime = end - start
print (str(excTime)[:7])
import cv2 #for camera #pip install opencv-python
from datetime import datetime, timezone
import schedule
import time
from threading import Thread #for the future
import os
import logging
from logging.handlers import BaseRotatingHandler

chosen_res = [0, 0]

res_options = {
    '1' : [1920, 1080],
    '2' : [1280, 720],
    '3' : [720, 480],
    '4' : [640, 360]
}

interval = 1 # in seconds?

# Create logs directory
logs_path = './logs'
os.makedirs(logs_path, exist_ok = True)

# Custom log handler
class MaxLinesRotatingFileHandler(BaseRotatingHandler):
    def __init__(self, filename, maxLines = 1500, backupCount = 5, encoding = None, delay = False):
        self.maxLines = maxLines
        self.backupCount = backupCount
        self.counter = 0  # Line counter
        super(MaxLinesRotatingFileHandler, self).__init__(filename, mode = 'a', encoding = encoding, delay = delay)

    def shouldRollover(self, record):
        # Increment line counter with each log entry
        self.counter += 1
        if self.counter >= self.maxLines:
            return 1
        return 0

    def doRollover(self):
        self.stream.close()
        # Rotate files
        for i in range(self.backupCount - 1, 0, -1):
            sfn = self.rotation_filename(f'{self.baseFilename}.{i}')
            dfn = self.rotation_filename(f'{self.baseFilename}.{i + 1}')
            if os.path.exists(sfn):
                if os.path.exists(dfn):
                    os.remove(dfn)
                os.rename(sfn, dfn)
        dfn = self.rotation_filename(f'{self.baseFilename}.1')
        if os.path.exists(dfn):
            os.remove(dfn)
        self.rotate(self.baseFilename, dfn)

        if not self.delay:
            self.stream = self._open()
        self.counter = 0  # Reset counter



# Set up logging
log_filename = os.path.join(logs_path, 'webcam_capture.log')
logger = logging.getLogger('WebcamCaptureLogger')
logger.setLevel(logging.DEBUG)

handler = MaxLinesRotatingFileHandler(log_filename, maxLines=1500, backupCount = 5)
handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)

def set_resolution(cap, width, height):
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    logger.info(f'Resolution set to {width}x{height}')

def set_interval():
    pass

def take_photo(chosen_res, save_path ='./photos/'):
    # Check for path
    os.makedirs(save_path, exist_ok = True)

    # Initialize the camera
    cap = cv2.VideoCapture(0)
    # Check if the webcam is opened correctly
    if not cap.isOpened():
        logger.error('Cannot open webcam')
        raise IOError('Cannot open webcam')

    # Set values from chosen_res to the cv2 object
    set_resolution(cap, chosen_res[0], chosen_res[1])

    ### TIMERS
    cam = time.time()
    camTime = cam - start
    logger.info(f'Camera open in : {str(camTime)[:7]} seconds')
    print(f'Camera open in : {str(camTime)[:7]} seconds') # ~90 s in desktop

    ret, frame = cap.read()
    now = datetime.now(timezone.utc).isoformat(timespec='milliseconds')
    filename = now.replace(':', '-').replace('.', '-')
    filename = filename[:-6]
    filename += 'Z.jpg'
    full_path = os.path.join(save_path, filename)

    if ret:
        cv2.imwrite(full_path, frame)
        logger.info(f'Photo taken and saved at {full_path} with resolution {chosen_res[0]}x{chosen_res[1]}.')
        print(f'Photo taken and saved at {full_path} with resolution {chosen_res[0]}x{chosen_res[1]}.')
    else:
        logger.error('Failed to take photo')
        print('Failed to take photo.')

    # Release the camera
    logger.info('Camera released.')
    cap.release()

def get_user_res(res_options):

    prompt = 'Choose a resolution between the options given:\n'
    for key, value in res_options.items():
        prompt += f'\t{key}): {value[0]} x {value[1]}\n'
    prompt += '\t>> '

    choice = input(prompt)

    while choice not in res_options:
        logger.warning('Invalid option for resolution.')
        print('Chosen option not supported, please try again.\n')
        choice = input(prompt)

    return choice

### TIMERS
start = time.time()
logger.info(f'Program started at timestamp: {str(start)}')
print(f'Program started at timestamp: {str(start)}') # my machine is slow


### Ask users
user_res = get_user_res(res_options)
res = res_options[user_res]
take_photo(res)

### TIMERS
end = time.time()
excTime = end - start
logger.info(f'Program executed in {str(excTime)[:7]} seconds.')
print (str(excTime)[:7])
print('###END')
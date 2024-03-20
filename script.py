import sys
import subprocess

modules = {
    'cv2': 'opencv-python',  # 'cv2' is part of the 'opencv-python' package
    # Standard library modules don't need to be checked for installation, but listed here for clarity
    'datetime': None,  # Part of the Python Standard Library
    'time': None,      # Part of the Python Standard Library
    'os': None,        # Part of the Python Standard Library
    'logging': None,   # Part of the Python Standard Library
    'gzip': None,      # Part of the Python Standard Library
    'shutil': None,    # Part of the Python Standard Library
}
for module, package in modules.items():
    try:
        # Try to import the module
        __import__(module)
        print(f'{module} is already installed in this machine.')
    except ImportError as e:
        if package:
            # If the module is not found, and it's not part of the standard library (has a specified package), install it
            print(f'{module} not found, installing {package}...')
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
        else:
            print(f'Error importing {module}, but it is part of the Python Standard Library. Error: {e}')

import cv2
import time
import os
import logging
import gzip
import shutil

from datetime import datetime
from logging.handlers import BaseRotatingHandler

######
### Setup parameters, change this variables in order to change main functionalities acording to the hardware available

MAX_LOGGER_LINES = 1500

MAX_PHOTOS_ALLOWED = 100

MAX_INTERVAL_TIME = 21600

RES_OPTIONS = {
    '1' : [1920, 1080],
    '2' : [1280, 720],
    '3' : [720, 480],
    '4' : [640, 360]
}

LOGS_PATH = './logs'

PHOTOS_PATH ='./photos/'

### End of setup parameters
######

user_res = [0, 0] # Will store one of the values in RES_OPTIONS

photos_to_take = 1 # Gets stored as INT from get_user_photos()

interval = 1 # Wait time between photos in seconds,
             # gets stored as INT from get_user_interval()

# Custom format for dates
class MyFormatter(logging.Formatter):
    # Override the converter in logging.Formatter
    converter = datetime.fromtimestamp
    # Override formatTime in logging.Formatter
    def formatTime(self, record, datefmt = None):
        return self.converter(record.created).astimezone().isoformat()
# Custom log rotation handler
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
        # Compress the oldest file just before it's rotated out
        oldest_file = f'{self.baseFilename}.{self.backupCount}'
        if os.path.exists(oldest_file):
            with open(oldest_file, 'rb') as f_in:
                with gzip.open(f'{oldest_file}.gz', 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            os.remove(oldest_file)  # Remove the original to save space

        dfn = self.rotation_filename(f'{self.baseFilename}.1')
        if os.path.exists(dfn):
            os.remove(dfn)
        self.rotate(self.baseFilename, dfn)

        if not self.delay:
            self.stream = self._open()
        self.counter = 0  # Reset counter

# Set hardware
def set_resolution(cap, width, height):
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    logger.info(f'Resolution set to {width} x {height}.')

def take_photo(chosen_res, PHOTOS_PATH):
    # Check for path
    os.makedirs(PHOTOS_PATH, exist_ok = True)
    # Camera timer (this was implemented because severely affects performance and needed to get track)
    cam = time.time()
    # Initialize the camera
    cap = cv2.VideoCapture(0)
    # Check if the webcam is opened correctly
    if not cap.isOpened():
        logger.error('Cannot open webcam')
        raise IOError('Cannot open webcam')
    # Set values from chosen_res to the cv2 object
    set_resolution(cap, chosen_res[0], chosen_res[1])
    # End Camera timer
    camTime = time.time()
    camTime = camTime - cam
    logger.info(f'Camera setup completed in : {str(camTime)[:7]} seconds')

    ret, frame = cap.read()
    now = datetime.now().astimezone().isoformat(timespec = 'milliseconds')
    # Replace characters not supported in filenames
    filename = now.replace(':', '-').replace('.', '-')
    filename += '.jpg'
    full_path = os.path.join(PHOTOS_PATH, filename)

    if ret:
        cv2.imwrite(full_path, frame)
        print(f'Photo taken and saved at {full_path} with resolution {chosen_res[0]}x{chosen_res[1]} px.')
        logger.info(f'Photo taken and saved at {full_path} with resolution {chosen_res[0]}x{chosen_res[1]} px.')
    else:
        logger.error('Failed to take photo.')

    # Release the camera
    cap.release()
    logger.info('Camera released.')

def get_user_res(RES_OPTIONS):

    prompt = 'Choose a resolution between the options given:\n'
    for key, value in RES_OPTIONS.items():
        prompt += f'\t{key}): {value[0]} x {value[1]}\n'
    prompt += '\t>> '

    choice = input(prompt)

    # Input validation
    while choice not in RES_OPTIONS:
        logger.warning('Invalid option for resolution.')
        print('Chosen option not supported, please try again.\n')
        choice = input(prompt)

    logger.info(f'Choice valid, resolution option {choice} selected.')
    return choice

def get_user_photos():

    prompt = 'Type how many photos you need in total:\n\t>> '
    choice = input(prompt)

    # Input validation
    while not choice.isnumeric():
        logger.warning('Invalid option for number of photos.')
        print('Chosen option not supported, please try again.\n')
        choice = input(prompt)

    choice = int(choice)
    while choice > MAX_PHOTOS_ALLOWED:
        logger.warning('Too much photos requested.')
        print('Chosen option not supported, please ask for less photos.\n')
        choice = input(prompt)
        choice = int(choice)

    logger.info(f'Choice valid, {choice} photo(s) requested.')
    return choice

def get_user_interval():

    prompt = 'Type how many seconds to wait between each photo:\n\t>> '
    choice = input(prompt)

    # Input validation
    while not choice.isnumeric():
        logger.warning('Invalid option for interval time.')
        print('Chosen option not supported, please try again.\n')
        choice = input(prompt)

    choice = int(choice)
    while choice > MAX_INTERVAL_TIME:
        logger.warning('Too much wait time requested.')
        print('Chosen option not supported, please shorten time between photos.\n')
        choice = input(prompt)
        choice = int(choice)

    logger.info(f'Choice valid, {choice} interval second(s) requested.')
    return choice

# Start timer
start = time.time()
camTime = start
# Create logs and photos directories
os.makedirs(LOGS_PATH, exist_ok = True)
os.makedirs(PHOTOS_PATH, exist_ok = True)

# Set up logging
log_filename = os.path.join(LOGS_PATH, 'webcam_capture.log')
logger = logging.getLogger('WebcamCaptureLogger')
logger.setLevel(logging.DEBUG)

handler = MaxLinesRotatingFileHandler(log_filename, maxLines = MAX_LOGGER_LINES, backupCount = 5)
handler.setLevel(logging.DEBUG)
user_name = os.getlogin() # Get who is using the script
formatter = MyFormatter(f'%(asctime)s - {user_name} - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# First log entry
logger.info(f'Program started!')

# Ask users params
photos_to_take = get_user_photos()

if photos_to_take == 1:
    user_res = get_user_res(RES_OPTIONS)
else:
    interval = get_user_interval()
    user_res = get_user_res(RES_OPTIONS)

res = RES_OPTIONS[user_res] # See user_res declaration at line 33

if photos_to_take == 1:
    take_photo(res, PHOTOS_PATH)
else:
    # Loop for taking more than photos
    for i in range(photos_to_take):

        take_photo(res, PHOTOS_PATH)
        logger.info('Interval started.')
        time.sleep(interval)
        logger.info('Interval ended.')

# End timers
end = time.time()
excTime = end - start
logger.info(f'Program executed in {str(excTime)[:7]} seconds.')
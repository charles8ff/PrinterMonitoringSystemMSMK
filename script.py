import cv2 #for camera #pip install opencv-python
from datetime import datetime
import time
import os
import logging
from logging.handlers import BaseRotatingHandler
import gzip
import shutil

######
### Setup parameters, change this variables in order to change main functionalities acording to the hardware available

max_logger_lines = 30

max_photos_allowed = 100

max_interval_time = 21600

res_options = {
    '1' : [1920, 1080],
    '2' : [1280, 720],
    '3' : [720, 480],
    '4' : [640, 360]
}

logs_path = './logs'
save_path ='./photos/'


### End of setup parameters
######

chosen_res = [0, 0]

photos_to_take = 1 # Gets passed as an INT

interval = 1 # wait time between photos in seconds?

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

# Create logs and photos directories
os.makedirs(logs_path, exist_ok = True)
os.makedirs(save_path, exist_ok = True)
# Set up logging
log_filename = os.path.join(logs_path, 'webcam_capture.log')
logger = logging.getLogger('WebcamCaptureLogger')
logger.setLevel(logging.DEBUG)

handler = MaxLinesRotatingFileHandler(log_filename, maxLines = max_logger_lines, backupCount = 5)
handler.setLevel(logging.DEBUG)
user_name = os.getlogin() # Get who is using the script
formatter = MyFormatter(f'%(asctime)s - {user_name} - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)

def set_resolution(cap, width, height):
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    logger.info(f'Resolution set to {width}x{height}')

def set_interval():
    pass

def take_photo(chosen_res, save_path):
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
    print(f'Camera open in : {str(camTime)[:7]} seconds')

    ret, frame = cap.read()
    now = datetime.now().astimezone().isoformat(timespec = 'milliseconds')
    # Replace characters not supported in filenames
    filename = now.replace(':', '-').replace('.', '-')
    filename += '.jpg'
    full_path = os.path.join(save_path, filename)

    if ret:
        cv2.imwrite(full_path, frame)
        logger.info(f'Photo taken and saved at {full_path} with resolution {chosen_res[0]}x{chosen_res[1]} px.')
        print(f'Photo taken and saved at {full_path} with resolution {chosen_res[0]}x{chosen_res[1]} px.')
    else:
        logger.error('Failed to take photo.')
        print('Failed to take photo.')

    # Release the camera
    cap.release()
    logger.info('Camera released.')

def get_user_res(res_options):

    prompt = 'Choose a resolution between the options given:\n'
    for key, value in res_options.items():
        prompt += f'\t{key}): {value[0]} x {value[1]}\n'
    prompt += '\t>> '

    choice = input(prompt)

    # Input validation
    while choice not in res_options:
        logger.warning('Invalid option for resolution.')
        print('Chosen option not supported, please try again.\n')
        choice = input(prompt)

    logger.info(f'Choice valid, resolution option {choice} selected.')
    return choice

def get_user_photos():
    prompt = 'Type how many photos you need in total:\n\t>>'
    choice = input(prompt)

    # Input validation
    while not choice.isnumeric():
        logger.warning('Invalid option for number of photos.')
        print('Chosen option not supported, please try again.\n')
        choice = input(prompt)

    choice = int(choice)
    while choice > max_photos_allowed:
        logger.warning('Too much photos requested.')
        print('Chosen option not supported, please ask for less photos.\n')
        choice = input(prompt)
        choice = int(choice)

    logger.info(f'Choice valid, {choice} photo(s) requested.')
    return choice

def get_user_interval():
    prompt = 'Type how many seconds to wait between each photo:\n\t>>'
    choice = input(prompt)

    # Input validation
    while not choice.isnumeric():
        logger.warning('Invalid option for interval time.')
        print('Chosen option not supported, please try again.\n')
        choice = input(prompt)

    choice = int(choice)
    while choice > max_interval_time:
        logger.warning('Too much wait time requested.')
        print('Chosen option not supported, please shorten time between photos.\n')
        choice = input(prompt)
        choice = int(choice)

    logger.info(f'Choice valid, {choice} interval second(s) requested.')
    return choice

start = time.time()
logger.info(f'Program started!.')

### TBDeleted
print(f'Program started at timestamp: {str(start)}') # My machine is slow :(

# Ask users params
photos_to_take = get_user_photos()
interval = get_user_interval()
user_res = get_user_res(res_options)

res = res_options[user_res]

for i in range(photos_to_take):

    take_photo(res, save_path)
    logger.info('Interval started.')
    time.sleep(interval)
    logger.info('Interval ended.')

end = time.time()
excTime = end - start
logger.info(f'Program executed in {str(excTime)[:7]} seconds.')
### TBDeleted
print (str(excTime)[:7])
print('###END')
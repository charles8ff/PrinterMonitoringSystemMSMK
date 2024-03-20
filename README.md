# Printer Monitoring System

> Assignment Brief 1  - Advanced Operating Systems - BBSc (Hons) Computer Forensics and Security

## Table of Contents

1. [Project Description](#project-description)
2. [Technologies Applied](#technologies-applied)
3. [Branches Usage](#branches-usage)
4. [Credits](#credits)
5. [Additional Documentation](#additional-documentations)

## Project Description

This project aims to take photos of the main camera of the machine, with the user being _able to choose_ the resolution from a given list of options, the number of photos and interval between them.

The script has some constants (showed below) that could be changed depending on the hardware performance, but I have set them according to the specifications given by the instructions.

```python
# this is at line 37 of script.py
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
```

All the files created by the script will be stored in folders in the working directory of the script unless stated otherwise in the setup constants mentioned above.

## Technologies Applied

For the challenges that were approached, I have chosen to work with an Open Source library called [OpenCV](https://docs.opencv.org/4.x/index.html), that grans acces to the webcam of the machine and is able to open a video stream and take frames for a specified duration. Then, using the integrated Python logging resources I have fullfilled the logging and log rotation requirements.

_Git_ as the version control software and _GitHub_ as an online repository have been used to keep track of changes in the code and to have access to the code from different machines in order to test the script under different circumstances.

## Branches Usage

There are 2 branches in this project, the `main` branch will carry the README.md updates and the merging updates from the `dev` branch, where new functionalities will be implemented.

The standard procedure will always be to merge `main` into `dev` **first** to avoid possible conflicts, fix them in the axuliar branch, and thus keeping branch `main` clean.

## Credits

I have used the Python Documentation about [Logging Handlers](https://docs.python.org/3/howto/logging.html#useful-handlers) in order to overload some methods of _**BaseRotatingHandler()**_.

I have used the [OpenCV documentation](https://docs.opencv.org/4.x/index.html) in order to setup the webcam resolution and gain access safely to the webcam.

I have consulted many sites and resources, including this [Stack Overflow post](https://stackoverflow.com/questions/63501504/python-logging-iso8601-timestamp-with-milliseconds-and-timezone-using-config-fi) that had a very similar approach to use the ISO8601 in the logs.

## Additional Documentations

Further reading at CCCU Blackboard under the instructions of the assignment.

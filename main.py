import numpy as nm
import pytesseract
import time
import ctypes
import datetime
import logging
import os
from PIL import ImageGrab, ImageOps, Image
SETTINGS = {
        "tesseract_path": r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe',
        "box_coords_x1": 46,
        "box_coords_y1": 1263,
        "box_coords_x2": 273,
        "box_coords_y2": 1318,
}
# Box co-ordinated per resolutions running fullscreen - For having the beta client at full screen.
# (x1, y1, x2, y2)
# 46, 1263, 273, 1318 (2560x1440) | 41, 903, 308, 958 (1920x1080)
pytesseract.pytesseract.tesseract_cmd = SETTINGS["tesseract_path"] # Set the tesseract path
logging.basicConfig(filename='console.log',level=logging.DEBUG) # Setup logging

def log(message):
        now = datetime.datetime.now()
        print(f'{now.strftime("%H:%M:%S [%d.%m.%Y]")} | {message}')
        logging.debug(f'{now.strftime("%H:%M:%S [%d.%m.%Y]")} | {message}')

def click(x, y):
        ctypes.windll.user32.SetCursorPos(x, y)
        ctypes.windll.user32.mouse_event(2, 0, 0, 0,0) # left down
        ctypes.windll.user32.mouse_event(4, 0, 0, 0,0) # left up

def capture():
        image = ImageGrab.grab(bbox =((SETTINGS["box_coords_x1"],SETTINGS["box_coords_y1"],SETTINGS["box_coords_x2"],SETTINGS["box_coords_y2"])))
        image.save("capture.jpg")
        image = Image.open("capture.jpg")
        image = ImageOps.grayscale(image)
        image.save('capture.jpg')
        stringFound = pytesseract.image_to_string(nm.array(image), lang ='eng').upper().split()
        os.remove("capture.jpg")
        return stringFound


file = open("console.log","r+")
file.truncate(0)
file.close()
log('COD Updater Log Initialised.')

while(True):
        imageStr = capture()
        time.sleep(1)
        log(f'DEBUG: Current Text: {imageStr}')
        if "PLAY" not in imageStr:
                click(115, 1270)
                log('INFO: Click Attempted.')
        elif "UPDATING" in imageStr:
                log('============================== SUCCESS ==============================\INFO: Update Initialised.')
                break
        time.sleep(60)
import numpy as nm
import pytesseract
import time
import ctypes
import datetime
import logging
import os
from PIL import ImageGrab
SETTINGS = {
        "tesseract_path": r'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe',
        "box_coords_x1": 46,
        "box_coords_y1": 1263,
        "box_coords_x2": 273,
        "box_coords_y2": 1318,
}
# Box co-ordinated per resolutions running fullscreen (personal)
# (x1, y1, x2, y2)
# 46, 1263, 273, 1318 - for 2560x1440 displays
# 41, 903, 308, 958 - for 1920x1080 displays
# 42, 902, 310, 958 - this is for when it decides to change your resolution
pytesseract.pytesseract.tesseract_cmd = SETTINGS["tesseract_path"] # Set the tesseract path
logging.basicConfig(filename='console.log',level=logging.DEBUG) # Setup logging

######################################################################################################################################################################
##############################################################################FUNCTIONS###############################################################################
######################################################################################################################################################################
def log(message):
        now = datetime.datetime.now()
        print(f'{now.strftime("%H:%M:%S [%d.%m.%Y]")} | {message}')
        logging.warning(f'{now.strftime("%H:%M:%S [%d.%m.%Y]")} | {message}')

def click(x, y):
        ctypes.windll.user32.SetCursorPos(x, y)
        ctypes.windll.user32.mouse_event(2, 0, 0, 0,0) # left down
        ctypes.windll.user32.mouse_event(4, 0, 0, 0,0) # left up

def takeCap():
        capcoords = (SETTINGS["box_coords_x1"],SETTINGS["box_coords_y1"],SETTINGS["box_coords_x2"],SETTINGS["box_coords_y2"])
        image = ImageGrab.grab(bbox =(capcoords))
        image.convert('L')
        image.save("cap.jpg")
        # ImageGrab-To capture the screen image in a loop.  
        # Bbox used to capture a specific area. 
        image = ImageGrab.grab(bbox =(capcoords)) 
        # Get the time
        now = datetime.datetime.now()
        # Converted the image to monochrome for it to be easily  
        # read by the OCR and obtained the output String. 
        imageAsString = pytesseract.image_to_string(nm.array(image),  
                lang ='eng')
        return imageAsString # Return the image converted string

def Initialise():
        # clear the log file
        file = open("console.log","r+")
        file.truncate(0)
        file.close()
        # Thing to tell user its started
        log('============================== RUNNING ==============================')
        log('COD Updater log initialised.')
        log('=====================================================================')

######################################################################################################################################################################
##############################################################################MAIN CODE###############################################################################
######################################################################################################################################################################
Initialise()

# THE WHILE LOOP -- MAIN CODE
# Finds button, if button does not equal PLAY then it'll click then check if it says Updating, if not then restart loop else break it.
while(True):
        tesstr = takeCap()
        if tesstr != "PLAY":
                log(f'String found: "{tesstr}"') # Debugging purposes
                click(115, 1270)
                log('Potential update button pressed.')
                time.sleep(10)
                os.remove("cap.jpg")
                takeCap()
                if tesstr != "UPDATING":
                        log(f'Update button not found, instead found: "{tesstr}". Retrying.')
                else: # if update is found
                        log('============================== SUCCESS ==============================')
                        log(f'Update button found and update started. | Text Found: "{tesstr}"')
                        log('=====================================================================')
                        os.remove("cap.jpg")
                        break
        else:
                time.sleep(60) # A cooldown for another check
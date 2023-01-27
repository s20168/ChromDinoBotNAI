import numpy as np
import cv2
from PIL import ImageGrab

# We created class objects from the images folder which contains info such as width, height of the object and location of the object
class Object:

    def __init__(self, path):
        img = cv2.imread(path, 0)
        self.img = img
        self.width = img.shape[1]
        self.height = img.shape[0]
        # We don't know the location until matching it with the screenshot
        self.location = None
    # Function to match the object in the screenshot and to create the location of the object
    def match(self, scr):
        # We use matchTemplate method to match the object
        # It contains args: screenshot were our obj is located, object image, formula for matching
        res = cv2.matchTemplate(scr, self.img, cv2.TM_CCOEFF_NORMED)
        minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(res)
        # coordiantes
        startLoc = maxLoc
        endLoc = (startLoc[0]+self.width, startLoc[1]+self.height)

        if maxVal>0.8:
            self.location = (startLoc, endLoc)
            return True
        else:
            self.location = None
            return False

# Function that takes a screenshot of the screen
def grabScreen(bbox=None):
    img = ImageGrab.grab(bbox=bbox)
    img = np.array(img)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    return img
import cv2
import numpy as np

class ImageProcessor:
    def __init__(self):
        self.dim = 64
        self.yellow_mask = None
        self.red_mask = None
        self.green_mask = None
        self.blue_mask = None
        self.white_mask = None

    def getYellow(self, frame):
        img_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) # Convert BGR to HSV
        
        # define range of yellow color in HSV
        lower = np.array([22, 93, 0], dtype="uint8")
        upper = np.array([45, 255, 255], dtype="uint8")
        
        # Threshold the HSV image to get only yellow colors
        mask = cv2.inRange(img_hsv, lower, upper)
        self.yellow_mask = mask

    def getRed(self, frame):
        img_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) # Convert BGR to HSV
    
        # define range of red color in HSV
        lower = np.array([155,25,0], dtype="uint8")
        upper = np.array([179,255,255], dtype="uint8")
        
        # Threshold the HSV image to get only red colors
        mask = cv2.inRange(img_hsv, lower, upper)
        self.red_mask = mask

    def getGreen(self, frame):
        img_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) # Convert BGR to HSV
    
        # define range of green color in HSV
        lower = np.array([36,25,25], dtype="uint8")
        upper = np.array([70,255,255], dtype="uint8")
        
        # Threshold the HSV image to get only green colors
        mask = cv2.inRange(img_hsv, lower, upper)
        self.green_mask = mask

    def getBlue(self, frame):
        img_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) # Convert BGR to HSV
    
        # define range of blue color in HSV
        lower = np.array([90,105,111], dtype="uint8")
        upper = np.array([110,185,191], dtype="uint8")
        
        # Threshold the HSV image to get only blue colors
        mask = cv2.inRange(img_hsv, lower, upper)
        self.blue_mask = mask

    def getWhite(self, frame):
        img_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) # Convert BGR to HSV
    
        # define range of white color in HSV
        lower = np.array([0,0,168], dtype="uint8")
        upper = np.array([172,111,255], dtype="uint8")
        
        # Threshold the HSV image to get only white colors
        mask = cv2.inRange(img_hsv, lower, upper)
        self.white_mask = mask

    def getBoundingBoxes(self, color):
        mask = None
        if color == "yellow":
            mask = self.yellow_mask
        elif color == "red":
            mask = self.red_mask
        elif color == "green":
            mask = self.green_mask
        elif color == "blue":
            mask = self.blue_mask
        else:
            mask = self.white_mask
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10] #only consider best 10
        boxes = []
        for contour in contours:
            if len(boxes)>5:
                break
            rect = cv2.boundingRect(contour)
            x, y, w, h = rect
            if w < 40 or h < 40: # too small, ignore
                continue
            if w > 200 or h > 200: # too big, likely to be not our target
                continue
            if w > 1.5*h or h > 1.5*w: # not proportional, not square (80% allowance)
                continue
            #give some extra space/padding of 5%
            #extra_width = int(0.05*w)
            #extra_height = int(0.05*h)
            #new_x = max(0, x-extra_width)
            #new_y = max(0, y-extra_height)
            #rect = (new_x, new_y, w+2*extra_width, h+2*extra_height)
            boxes.append(np.array(rect))
        return np.array(boxes)

    def resizeNormalize(self, frame, channels):
        resized = cv2.resize(frame, dsize=(self.dim, self.dim), interpolation=cv2.INTER_CUBIC)
        resized = np.reshape(resized, newshape=(1,self.dim,self.dim,channels))/255
        return resized
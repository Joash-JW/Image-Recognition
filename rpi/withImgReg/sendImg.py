import time, pickle, requests, threading
from picamera import PiCamera
from picamera.array import PiRGBArray

class sendImg:
  def __init__(self):
    self.count = 0

    # camera initialisation
    self.camera = PiCamera()
    self.camera.exposure_mode = "sports"
    self.camera.resolution = (640, 480)
    self.output = PiRGBArray(self.camera)

    # start camera preview to let camera warm up
    self.camera.start_preview()
    threading.Thread(target=time.sleep, args=(2,)).start()

  # this function takes a picture when commanded
  def takePic(self):
    self.camera.capture(self.output, 'bgr')
    frame = self.output.array
    self.output.truncate(0)
    self.count += 1
    data = pickle.dumps(frame)
    # send to Laptop via HTTP POST
    r = requests.post("http://192.168.16.133:8123", data=data) #static IP
    print("Image", self.count, "sent")

import cv2
import matplotlib.pyplot as plt
import numpy as np
import subprocess as sub


exp_val = -4

value = 10000
sub.run(["v4l2-ctl", "-d", "/dev/video0", "-c", "auto_exposure=1", "-c", f"exposure_time_absolute={value}"])

i = True
while i:
    i = True

cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_EXPOSURE, exp_val)
ret, frame = cam.read()


img = np.uint8(frame)

countI = img.astype(np.float32)
countI[countI <= 254] = 0
overexposedPixelNumber = np.sum(countI > 254)
meanValue = np.mean(img)

print("Mean Value: ",meanValue)
print("Overexposed Pixel Number: ",overexposedPixelNumber)
print("Exposure value: {}".format(exp_val))

if not ret:
    print("Fehler beim Aufnehmen des Bildes. Bitte erneut versuchen.")
  

img_name = "picture_{}.bmp".format(exp_val)
cv2.imwrite(img_name,frame)

cam.release()
cv2.destroyAllWindows() 


import cv2
import numpy as np
import subprocess as sub
import time

def cam_setup():
    sub.run(["v4l2-ctl", "-d", "/dev/video0", "-c", "auto_exposure=1"])
    sub.run(["v4l2-ctl", "-d", "/dev/video0", "-c", "exposure_time_us=5000"])
    #sub.run()
    print("Camera Ok")
    #also possible to implement gain etc, see v4l2-ctl --device /dev/video0 --all

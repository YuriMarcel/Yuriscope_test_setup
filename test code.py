#!/usr/bin/env phyton3
import serial
import time
import numpy as np
import os
import subprocess as sub
import cv2

start_time=time.time()
ser_motor = serial.Serial('/dev/ttyUSBM1', 115200, timeout=1.0)
ser_led1 = serial.Serial('/dev/ttyUSBL1', 115200, timeout=1.0)
ser_led2 = serial.Serial('/dev/ttyUSBL2', 115200, timeout=1.0)
ser_led3 = serial.Serial('/dev/ttyUSBL3', 115200, timeout=1.0)
ser_led4 = serial.Serial('/dev/ttyUSBL4', 115200, timeout=1.0)
ser_led5 = serial.Serial('/dev/ttyUSBL5', 115200, timeout=1.0)
time.sleep(3)

led_list = [{"ser_led1":ser_led1}, {"ser_led2":ser_led2}, {"ser_led3":ser_led3}, {"ser_led4":ser_led4}, {"ser_led5":ser_led5}]

ser_motor.reset_input_buffer()
for ser in led_list:
    for key, value in ser.items():
        var_name = key
        led_control = value
        led_control.reset_input_buffer()
        led_control.write("000".encode('utf-8'))
print("Serial OK")

#Camera setup - resolution
"""
try:
    # Versuchen Sie, die Kamera mit dem Index 1 zu öffnen
    cam = cv2.VideoCapture(1)
    if not cam.isOpened():
        raise ValueError('Kamera 1 konnte nicht geöffnet werden')
    print('Kamera 1 wurde erfolgreich geöffnet')
except (cv2.error, ValueError):
    # Falls die Kamera mit dem Index 1 nicht geöffnet werden kann, öffnen Sie die Kamera mit dem Index 0
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        raise ValueError('Kamera 0 konnte nicht geöffnet werden')
    print('Kamera 0 wurde erfolgreich geöffnet')
"""

cam = cv2.VideoCapture(0)

cam.set(cv2.CAP_PROP_FRAME_WIDTH, 4000)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 3000)
cam.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0) #exposure time

cam.set(cv2.CAP_PROP_EXPOSURE, 5000) #exposure time

#cv2.imshow('Live Cam',frame)

#Distances setup
stepper_series1 = np.arange(80000,81000,50)
stepper_series2 = np.arange(90000,91000,50)

#Create path of test run
path = "/home/rm/microscope/test_run_with_lid_103"
os.makedirs(path, exist_ok=True)

def open_close_led_serial(operation):
    for ser in led_list:
        for key, value in ser.items():
            var_name = key
            led_control_2 = value
            if operation == "open":
                led_control_2.open()
                led_control_2.reset_input_buffer()
                led_control_2.write("000".encode('utf-8'))
                #print("opened")
            elif operation == "close":
                led_control_2.close()
                #print("closed")
while True:
    x = input("Input to Arduino:  ")
    ser_motor.write(str(x).encode('utf-8'))
    time.sleep(0.01)

    #Output from Arduino
    while True:
        if ser_motor.in_waiting > 0:
            line = ser_motor.readline().decode('utf-8')
            if line.find("x") > -1:
                break
            print(line)
        time.sleep(0.01)


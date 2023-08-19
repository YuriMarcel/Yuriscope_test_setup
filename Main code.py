import time
import os
import json
import functions as f
import subprocess as sub

#picture = "/home/rm/Desktop/Yuriscope_pictures/Blood_cells_1/pictures/LED_1101.bmp"
#print(f.analyze_image_path(picture))
folder = "/home/rm/Desktop/Yuriscope_pictures/NEMUCO_cells_2"
if not os.path.exists(folder):
    os.makedirs(folder)
infos_path = os.path.join(folder, "info.txt")
exposure_path = os.path.join(folder, "led_exposure.txt")
print(exposure_path)
#loaded path
#exposure_path = "/home/rm/Desktop/Yuriscope_pictures/Blood_cells_1/led_exposure.txt"


#setup seriell communication
ser_motor,ser_led2,ser_led1345 = f.setup_com()
f.cam_setup()


##for mounting the Sample/CC, the motors go as far apart as possible
#mounting = input("Do you wanna start the mounting procedure? \n[y/n]    :")

#if mounting == "y":
    #start mounting procedure 
 #   f.mounting_procedure(ser_motor)

#user input
[find_ROI, Beamcenter_set, exposure_set, pattern, Cam_total, Cam_steps, LED_total, LED_steps] = f.get_user_input()

#set camera up the observe ROI
if find_ROI == "yes":
    f.find_ROI(ser_led1345)

#change LED Position to find Beamcenter
if Beamcenter_set != "skip":
    f.find_beamcenter(folder,infos_path,Beamcenter_set,ser_led1345)

#get exposure values for each LED
if exposure_set== "Get new values":
    f.LED_control(ser_led1345,"1101")
    f.find_exposure_manually(ser_led2,ser_led1345,exposure_path)
    exposure_times = f.read_exposure_times(exposure_path)
     
elif exposure_set == "Load from given path":
    exposure_times = f.read_exposure_times(exposure_path)
    mean = sum(float(value) for value in exposure_times.values()) / len(exposure_times)
    print(f"Mean exposure value: {mean}")

#start image acquisition 
if pattern == "80 LEDs individualy":
    f.LED80_sequence(exposure_times,folder,ser_led2,ser_led1345)
else:
    print("No other pattern implemented :/")

print("finished :)")













"""
for i in range(1101, 1117):
    LED = str(i)    
    try:
        while True:
            value = int(input("Exposure time in ms: "))
            #print(value)
            f.exposure_tests(ser_led1345,LED,value)
    except KeyboardInterrupt:
            f.LED_control(ser_led1345,"0000")
            continue

while True:
    x = input("Input to Arduino: ")
    ser_motor.write(str(x).encode('utf-8'))
    time.sleep(0.01)

    # Output from Arduino
    while True:
        if ser_motor.in_waiting > 0:
            line = ser_motor.readline().decode('utf-8')
            if line.find("x") > -1:
                break
            print(line)
        time.sleep(0.01)


not_working_leds, working_leds = f.test_leds(ser_led2,ser_led1345)

print("Working LEDs:", working_leds)
print("Not working LEDs:", not_working_leds)

"""
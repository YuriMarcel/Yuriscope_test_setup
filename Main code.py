import os
import functions as f


folder = "/home/rm/Desktop/Yuriscope_pictures/DLR_Spores 4/"
if not os.path.exists(folder):
    os.makedirs(folder)
infos_path = os.path.join(folder, "info.txt")
exposure_path = os.path.join(folder, "led_exposure.txt")

#%%

#setup seriell communication and homing position
ser_motor,ser_led2,ser_led1345 = f.setup_com()
f.move_motor(ser_motor,"start")
f.cam_setup()

#%%
#exposure_times = f.read_exposure_times(exposure_path)
#print(exposure_times)
#f.check_exposure_values(ser_led2, ser_led1345,exposure_times)

#f.get_exposure_values_p_control(ser_led1345, ser_led2, exposure_path)
# Durchschnittlicher Pixelversatz in x-Richtung: 2.9083635012308755 -> versatz zwischen 3.01 bis 3.04 
# also insgesamt um 11,6 pixel = 21.46um verschieben
# Durchschnittlicher Pixelversatz in y-Richtung: 0.007958851754665375

#f.get_pixelshift_LED(ser_led1345)

##for mounting the Sample/CC, the motors go as far apart as possible
try:
    mounting = input("Do you wanna start the mounting procedure? \n[y/n]    :")

    if mounting == "y":
        f.mounting_procedure(ser_motor)

    
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
        #loaded path
        exposure_path = "/home/rm/Desktop/Yuriscope_pictures/NEMUCO_cells_2/led_exposure.txt"
        exposure_times = f.read_exposure_times(exposure_path)
        mean = sum(float(value) for value in exposure_times.values()) / len(exposure_times)
        print(f"Mean exposure value: {mean}")

    elif exposure_set == "check values":
        exposure_times = f.read_exposure_times(exposure_path)
        f.check_exposure_times(exposure_times, ser_led2, ser_led1345)

    #start image acquisition 
    if pattern == "80 LEDs individualy":
        f.LED80_sequence(exposure_times,folder,ser_led2,ser_led1345)
    else:
        print("No other pattern implemented :/")

    print("finished :)")

except KeyboardInterrupt:
    print("stop")
    #implement that everything should stop
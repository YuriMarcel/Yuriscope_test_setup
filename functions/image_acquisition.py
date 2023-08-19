import functions as f
import os
def LED80_sequence(exposure_times,folder,ser_led2,ser_led1345):

    picture_path = os.path.join(folder, "pictures")
    if not os.path.exists(picture_path):
        os.makedirs(picture_path)

    for led_list, exposure_time in exposure_times.items():
        # Ändern Sie den LED-Namen von 1.12 zu 1112
        LED = led_list.replace(".", "1")
        
        if LED[0] == "2":
            f.LED_control(ser_led2,LED)
        else:
            f.LED_control(ser_led1345,LED)
        
        exposure_time_us = int(exposure_time * 1000)
        f.set_exposure(exposure_time_us)

        #check if exposure value ist right
        if exposure_time == f.get_exposure() / 1000:
            print(f"LED {LED} exposure time changed to {exposure_time} ms")

        f.save_image(picture_path, LED)

        if LED[0] == "2":
            f.LED_control(ser_led2,"0000")
        else:
            f.LED_control(ser_led1345,"0000")
        
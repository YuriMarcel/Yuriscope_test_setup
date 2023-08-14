import time
import cv2
import functions as f


#setup seriell communication
ser_motor = f.setup_com()

#vid = f.auto_adjust_exposure()

#f.get_beam_center(vid)




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


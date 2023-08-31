import serial
import time

def move_motor(ser_motor,position):
    
    if position == "start":
        ser_motor.write(position.encode('utf-8'))
        while True:
            data_received = ser_motor.readline().decode('utf-8').strip()
            if data_received == "Homing completed!":
                #print(data_received)
                break
            time.sleep(0.01)
    else:
        position = adjust_value(position)
        ser_motor.write(position.encode('utf-8'))
        #Output from Arduino
        print("function called")
 
        while True:
            data_received = ser_motor.readline().decode('utf-8').strip()
            if data_received == "finished":
                #print(data_received)
                break
            time.sleep(0.01)

def mounting_procedure(ser_motor):
    
    move_motor(ser_motor,"925000")
    move_motor(ser_motor,"820000")
    
    answer = input("Return back to Home? \n[y/n]:    ")

    if answer == "y":
        move_motor(ser_motor,"90000")
        move_motor(ser_motor,"80000")

    print("continue with next steps :)")

def adjust_value(val):
    first_digit = int(str(val)[0])  # Erste Ziffer extrahieren
    remainder = int(str(val)[1:])  # Den Rest des Strings extrahieren und in eine Zahl umwandeln
    adjusted_remainder = int(remainder * 0.8)  # Multiplizieren Sie mit 0,8
    return str(first_digit) + str(adjusted_remainder)  # Kombinieren Sie die erste Ziffer mit dem angepassten Rest
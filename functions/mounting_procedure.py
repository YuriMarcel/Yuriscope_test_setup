import serial
import time

def mounting_procedure(ser_motor):
    ser_motor.write("start".encode('utf-8'))
    time.sleep(0.01)
    
    #Output from Arduino
    while True:
        if ser_motor.in_waiting > 0:
            line = ser_motor.readline().decode('utf-8')
            if line.find("x") > -1:
                break
            print(line)
        time.sleep(0.01)

    ser_motor.write("899999".encode('utf-8'))
    #Output from Arduino
    while True:
        if ser_motor.in_waiting > 0:
            line = ser_motor.readline().decode('utf-8')
            if line.find("x") > -1:
                break
            print(line)
            print("LED ready")
        time.sleep(0.01)
    
    ser_motor.write("999999".encode('utf-8'))
    #Output from Arduino
    while True:
        if ser_motor.in_waiting > 0:
            line = ser_motor.readline().decode('utf-8')
            if line.find("x") > -1:
                break
            print(line)
            print("Camera ready")
        time.sleep(0.01)

    answer = input("Return back to Home? \n[y/n]:    ")

    if answer == "y":
        ser_motor.write("80000".encode('utf-8'))
        #Output from Arduino
        while True:
            if ser_motor.in_waiting > 0:
                line = ser_motor.readline().decode('utf-8')
                if line.find("x") > -1:
                    break
                
        time.sleep(0.01)
    
        ser_motor.write("90000".encode('utf-8'))
        #Output from Arduino
        while True:
            if ser_motor.in_waiting > 0:
                line = ser_motor.readline().decode('utf-8')
                if line.find("x") > -1:
                    break
                
        print("continue with next steps :)")
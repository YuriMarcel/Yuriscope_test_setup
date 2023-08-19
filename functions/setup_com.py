import serial
import time

def setup_com():
    global ser_motor, ser_led2, ser_led1345
    start_time = time.time()
    ser_motor = serial.Serial('/dev/ttyUSBM1', 115200, timeout=1.0)
    ser_led2 = serial.Serial('/dev/ttyUSBU1', 115200, timeout=1.0)
    ser_led1345 = serial.Serial('/dev/ttyUSBM2', 115200, timeout=1.0)
    
    ser_motor.reset_input_buffer()
    ser_led2.reset_input_buffer()
    ser_led2.write("0000".encode('utf-8'))
    ser_led1345.reset_input_buffer()
    ser_led1345.write("0000".encode('utf-8'))
    

    print("Serial OK")
    
    time.sleep(3)

    return ser_motor, ser_led2, ser_led1345
    









    
    """
    led_list = [{"ser_led2":ser_led2}, {"ser_led1345":ser_led1345}]
    for ser in led_list:
        for key, value in ser.items():
            led_control = value
            led_control.reset_input_buffer()
            led_control.write("0000".encode('utf-8'))


    
    for using the ESP32 Microcontrollers
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
    time.sleep(1)
    return ser_motor, led_list
    """


import serial
import time

def setup_com():
    start_time = time.time()
    ser_motor = serial.Serial('/dev/ttyUSBM1', 115200, timeout=1.0)
    ser_motor.reset_input_buffer()
    print("Serial OK")
    
    time.sleep(3)

    return ser_motor





    """
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


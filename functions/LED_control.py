def LED_control(ser,LED):
    ser.write(LED.encode('utf-8'))
    while True:
        data_received = ser.readline().decode('utf-8').strip()
        #print(data_received)
        if data_received == "LED on":
            #print("Daten 'LED on' erfolgreich empfangen!")
            break
        elif data_received == "All LEDs off":
            #print("Daten 'All LED off' erfolgreich empfangen!")
            break
    # Restlicher Code
    

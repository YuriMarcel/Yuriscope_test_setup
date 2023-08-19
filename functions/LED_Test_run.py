import serial

def test_leds(ser_led2,ser_led1345):

    working_leds = []
    not_working_leds = []

    try:
        for array_id in range(1, 6):  # Für jedes LED-Array (angenommen, Sie haben 5 Arrays)
            for led_num in range(1, 17):  # Für jede LED im Array (angenommen, jedes Array hat 16 LEDs)
                
                cmd = str(array_id) + "1" + str(led_num).zfill(2)
                print(cmd)
                
                if array_id == 2:
                    ser_led2.write(cmd.encode('utf-8'))
                else:
                    ser_led1345.write(cmd.encode('utf-8'))

                response = input("Is LED on? y/n: ")

                if response == 'y':
                    working_leds.append((array_id, led_num))
                else:
                    not_working_leds.append((array_id, led_num))

                
                if array_id == 2:
                    ser_led2.write("0000".encode('utf-8'))
                else:
                    ser_led1345.write("0000".encode('utf-8'))
                input("Continue?")
    except KeyboardInterrupt:
        print("\nTest interrupted by user.")

    return not_working_leds, working_leds


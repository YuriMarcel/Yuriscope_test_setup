import functions as f
import time
import json

def get_exposure_values(ser_led1345,ser_led2,exposure_path):
    all_leds = [f"{i}{j:03}" for i in range(3, 6) for j in range(101, 117)]
    for LED in all_leds:
        if LED[0] == "2":
            f.LED_control(ser_led2,LED)
        else:
            f.LED_control(ser_led1345,LED)

        # Initialisierungen
        ExposureTime = 200*1e3      #first value is ms, so start = 100ms
        i = 1  # Initialisiere den Iterationszähler
        print(f'Adjusting exposure time for LED:    {LED[0]}.{LED[2:]}')
        raw_data = f.capture_image(LED)
        overexposed_pixels, mean_value = f.analyze_image(raw_data)

        # Überprüfe, ob die LED bei Start-Exposurezeit funktioniert
        if mean_value < 30:
            status = "not functioning"
            # Speichern der Daten in der .txt-Datei
            with open(exposure_path, 'a') as file:
                file.write(f'LED: {LED[0]}.{LED[2:]}: Status: {status}')
                file.write(f'\tFinal exposure time: {ExposureTime/1e3} ms')
                file.write(f'\tOverexpose: {overexposed_pixels}')
                file.write(f'\tMean value: {mean_value}\n')
            continue  # Gehe zur nächsten LED

        while True:
            
            if ExposureTime < 0:
                ExposureTime = 0.05*1e3
                print("under 0")
                break
                    
            f.set_exposure(ExposureTime)
            time.sleep(0.1)  # Setze die Belichtungszeit
            raw_data = f.capture_image(LED)
            overexposed_pixels, mean_value = f.analyze_image(raw_data)

            # Überprüfe die Bedingungen
            if overexposed_pixels <= 2000 and 20 < mean_value < 100:
                break
            else:
                decrement = 10*1e3 
            # Reduce the exposure time based on the number of over-exposed pixels
                if overexposed_pixels > 10000000:
                    decrement = 10*1e3 if ExposureTime >= 2*decrement else decrement/2             
                elif overexposed_pixels > 5000000:
                    decrement = 10*1e3 if ExposureTime >= 2*decrement else decrement/2 
                    if ExposureTime < 2 * decrement:
                        decrement = 5*1e3 if ExposureTime >= 2*decrement else decrement/2 
                elif overexposed_pixels > 20000:
                    decrement = 4*1e3 if ExposureTime >= 2*decrement else decrement/2 
                elif overexposed_pixels > 10000:
                    decrement = 4*1e3 if ExposureTime >= 2*decrement else decrement/2 
                elif overexposed_pixels > 2000:
                    decrement = 2*1e3 if ExposureTime >= 2*decrement else decrement/2 
                elif overexposed_pixels > 1000:
                    decrement = 1*1e3 if ExposureTime >= 2*decrement else decrement/2 
                elif overexposed_pixels < 20:
                    if ExposureTime < 10:
                        decrement = -1*1e3
                    else:
                        decrement = -1*1e3  # Increase the exposure time

                ExposureTime -= decrement  # Adjust the exposure time

                #print('Adjusting exposure time')
                print(f'exposure time: {ExposureTime/1e3} ms')
                print(f'overexpose: {overexposed_pixels}; mean value: {mean_value}')

            i += 1
        #print(f'Iterations: {i}')
        #print(f'Final exposure time: {ExposureTime/1e3} ms')
        #print(f'overexpose: {overexposed_pixels}; mean value: {mean_value}')

        if LED[0] == "2":
            f.LED_control(ser_led2,"0000")
        else:
            f.LED_control(ser_led1345,"0000")

        with open(exposure_path, 'a') as file:
            file.write(f'LED: {LED[0]}.{LED[2:]}')
            file.write(f'\tIterations: {i}')
            file.write(f'\tFinal exposure time: {ExposureTime/1e3} ms')
            file.write(f'\tOverexpose: {overexposed_pixels}')
            file.write(f'\tMean value: {mean_value}\n')  # Eine zusätzliche Leerzeile für die Trennung
 
    return raw_data

def read_exposure_times(filename):
    exposure_times = {}  # Wörterbuch zum Speichern der Belichtungszeiten

    with open(filename, 'r') as file:
        for line in file:
            # Überprüfen Sie, ob die LED funktioniert
            if "Status: not functioning" in line:
                continue  # Überspringen Sie diese Zeile und gehen Sie zur nächsten

            if "LED:" in line and "Final exposure time:" in line:
                # Extrahieren Sie die LED-ID und die Belichtungszeit aus der Zeile
                led = line.split("LED:")[1].split()[0]
                exposure_time = float(line.split("Final exposure time:")[1].split()[0])
                exposure_times[led] = exposure_time

    return exposure_times


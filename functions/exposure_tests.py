import functions as f
import time
import json

def exposure_tests(ser,LED,ExposureTime):
    f.LED_control(ser,LED)
    # Initialisierungen

    f.set_exposure(ExposureTime)  # Setze die Belichtungszeit
    raw_data = f.capture_image(LED)
    overexposed_pixels, mean_value = f.analyze_image(raw_data)

    #print(f'exposure time: {ExposureTime} ms')
    print(f'overexpose: {overexposed_pixels}; mean value: {mean_value}')
    #cmd_exposure  = f.get_exposure
    print(f'Value for exposure time in ms: {f.get_exposure()}')


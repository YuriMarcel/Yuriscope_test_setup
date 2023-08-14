import cv2
import numpy as np
import subprocess as sub
import time

def set_exposure(value):
    sub.run(["v4l2-ctl", "-d", "/dev/video0", "-c", "auto_exposure=1", "-c", f"exposure_time_absolute={value}"])
    

def analyze_image(image):
    overexposed_pixels = np.sum(image > 200)
    mean_value = np.mean(image)
    return overexposed_pixels, mean_value

def get_exposure():
    result = sub.run(["v4l2-ctl", "-d", "/dev/video0", "-C", "exposure_time_absolute"], capture_output=True, text=True)
    if result.returncode == 0:
        # Extrahieren Sie den Wert aus der Ausgabe
        exposure_value = int(result.stdout.split(":")[1].strip())
        return exposure_value
    else:
        print("Fehler beim Abrufen der Belichtungszeit.")
        return None


def auto_adjust_exposure():
    exposure_value = 200  # Startwert
    set_exposure(exposure_value)
    vid = cv2.VideoCapture(0)
    vid.set(cv2.CAP_PROP_FRAME_WIDTH, 4000)
    vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 3000)
    while True:
        
        for _ in range(5):
            ret, frame = vid.read()
        

        if not ret:
            print("Fehler beim Aufnehmen des Bildes.")
            break

        overexposed, mean_val = analyze_image(frame)

        if overexposed < 200 and 30 <= mean_val <= 130:
            print("Optimale Belichtungszeit gefunden!")
            final_frame = frame
            break
        elif overexposed >= 200:
            exposure_value -= 1  # Belichtungszeit verringern
        elif mean_val < 30:
            exposure_value -= 1  # Belichtungszeit verringern
        elif mean_val > 100:
            exposure_value += 1  # Belichtungszeit erhöhen

        set_exposure(exposure_value)
        current_exposure = get_exposure()
        if current_exposure == exposure_value:
            print(f"Exposure time is at {exposure_value}!\nMean value: {mean_val}\noverexposed: {overexposed}")
        else:
            print("error :(")
    # Ausgabe der finalen Belichtungszeit
    print(f"\n\nFinal exposure time = {exposure_value}\nMean value: {mean_val}\noverexposed: {overexposed}")

    # Zeigen Sie das finale Bild an
    if final_frame is not None:
        window_name = "Final Image"
        cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.imshow(window_name, final_frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return vid


    


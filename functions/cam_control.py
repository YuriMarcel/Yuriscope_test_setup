import subprocess as sub
import numpy as np
import time
import serial
import matplotlib.pyplot as plt
from scipy.ndimage import center_of_mass,gaussian_filter
import functions as f
import cv2
import tkinter as tk
from tkinter import ttk
import os
import imageio
from PIL import Image
import matplotlib.pyplot as plt

#select LEDs
leds = [f"{i}1{str(j).zfill(2)}" for i in range(1, 6) for j in range(1, 17)]


root = None
process = None
root = None
exposure_label = None
led_label = None
current_led_index = 0


def capture_image():
    #print("---------------------------------------------------------------------")
    cmd = ["v4l2-ctl", "--device", "/dev/video0", "--stream-mmap", "--stream-to=-", "--stream-count=1"]
    result = sub.run(cmd, capture_output=True)
    if result.returncode != 0:
        print("Fehler beim Aufnehmen des Bildes.")
        print("Fehlermeldung:", result.stderr.decode())  # Gibt die Fehlermeldung aus
        return None

    #print(f"Image captured with LED: {LED[0]}.{LED[2:]}!")
    
    return result.stdout

def save_raw_to_bmp(raw_data, width, height, output_path):
    # Konvertieren Sie die Rohdaten in ein Numpy-Array
    img_array = np.frombuffer(raw_data, dtype=np.uint8).reshape((height, width))

    # Erstellen Sie ein PIL-Image-Objekt aus dem Numpy-Array
    img = Image.fromarray(img_array)

    # Speichern Sie das Bild im BMP-Format
    img.save(output_path, format='BMP')

def save_image(path, LED):
    LED_name = LED.replace(".", "_")
    
    # Bild mit der bereits definierten Funktion aufnehmen
    cmd_setup = ["v4l2-ctl", "--device", "/dev/video0", "--set-fmt-video=width=4000,height=3000,pixelformat=0"]
    sub.run(cmd_setup)

    cmd_capture = ["v4l2-ctl", "--device", "/dev/video0", "--stream-mmap", "--stream-to=-", "--stream-count=1"]
    result = sub.run(cmd_capture, capture_output=True)

    if result.returncode != 0:
        print(f"Fehler beim Aufnehmen des Bildes für LED: {LED_name}.")
        return

    raw_data = result.stdout

    # Konvertieren Sie die .raw-Datei in eine Graustufen-.bmp-Datei
    bmp_file_path = os.path.join(path, f"LED_{LED_name}.bmp")
    save_raw_to_bmp(raw_data, 4000, 3000, bmp_file_path)

    print(f"Bild mit LED: {LED_name} unter {bmp_file_path} gespeichert!")

"""
def save_image(path, LED):
    LED_name = LED.replace(".", "_")
    # Bild mit der bereits definierten Funktion aufnehmen
    cmd_capture = ["v4l2-ctl", "--device", "/dev/video0", "--stream-mmap", "--stream-to=-", "--stream-count=1"]
    result = sub.run(cmd_capture, capture_output=True)

    if result.returncode != 0:
        print(f"Fehler beim Aufnehmen des Bildes für LED: {LED_name}.")
        return

    raw_data = result.stdout

    # Konvertieren Sie das Rohbild direkt aus dem Speicher in eine .bmp Datei mit ImageMagick's convert
    bmp_file_path = os.path.join(path, f"LED_{LED}.bmp")
    cmd_convert = ["convert", "-size", "4000x3000", "-depth", "8", "gray:-", bmp_file_path]
    sub.run(cmd_convert, input=raw_data)

    print(f"Bild mit LED: {LED_name} unter {bmp_file_path} gespeichert!")
"""

def close_gui():
        global process
        root.destroy()
        process.terminate()

def display_live_video():
    global process,root
    # Setzen Sie die gewünschte Auflösung mit v4l2-ctl
    sub.run(["v4l2-ctl", "--device", "/dev/video0", "--set-fmt-video=width=3000,height=4000,pixelformat=1"], 
            stdout=sub.DEVNULL, 
            stderr=sub.DEVNULL)

    # Erstellen Sie ein Hauptfenster
    root = tk.Tk()
    root.title("Adjust Exposure")
    root.geometry('500x200')  # Vergrößern Sie das Fenster

    # Fügen Sie einen Schieberegler hinzu, um die Belichtungszeit zu steuern
    exposure_slider = ttk.Scale(root, from_=0, to_=10*1e3, orient="horizontal", command=update_exposure_and_label)
    exposure_slider.pack(pady=20, padx=20, fill=tk.X)

    # Fügen Sie ein Label hinzu, um den aktuellen Wert der Belichtungszeit anzuzeigen
    global exposure_label
    exposure_label = tk.Label(root, text="Current Exposure Time: 0 ms")
    exposure_label.pack(pady=20)

    # Verwenden Sie ffplay, um das Live-Video anzuzeigen
    process = sub.Popen(["ffplay", "/dev/video0", "-autoexit"], 
                        stdout=sub.DEVNULL, 
                        stderr=sub.DEVNULL)
    
    # Starten Sie die Haupt-GUI-Schleife
    close_button = tk.Button(root, text="Continue with finding Beamcenter", command=close_gui)
    close_button.pack(pady=20)

    root.mainloop()
   
def find_ROI(ser):
    f.LED_control(ser,"3106")
    display_live_video()
    f.LED_control(ser,"0000")

def set_exposure(value):
    #value = value * 1e3
    #sub.run(["v4l2-ctl", "-d", "/dev/video0", "-c", "auto_exposure=1", "-c", f"exposure_time_absolute={value}"])
    sub.run(["v4l2-ctl", "-d", "/dev/video0", "-c", f"exposure_time_us={value}"])

def get_exposure():
    result = sub.run(["v4l2-ctl", "-d", "/dev/video0", "-C", "exposure_time_us"], capture_output=True, text=True)
    if result.returncode == 0:
        # Extrahieren Sie den Wert aus der Ausgabe
        exposure_value = int(result.stdout.split(":")[1].strip())
        
        return exposure_value
    else:
        print("Fehler beim Abrufen der Belichtungszeit.")
        return None

def analyze_image(data):

    if data is  None:
        print("Keine Bilddaten erhalten!")
        return
        

    # Konvertieren Sie die rohen Daten in ein numpy Array mit RGB-Kanälen
    image = np.frombuffer(data, dtype=np.uint8).reshape(3000, 4000)

    # Wenn das Bild RGB-Kanäle hat, konvertiere es in Graustufen
    if len(image.shape) == 3:
        image = np.dot(image[...,:3], [0.2989, 0.5870, 0.1140])

    overexposed_pixels = np.sum(image > 200)
    mean_value = np.mean(image)
    return overexposed_pixels, mean_value

def save_beamcenter(folder,image,centroidX,centroidY):
    print("saving the figure")
    smoothImg = gaussian_filter(image.astype(float), 15)
    Beamcenter = f"beamcenter {round(centroidX)}x{round(centroidY)}"
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    x, y = np.meshgrid(np.arange(image.shape[1]), np.arange(image.shape[0]))
    ax.plot_surface(x, y, smoothImg, cmap='viridis', edgecolor='none')
    ax.set_xlabel('x (pixels)')
    ax.set_ylabel('y (pixels)')
    ax.set_zlabel('Intensity (8-bit scale)')
    ax.set_title(f'3D-Plot of pixel intensity with {Beamcenter}')
    ax.scatter(centroidX, centroidY, image.max(), c='r', s=100, edgecolors='k')
    plt.colorbar(ax.plot_surface(x, y, smoothImg, cmap='viridis', edgecolor='none'))

    # Save the figure
    path = f"{folder}/{Beamcenter}.tiff"
    plt.savefig(path)
    plt.close(fig)

def save_info_to_txt(folder, file_path, mean_val, overexposed, image, centroidY, centroidX):
    with open(file_path, 'a') as file:  # 'a' bedeutet, dass Daten an die Datei angehängt werden, wenn sie bereits existiert
        file.write(f"Mean value:\t\t{round(mean_val,2)}\n")
        file.write(f"Overexposed pixels:\t{overexposed}\n")
        file.write(f"Image Format:\t\t{image.shape[0]}\t{image.shape[1]}\n")
        file.write(f"Beamcenter:\t\t{round(centroidY, 2)}\t{round(centroidX, 2)}\n")
        file.write("--------------------------------------------------\n")  # Eine Trennlinie für bessere Lesbarkeit

def get_beamcenter():
    raw_data = capture_image()
    if raw_data:
        overexposed, mean_val = analyze_image(raw_data)
        image = np.frombuffer(raw_data, dtype=np.uint8).reshape(3000, 4000)
        centroidY, centroidX = center_of_mass(image)
        print(f"Mean value:\t\t{round(mean_val,2)}\nOverexposed pixels:\t{overexposed}")
        print(f"Image Format:\t\t{image.shape[0]}\t{image.shape[1]} ")
        print(f"Beamcenter:\t\t{round(centroidY, 2)}\t{round(centroidX, 2)}\n")
    return image,centroidY,centroidX,overexposed,mean_val

def get_beamcenter_mean(ser_Led1345):
    LEDs_center = ["3106","3107","3110","3111"]
    total_centroidX = 0
    total_centroidY = 0
    total_overexposed = 0
    total_mean_val = 0

    for LED in LEDs_center:
    #for i in range(3101, 3117):
        #LED = str(i)
        f.LED_control(ser_Led1345,LED)
        time.sleep(0.2)
        raw_data = capture_image()
        if raw_data:
            overexposed, mean_val = analyze_image(raw_data)
            image = np.frombuffer(raw_data, dtype=np.uint8).reshape(3000, 4000)
            centroidY, centroidX = center_of_mass(image)
            print(f"Mean value:\t\t{round(mean_val,2)}\nOverexposed pixels:\t{overexposed}")
            print(f"Image Format:\t\t{image.shape[0]}\t{image.shape[1]} ")
            print(f"Beamcenter:\t\t{round(centroidY, 2)}\t{round(centroidX, 2)}\n")
            
            total_centroidX += centroidX
            total_centroidY += centroidY
            total_overexposed += overexposed
            total_mean_val += mean_val
        f.LED_control(ser_Led1345,"0000")
        time.sleep(0.1)

    # Berechnen Sie den Mittelwert für alle LEDs
    avg_centroidX = total_centroidX / len(LEDs_center)
    avg_centroidY = total_centroidY / len(LEDs_center)
    avg_overexposed = total_overexposed / len(LEDs_center)
    avg_mean_val = total_mean_val / len(LEDs_center)

    print(f"\nAverage Beamcenter for all LEDs:\t{round(avg_centroidY, 2)}\t{round(avg_centroidX, 2)}")
    print(f"Average Mean value:\t\t{round(avg_mean_val,2)}")
    print(f"Average Overexposed pixels:\t{avg_overexposed}\n")

    return image, avg_centroidY, avg_centroidX, avg_overexposed, avg_mean_val

def find_beamcenter(folder,file_path,Beamcenter_set,ser_Led1345):

    if Beamcenter_set == "Start finding procedure":
        while True:
            try:
                image,centroidY,centroidX,overexposed,mean_val = get_beamcenter_mean(ser_Led1345)
                input("To get Beamcenter again press Enter")
            except KeyboardInterrupt:
                print("\n")
                save_beamcenter(folder,image,centroidX,centroidY)
                save_info_to_txt(folder, file_path, mean_val, overexposed, image, centroidY, centroidX)
                break
    elif Beamcenter_set == "Start finding procedure(no figure)":
        while True:
            try:
                image,centroidY,centroidX,overexposed,mean_val = get_beamcenter_mean(ser_Led1345)
                time.sleep(1)
            except KeyboardInterrupt:
                print("\n")
                save_info_to_txt(folder, file_path, mean_val, overexposed, image, centroidY, centroidX)
                break
    elif Beamcenter_set == "Just show the beamcenter":
        image,centroidY,centroidX,overexposed,mean_val  = get_beamcenter_mean(ser_Led1345)
        save_beamcenter(folder,image,centroidX,centroidY)
        save_info_to_txt(folder, file_path, mean_val, overexposed, image, centroidY, centroidX)
    elif Beamcenter_set == "Just show the beamcenter(no figure)":
        image,centroidY,centroidX,overexposed,mean_val  = get_beamcenter_mean(ser_Led1345)
        save_info_to_txt(folder, file_path, mean_val, overexposed, image, centroidY, centroidX)

def switch_to_next_led(ser2,ser1345,exposure_path):
    global current_led_index
    print("switching")
    raw_data = f.capture_image()
    overexposed_pixels, mean_value = f.analyze_image(raw_data)
    ExposureTime = get_exposure()
    with open(exposure_path, 'a') as file:
        file.write(f'LED: {leds[current_led_index][0]}.{leds[current_led_index][2:]}')        
        file.write(f'\tFinal exposure time: {ExposureTime/1e3} ms')
        file.write(f'\tOverexpose: {overexposed_pixels}')
        file.write(f'\tMean value: {round(mean_value, 2)}\n')  # Eine zusätzliche Leerzeile für die Trennung

    # Schalten Sie die aktuelle LED aus
    if leds[current_led_index][0] == "2":
        f.LED_control(ser2, "0000")
    else:
        f.LED_control(ser1345, "0000")
    print("off")
    # Zum nächsten LED wechseln
    current_led_index += 1
    if current_led_index >= len(leds):
        root.destroy()  # Schließt das Tkinter-Fenster
        print("Finished exposure time setting")
        return    
    print(f"Switching to LED: {leds[current_led_index]}")

    # Schalten Sie die nächste LED ein
    if leds[current_led_index][0] == "2":
        f.LED_control(ser2, leds[current_led_index])
    else:
        f.LED_control(ser1345, leds[current_led_index])
    
    # Aktualisieren Sie das LED-Label
    led_label.config(text=f"Current LED: {leds[current_led_index]}")

def update_exposure_and_label(value):
    set_exposure(value)
    exposure_label.config(text=f"Current Exposure Time: {round(float(value)/1e3, 2)} ms")

def update_values():
    raw_data = f.capture_image()
    overexposed_pixels, mean_value = f.analyze_image(raw_data)

    overexposed_label.config(text=f"Overexposed Pixels: {overexposed_pixels}")
    mean_value_label.config(text=f"Mean Value: {round(mean_value,2)}")

    # Rufen Sie die Funktion nach 0,5 Sekunden erneut auf
    root.after(200, update_values)

def set_exposure_from_entry():
    try:
        value = float(exposure_entry.get())
        value = value *1e3
        update_exposure_and_label(value)
    except ValueError:
        print("Bitte geben Sie eine gültige Zahl ein.")

def mark_led_as_not_working(ser2,ser1345,exposure_path):

    raw_data = f.capture_image()
    overexposed_pixels, mean_value = f.analyze_image(raw_data)
    ExposureTime = get_exposure()
    print("not working")
    with open(exposure_path, 'a') as file:
        file.write(f'LED: {leds[current_led_index][0]}.{leds[current_led_index][2:]}')
        file.write('\tNot functioning')  # Hinweis, dass die LED nicht funktioniert
        file.write(f'\tFinal exposure time: {ExposureTime/1e3} ms')
        file.write(f'\tOverexpose: {overexposed_pixels}')
        file.write(f'\tMean value: {round(mean_value, 2)}\n')  # Eine zusätzliche Leerzeile für die Trennung
    switch_to_next_led(ser2,ser1345,exposure_path)  # Wechseln Sie zur nächsten LED

def find_exposure_manually(ser2,ser1345,exposure_path):
    global root, led_label, overexposed_label, mean_value_label, exposure_entry

    # Erstellen Sie ein Hauptfenster
    root = tk.Tk()
    root.title("Adjust Exposure")
    root.geometry('500x600')  # Vergrößern Sie das Fenster

    # Fügen Sie einen Schieberegler hinzu, um die Belichtungszeit zu steuern
    exposure_slider = ttk.Scale(root, from_=0, to_=100*1e3, orient="horizontal", command=update_exposure_and_label)
    exposure_slider.pack(pady=20, padx=20, fill=tk.X)

    # Fügen Sie ein Label hinzu, um den aktuellen Wert der Belichtungszeit anzuzeigen
    global exposure_label
    exposure_label = tk.Label(root, text="Current Exposure Time: 0 ms")
    exposure_label.pack(pady=10)

    # Fügen Sie ein Label hinzu, um den aktuellen LED-Status anzuzeigen
    led_label = tk.Label(root, text=f"Current LED: {leds[current_led_index]}")
    led_label.pack(pady=10)

    overexposed_label = tk.Label(root, text="Overexposed Pixels: Loading...")
    overexposed_label.pack(pady=10)

    mean_value_label = tk.Label(root, text="Mean Value: Loading...")
    mean_value_label.pack(pady=10)

    # Fügen Sie einen Button hinzu, um zur nächsten LED zu wechseln
    next_led_button = tk.Button(root, text="Go to next LED", command=lambda: switch_to_next_led(ser2,ser1345,exposure_path))
    next_led_button.pack(pady=20)

    exposure_entry = tk.Entry(root)
    exposure_entry.pack(pady=10, padx=20, fill=tk.X)

    # Fügen Sie einen Button hinzu, um die Belichtungszeit zu aktualisieren
    update_button = tk.Button(root, text="update exposure time", command=set_exposure_from_entry)
    update_button.pack(pady=10)

    
    # Setzen Sie die gewünschte Auflösung mit v4l2-ctl
    sub.run(["v4l2-ctl", "--device", "/dev/video0", "--set-fmt-video=width=3000,height=4000,pixelformat=0"], 
            stdout=sub.DEVNULL, 
            stderr=sub.DEVNULL)

    not_working_button = tk.Button(root, text="LED not working", command=lambda: mark_led_as_not_working(ser2,ser1345,exposure_path))
    not_working_button.pack(pady=20)

    update_values()

    

    #close_button = tk.Button(root, text="Continue with finding Beamcenter", command=close_gui)
    #close_button.pack(pady=20)

    root.mainloop()

def raw_to_cv2_image(raw_data, width, height):
    img_array = np.frombuffer(raw_data, dtype=np.uint8).reshape((height, width))
    return img_array

def capture_raw_image():
    cmd_setup = ["v4l2-ctl", "--device", "/dev/video0", "--set-fmt-video=width=4000,height=3000,pixelformat=0"]
    sub.run(cmd_setup)
    cmd_capture = ["v4l2-ctl", "--device", "/dev/video0", "--stream-mmap", "--stream-to=-", "--stream-count=1"]
    result = sub.run(cmd_capture, capture_output=True)
    if result.returncode != 0:
        print("Fehler beim Aufnehmen des Bildes.")
        return None
    return result.stdout

def compute_shift_from_raw(raw_image1, raw_image2):
    img1 = raw_to_cv2_image(raw_image1, 4000, 3000)
    img2 = raw_to_cv2_image(raw_image2, 4000, 3000)

    # Display the images in pop-up windows
    cv2.imshow('Image 1', img1)
    cv2.imshow('Image 2', img2)
    cv2.waitKey(0)  # Wait until a key is pressed
    cv2.destroyAllWindows()  # Close the windows
    
    warp_mode = cv2.MOTION_TRANSLATION
    warp_matrix = np.eye(2, 3, dtype=np.float32)
    number_of_iterations = 5000
    termination_eps = 1e-10
    criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, number_of_iterations, termination_eps)
    
    _, warp_matrix = cv2.findTransformECC(img2, img1, warp_matrix, warp_mode, criteria)
    dx = warp_matrix[0,2]
    dy = warp_matrix[1,2]
    return dx, dy

def get_pixelshift_LED(ser1345):
    print("Start getting pixelshift")
    f.LED_control(ser1345,"3101")
    time.sleep(1)
    raw_img1 = capture_raw_image()
    f.LED_control(ser1345,"0000")
    f.LED_control(ser1345,"3102")
    time.sleep(1)
    raw_img2 = capture_raw_image()


    # Estimate pixel shift
    x_shift, y_shift = compute_shift_from_raw(raw_img1, raw_img2)
    print(f"X Shift: {x_shift}, Y Shift: {y_shift}")



def check_exposure_values(ser2, ser1345, exposure_times):
    exposure_times_transformed = {key.replace(".", "1"): value for key, value in exposure_times.items()}
    global current_led_index, leds, exposure_label, overexposed_label, mean_value_label,led_label

    # Erstellen Sie ein Hauptfenster
    root = tk.Tk()
    root.title("Check Exposure Values")
    root.geometry('500x400')

    # Fügen Sie ein Label hinzu, um den aktuellen LED-Status anzuzeigen
    led_label = tk.Label(root, text=f"Current LED: {leds[current_led_index]}")
    led_label.pack(pady=10)

    overexposed_label = tk.Label(root, text="Overexposed Pixels: Loading...")
    overexposed_label.pack(pady=10)

    mean_value_label = tk.Label(root, text="Mean Value: Loading...")
    mean_value_label.pack(pady=10)

    # Fügen Sie einen Button hinzu, um zur nächsten LED zu wechseln
    next_led_button = tk.Button(root, text="Go to next LED", command=lambda: switch_to_next_led(ser2, ser1345, exposure_times_transformed))
    next_led_button.pack(pady=20)

    exposure_label = tk.Label(root, text="Current Exposure Time: Loading...")
    exposure_label.pack(pady=10)

    # Fügen Sie einen Button hinzu, um das Bild anzuzeigen
    show_image_button = tk.Button(root, text="Show Picture", command=show_image)
    show_image_button.pack(pady=20)

    root.mainloop()

def show_image():
    global current_led_index, leds

    # Nehmen Sie ein Bild auf
    image_data = capture_raw_image()

    image = np.frombuffer(image_data, dtype=np.uint8).reshape(3000, 4000)
    plt.imshow(image, cmap='gray')  # cmap='gray' ist optional, je nachdem, wie Ihr Bild aussieht
    plt.title(f"Image for LED {leds[current_led_index]}")
    plt.show()


def update_values_and_show_image(ser2, ser1345, exposure_times):
    global current_led_index, leds, exposure_label, overexposed_label, mean_value_label

    # Holen Sie sich den aktuellen LED-Namen
    led_list = leds[current_led_index]
    # Überprüfen Sie, ob led_list im exposure_times-Wörterbuch vorhanden ist
    if led_list not in exposure_times:
        print(f"Fehler: {led_list} nicht in exposure_times gefunden!")
        return

    # Setzen Sie die Belichtungszeit für die aktuelle LED
    exposure_time = exposure_times[led_list]
    f.set_exposure(int(exposure_time * 1000))

    # Nehmen Sie ein Bild auf
    image_data = capture_raw_image()

    # Analysieren Sie das Bild
    overexposed_pixels, mean_value = analyze_image(image_data)

    # Zeigen Sie das Bild mit cv2 an
    #image = np.frombuffer(image_data, dtype=np.uint8).reshape(3000, 4000)
    #plt.imshow(image, cmap='gray')  # cmap='gray' ist optional, je nachdem, wie Ihr Bild aussieht
    #plt.title(f"Image for LED {led_list}")
    #plt.show()

    # Aktualisieren Sie die GUI-Labels mit den neuen Werten
    exposure_label.config(text=f"Current Exposure Time: {exposure_time} ms")
    led_label.config(text=f"Current LED: {led_list}")
    overexposed_label.config(text=f"Overexposed Pixels: {overexposed_pixels}")
    mean_value_label.config(text=f"Mean Value: {mean_value}")
    
"""
def switch_to_next_led(ser_led2, ser_led1345, exposure_times):
    
    global current_led_index

    if leds[current_led_index][0] == "2":
            f.LED_control(ser_led2,"0000")
    else:
            f.LED_control(ser_led1345,"0000")

    if leds[current_led_index][0] == "2":
            f.LED_control(ser_led2,leds[current_led_index])
    else:
            f.LED_control(ser_led1345,leds[current_led_index])


    current_led_index += 1
    if current_led_index >= len(leds):
        current_led_index = 0
    update_values_and_show_image(ser_led2, ser_led1345, exposure_times)
"""
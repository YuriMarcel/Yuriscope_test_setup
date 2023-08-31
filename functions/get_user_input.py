import tkinter as tk
from tkinter import simpledialog, messagebox,ttk

def get_user_input():
    # Erstellen Sie das Hauptfenster

    root = tk.Tk()
    root.title("Input Dialog")

    # Erstellen Sie Labels und Entry-Felder für jede Eingabe
    labels = ["Find ROI","Beamcenter setting","Exposure time Values for each LED", "Choose a LED pattern", "Camera end position (in mm)", 
              "Camera steps in between (in mm)", "LED Array end position (in mm)","LED Array steps in between (in mm)"]
    default_values = ["","", "", "","20", "20", "0.5","0.5"]
    
    entries = []
    for i, label in enumerate(labels):
        lbl = tk.Label(root, text=label)
        lbl.grid(row=i, column=0, padx=10, pady=5)

        if label == "Choose a LED pattern":
            options = ["80 LEDs individualy", "Quarter of each array", "whole Array"]
            dropdown = ttk.Combobox(root, values=options)
            dropdown.grid(row=i, column=1, padx=10, pady=5)
            dropdown.set(options[0])  # Setzen Sie die Standardoption
            entries.append(dropdown)
        elif label == "Exposure time Values for each LED":
            options = ["Load from given path", "Get new values","Check values"]
            dropdown = ttk.Combobox(root, values=options)
            dropdown.grid(row=i, column=1, padx=10, pady=5)
            dropdown.set(options[0])  # Setzen Sie die Standardoption
            entries.append(dropdown)
        elif label == "Beamcenter setting":
            options = ["Start finding procedure", "Just show the beamcenter","Start finding procedure(no figure)","Just show the beamcenter(no figure)","skip"]
            dropdown = ttk.Combobox(root, values=options)
            dropdown.grid(row=i, column=1, padx=10, pady=5)
            dropdown.set(options[0])  # Setzen Sie die Standardoption
            entries.append(dropdown)
        elif label == "Find ROI":
            options = ["yes", "no"]
            dropdown = ttk.Combobox(root, values=options)
            dropdown.grid(row=i, column=1, padx=10, pady=5)
            dropdown.set(options[0])  # Setzen Sie die Standardoption
            entries.append(dropdown)
        else:
            entry = tk.Entry(root)
            entry.insert(0, default_values[i])
            entry.grid(row=i, column=1, padx=10, pady=5)
            entries.append(entry)


    # Funktion zum Sammeln von Daten und Schließen des Fensters
    def collect_data():
        global answers
        answers = [entry.get() for entry in entries]
        root.quit()

    # Hinzufügen einer Schaltfläche zum Abschließen der Eingabe
    submit_button = tk.Button(root, text="Submit", command=collect_data)
    submit_button.grid(row=len(labels), column=0, columnspan=2, pady=10)

    root.update_idletasks()

    # Bildschirmbreite und -höhe abrufen
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Größe des Fensters abrufen
    window_width = root.winfo_width()
    window_height = root.winfo_height()

    # Position für das Fenster berechnen
    x = (screen_width / 2) - (window_width / 2)
    y = (screen_height / 2) - (window_height / 2)

    # Fensterposition setzen
    root.geometry(f"{window_width}x{window_height}+{int(x)}+{int(y)}")

    root.mainloop()
    root.destroy()

    return answers



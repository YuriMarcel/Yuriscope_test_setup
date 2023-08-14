import subprocess as sub

def get_exposure():
    result = sub.run(["v4l2-ctl", "-d", "/dev/video0", "-C", "exposure_time_absolute"], capture_output=True, text=True)
    if result.returncode == 0:
        # Extrahieren Sie den Wert aus der Ausgabe
        exposure_value = int(result.stdout.split(":")[1].strip())
        return exposure_value
    else:
        print("Fehler beim Abrufen der Belichtungszeit.")
        return None

value = 12345678
sub.run(["v4l2-ctl", "-d", "/dev/video0", "-c", "auto_exposure=1", "-c", f"exposure_time_absolute={value}"])

# Überprüfen Sie den aktuellen Wert
current_exposure = get_exposure()
if current_exposure == value:
    print(f"Belichtungszeit erfolgreich auf {value} gesetzt!")
else:
    print(f"Fehler: Belichtungszeit ist {current_exposure}, erwartet wurde {value}.")


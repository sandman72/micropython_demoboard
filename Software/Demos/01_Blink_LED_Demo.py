# Bibliotheken laden
#from machine import Pin
import time

# Blaue LED and GPIO22 als Ausgang initialisieren
#led = Pin(22, Pin.OUT)
    
# Endlosschleife LED blinken lassen
while True:
    # LED einschalten
    led.on()
    # Warte eine halbe Sekunde
    time.sleep(0.5)

    # LED ausschalten
    led.off()
    # Warte eine halbe Sekunde
    time.sleep(0.5)
    
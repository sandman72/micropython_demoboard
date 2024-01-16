# Bibliotheken laden
import machine
import utime

# Analog/Digital Wandler ADC0 GPIO 26 initialisieren
# an ADC 0 hängt das einstellbare Potentiometer RV1
potentiometer = machine.ADC(26)

# Endlosschleife Poti auslesen und Wert anzeigen
while True:
    print("Poti: " + str(potentiometer.read_u16()))
    utime.sleep(1)

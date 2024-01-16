# Bibliotheken laden
import machine
import utime

# Analog/Digital Wandler ADC1 GPIO 27 initialisieren
# an ADC 1 hängt der lichtempfindliche Widerstand R1 
ldr = machine.ADC(27)

# Endlosschleife Poti auslesen und Wert anzeigen
while True:
    print("LDR: " + str(ldr.read_u16()))
    utime.sleep(1)

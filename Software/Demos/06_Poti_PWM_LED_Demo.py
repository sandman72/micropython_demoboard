# Bibliotheken laden
from machine import Pin, PWM
from time import sleep

# Blaue LED an GPIO22 mit PWM initialisieren
pwm = PWM(Pin(22))

# Frequenz (Hz) einstellen
pwm.freq(4000)

# Analog/Digital Wandler ADC0 GPIO 26 initialisieren
# an ADC 0 hängt das einstellbare Potentiometer RV1
potentiometer = machine.ADC(26)

# Endlosschleife ADC0 auslesen und damit LED PWM Helligkeit einstellen
while True:
    pwm.duty_u16(potentiometer.read_u16())
    sleep(0.005)

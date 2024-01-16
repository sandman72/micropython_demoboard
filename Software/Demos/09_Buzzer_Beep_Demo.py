# Bibliotheken laden
from machine import Pin, PWM
from utime import sleep

# Buzzer an GPIO 10 mit PWM initialisieren
buzzer = PWM(Pin(10))

# Frequenz (Hz) einstellen
frequency = 1000
buzzer.freq(frequency)

# Einschalten für 0.3 Sekunden
buzzer.duty_u16(1000)
sleep(0.3)

# Ausschalten
buzzer.duty_u16(0)

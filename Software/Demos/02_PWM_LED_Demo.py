# Bibliotheken laden
from machine import Pin, PWM
from time import sleep

# Blaue LED an GPIO22 mit PWM initialisieren
pwm = PWM(Pin(22))

# Frequenz (Hz) einstellen
pwm.freq(4000)

# Endlosschleife LED Helligkeit hoch/runterfahren
while True:
  # Helligkeit hoch fahren
  for duty_cycle in range(0, 65536, 129):
    pwm.duty_u16(duty_cycle)
    sleep(0.005)
    
  # Helligkeit runter fahren
  for duty_cycle in range(65536, 0, -129):
    pwm.duty_u16(duty_cycle)
    sleep(0.005)

# Bibliotheken laden
from machine import Pin
import time

# GPIO Pins als Eingänge mit Pull_Down initalisieren
button_up     = Pin(11, Pin.IN, Pin.PULL_DOWN)
button_left   = Pin(12, Pin.IN, Pin.PULL_DOWN)
button_right  = Pin(13, Pin.IN, Pin.PULL_DOWN)
button_down   = Pin(14, Pin.IN, Pin.PULL_DOWN)
button_center = Pin(15, Pin.IN, Pin.PULL_DOWN)

# Endlosschleife mit Abfrage der Buttons
while True:
    if button_up.value() == 1:
        print("Up Button is Pressed")
    if button_left.value() == 1:
        print("Left Button is Pressed")
    if button_right.value() == 1:
        print("Right Button is Pressed")
    if button_down.value() == 1:
        print("Down Button is Pressed")
    if button_center.value() == 1:
        print("Center Button is Pressed")
    time.sleep(0.1)

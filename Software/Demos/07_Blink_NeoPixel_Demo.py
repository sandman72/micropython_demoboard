# Bibliotheken laden
from machine import Pin
from neopixel import NeoPixel
from time import sleep_ms

# NeoPixel/WS2812 LED Streifen mit GPIO 28 initialisieren 
neopin = Pin(28, Pin.OUT)

# Anzahl der LEDs
leds = 5

# Helligkeit: 0 bis 255
brightness = 30

# Geschwindigkeit (Millisekunden)
speed = 50

# Initialisierung WS2812/NeoPixel
pixels = NeoPixel(neopin, leds)

# Endlosschleife LEDs abwechselnd einschalten
while True:
    for i in range (leds):
        # Nächste LED einschalten  (R,G,B)
        pixels[i] = (brightness, brightness, brightness)
        pixels.write()
        # kurz warten
        sleep_ms(speed)
        # LED wieder zurücksetzen
        pixels[i] = (0, 0, 0)
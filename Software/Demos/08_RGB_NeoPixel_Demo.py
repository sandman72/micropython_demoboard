# Bibliotheken laden
from machine import Pin
from neopixel import NeoPixel
from time import sleep_ms

# NeoPixel/WS2812 LED Streifen mit GPIO 28 initialisieren 
neopin = Pin(28, Pin.OUT)

# Anzahl der LEDs
leds = 5

# Geschwindigkeit (Millisekunden)
speed = 50

# Initialisierung WS2812/NeoPixel
pixels = NeoPixel(neopin, leds)

# Farbwandlungsfunkionen
def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colors are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3)

def rainbow_cycle():
    global leds, pixels
    for j in range(255):
        for i in range(leds):
            rc_index = (i * 256 // leds) + j
            (r,g,b) = wheel(rc_index & 255)
            # Helligkeit in RGB Werten anpassen
            pixels[i] = (int(r/4),int(g/4),int(b/4)) 
        pixels.write()

# Farbrad Position
counter = 0

# Endlosschleife Rainbow auf NeoPixeln anzeigen
while True:
    rainbow_cycle()
    counter += 1
    # kurze Pause
    sleep_ms(50)
# Bibliotheken laden
from machine import Pin, SPI
from utime import sleep
from bmp280_spi import BMP280SPI

# BMP280 Sensor an SPI Bus initialisieren
# GPIO 16 - Pico RX <- BMP TX
# GPIO 17 - Chip Select
# GPIO 18 - Clock
# GPIO 19 - Pico TX -> BMP RX
spi = SPI(0, sck=Pin(18), mosi=Pin(19), miso=Pin(16), polarity=1, phase=1)
spi_cs = Pin(17, Pin.OUT, value=1)
bmp280_spi = BMP280SPI(spi, spi_cs)

# Die BMP280 Chip ID Auslesen. Sollte 0x58 sein
print(bmp280_spi.chip_id)

# Sensor auslesen und die gemessenen Werte anzeigen
while True:
    readout = bmp280_spi.measurements
    print(f"Temperature: {readout['t']} °C, pressure: {readout['p']} hPa.")
    sleep(1)

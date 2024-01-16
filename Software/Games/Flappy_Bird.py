#
# *****     Flappy Bird     *****
#
# gespielt wird mit dem Center Button
#
# Adaptiert von Frank Hellmann 2023
# für das Attraktor MicroPython Demo Board
#
# Original Code:
# github.com/zelacerda/micropython

# Bibliotheken importieren
import ssd1306
import random
import os
from framebuf import FrameBuffer as FB
from machine import I2C, PWM, Pin
from utime import sleep

# OLED Auflösung
WIDTH   = 128
HEIGHT  = 64

# Initialiere Pins
i2c = I2C(0, sda=Pin(20), scl=Pin(21))
oled = ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c)
button = Pin(15, Pin.IN, Pin.PULL_DOWN)
buzzer = PWM(Pin(10))

# Wandle String in bytearray
def to_bytearray(s):
    return bytearray([int('0x'+s[i:i+2]) for i in range(0,len(s),2)])

# High Score speichern
def write_high_score(n):
    f = open('fb_hiscore', 'w')
    f.write(str(n))
    f.close()
    return 0

def read_high_score():
    if 'fb_hiscore' in os.listdir():
        f = open('fb_hiscore', 'r')
        high_score = f.read()
        f.close()
        return int(high_score)
    else:
        write_high_score(0)

# Bitmap images
BIRD = '07e018f021f871ecf9ecfcfcbe7e4c81717e4082307c0f80'
COL1 = '201c'*26+'ffff'+'800f'*4+'ffff'
COL2 = 'ffff'+'800f'*4+'ffff'+'201c'*26
bird_size = (16,12)
colu_size  = (16,32)

# Generate sprites
bird = FB(to_bytearray(BIRD),bird_size[0],bird_size[1],3)
col1 = FB(to_bytearray(COL1),colu_size[0],colu_size[1],3)
col2 = FB(to_bytearray(COL2),colu_size[0],colu_size[1],3)

class FlappyBird:
    def __init__(self):
        self.height = bird_size[1]
        self.y = HEIGHT // 2 - self.height // 2
        self.vel = -wing_power

    def move(self):
        self.vel += gravity
        self.y = int(self.y + self.vel)

    def flap(self):
        self.vel = -wing_power

    def crashed(self):
        y_limit = HEIGHT - self.height
        return self.y > y_limit

class Obstacle:
    def __init__(self, x):
        self.gap = random.randint(6+gap_size, HEIGHT-6-gap_size)
        self.x = x
        self.score = 0

    def scroll(self):
        self.x -= velocity
        if self.x < -colu_size[0]:
            self.score += 1
            self.x = WIDTH
            self.gap = random.randint(6+gap_size, HEIGHT-6-gap_size)

    def collided(self, y):
        if self.x < bird_size[0] and \
           self.x > -colu_size[0] and \
           (self.gap - y > gap_size or y + bird_size[1] - self.gap > gap_size):
            return True
        else:
            return False

def clicked():
    global pressed
    if button.value() == 1 and not pressed:
        pressed = True
        return True
    elif button.value() == 0 and pressed:
        pressed = False
    return False

def draw():
    oled.fill(0)
    oled.blit(bird, 0, flappy_bird.y)
    oled.blit(col1,obstacle_1.x,obstacle_1.gap-gap_size-colu_size[1])
    oled.blit(col2,obstacle_1.x,obstacle_1.gap+gap_size)
    oled.blit(col1,obstacle_2.x,obstacle_2.gap-gap_size-colu_size[1])
    oled.blit(col2,obstacle_2.x,obstacle_2.gap+gap_size)
    oled.fill_rect(WIDTH//2 - 13, 0, 26, 9, 0)
    oled.text('%03d' % (obstacle_1.score + obstacle_2.score), WIDTH//2 - 12, 0)
    oled.show()

# Game parameters
high_score  = read_high_score()
gap_size    = 20
velocity    = 2
gravity     = .5
wing_power  = 3
state       = 0
pressed     = False

# Game state functions
def splash_screen():
    global state
    oled.fill(0)
    oled.blit(col2, (WIDTH-colu_size[0])//2, HEIGHT-12)
    oled.blit(bird, (WIDTH-bird_size[0])//2, HEIGHT-12-bird_size[1])
    oled.rect(0, 0, WIDTH, HEIGHT, 1)
    oled.text('F L A P P Y', WIDTH//2-44, 3)
    oled.text('B I R D', WIDTH//2-28, 13)
    oled.text('Record: ' + '%03d' % high_score, WIDTH//2-44, HEIGHT//2-6)
    oled.show()
    state = 1

def game_waiting():
    global state,score,flappy_bird,obstacle_1,obstacle_2, pressed
    if clicked():
        flappy_bird = FlappyBird()
        obstacle_1 = Obstacle(WIDTH)
        obstacle_2 = Obstacle(WIDTH + (WIDTH + colu_size[0]) // 2)
        state = 2

def game_running():
    global state
    if clicked(): flappy_bird.flap()
    flappy_bird.move()
    if flappy_bird.crashed():
        flappy_bird.y = HEIGHT - flappy_bird.height
        state = 3
    obstacle_1.scroll()
    obstacle_2.scroll()
    if obstacle_1.collided(flappy_bird.y) or obstacle_2.collided(flappy_bird.y):
        state = 3
    draw()

def game_over():
    global state, high_score
    oled.fill_rect(WIDTH//2-32, 10, 64, 23, 0)
    oled.rect(WIDTH//2-32, 10, 64, 23, 1)
    oled.text('G A M E', WIDTH//2-28, 13)
    oled.text('O V E R', WIDTH//2-28, 23)
    score = obstacle_1.score + obstacle_2.score
    if score > high_score:
        high_score = score
        oled.fill_rect(WIDTH//2-48, 37, 96, 14, 0)
        oled.rect(WIDTH//2-48, 37, 96, 14, 1)
        oled.text('New record!',WIDTH//2-44, 40)
        write_high_score(high_score)
    oled.show()
    buzzer.freq(200)
    buzzer.duty_u16(2000)
    sleep(0.3)
    buzzer.duty_u16(0)
    state = 0
    sleep(1.5)

def loop():
    while True:
        if   state == 0: splash_screen()
        elif state == 1: game_waiting()
        elif state == 2: game_running()
        elif state == 3: game_over()

loop()
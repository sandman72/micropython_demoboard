# PicoPong.py: a simple Pong game by Vincent Mistler (YouMakeTech)
#
# Adapted to the Attraktor MicroPython Demo Board
# by Frank Hellmann 11.2023
#
# Original Code:
# https://github.com/YouMakeTech/PicoRetroGamingSystem
#

# Importiere Bibliotheken
from machine import Pin, PWM, I2C,
import ssd1306
import time
import random

def pico_pong_main():
        
    # Game parameters
    SCREEN_WIDTH = 128                       # size of the screen
    SCREEN_HEIGHT = 64
    BALL_SIZE = int(SCREEN_WIDTH/32)         # size of the ball size in pixels
    PADDLE_WIDTH = int(SCREEN_WIDTH/8)       # size of the paddle in pixels
    PADDLE_HEIGHT = int(SCREEN_HEIGHT/16)
    PADDLE_Y = SCREEN_HEIGHT-2*PADDLE_HEIGHT # Vertical position of the paddle

    # Initialiere Pins
    buzzer = PWM(Pin(10))
    i2c = I2C(0, sda=Pin(20), scl=Pin(21))
    oled = ssd1306.SSD1306_I2C(SCREEN_WIDTH, SCREEN_HEIGHT, i2c)
    oled.fill(0)

    # Buttons
    up = Pin(11, Pin.IN, Pin.PULL_DOWN)
    down = Pin(14, Pin.IN, Pin.PULL_DOWN)
    left = Pin(12, Pin.IN, Pin.PULL_DOWN)
    right = Pin(13, Pin.IN, Pin.PULL_DOWN)
    button1 = Pin(15, Pin.IN, Pin.PULL_DOWN)

    # variables
    ballX = 64     # ball position in pixels
    ballY = 0
    ballVX = 1.0    # ball velocity along x in pixels per frame
    ballVY = 1.0    # ball velocity along y in pixels per frame

    paddleX = int(SCREEN_WIDTH/2) # paddle  position in pixels
    paddleVX = 6                  # paddle velocity in pixels per frame

    soundFreq = 400 # Sound frequency in Hz when the ball hits something
    score = 0

    while True:
        # move the paddle when a button is pressed
        if right.value() == 1:
            # right button pressed
            paddleX += paddleVX
            if paddleX + PADDLE_WIDTH > SCREEN_WIDTH:
                paddleX = SCREEN_WIDTH - PADDLE_WIDTH
        elif left.value() == 1:
            # left button pressed
            paddleX -= paddleVX
            if paddleX < 0:
                paddleX = 0
        
        # move the ball
        if abs(ballVX) < 1:
            # do not allow an infinite vertical trajectory for the ball
            ballVX = 1

        ballX = int(ballX + ballVX)
        ballY = int(ballY + ballVY)
        
        # collision detection
        collision=False
        if ballX < 0:
            # collision with the left edge of the screen 
            ballX = 0
            ballVX = -ballVX
            collision = True
        
        if ballX + BALL_SIZE > SCREEN_WIDTH:
            # collision with the right edge of the screen
            ballX = SCREEN_WIDTH-BALL_SIZE
            ballVX = -ballVX
            collision = True

        if ballY+BALL_SIZE>PADDLE_Y and ballX > paddleX-BALL_SIZE and ballX<paddleX+PADDLE_WIDTH+BALL_SIZE:
            # collision with the paddle
            # => change ball direction
            ballVY = -ballVY
            ballY = PADDLE_Y-BALL_SIZE
            # increase speed!
            ballVY -= 0.2
            ballVX += (ballX - (paddleX + PADDLE_WIDTH/2))/10
            collision = True
            score += 10
            
        if ballY < 0:
            # collision with the top of the screen
            ballY = 0
            ballVY = -ballVY
            collision = True
            
        if ballY + BALL_SIZE > SCREEN_HEIGHT:
            # collision with the bottom of the screen
            # => Display Game Over
            oled.fill(0)
            oled.text("GAME OVER", int(SCREEN_WIDTH/2)-int(len("Game Over!")/2 * 8), int(SCREEN_HEIGHT/2) - 8)
            oled.text(str(score), SCREEN_WIDTH-int(len(str(score))*8), 0)
            oled.show()
            # play an ugly sound
            buzzer.freq(200)
            buzzer.duty_u16(2000)
            time.sleep(0.5)
            buzzer.duty_u16(0)
            # wait for a button
            while button1.value()==0:
                time.sleep(0.01)
            # exit the loop
            break
            
        # Make a sound if the ball hits something
        # Alternate between 2 sounds
        if collision:
            if soundFreq==400:
                soundFreq=800
            else:
                soundFreq=400
        
            buzzer.freq(soundFreq)
            buzzer.duty_u16(2000)
        
        # clear the screen
        oled.fill(0)
        
        # display the paddle
        oled.fill_rect(paddleX, PADDLE_Y, PADDLE_WIDTH, PADDLE_HEIGHT, 1)
        
        # display the ball
        oled.fill_rect(ballX, ballY, BALL_SIZE, BALL_SIZE, 1)
        
        # display the score
        oled.text(str(score), SCREEN_WIDTH-int(len(str(score))*8), 0)
        
        oled.show()
        
        time.sleep(0.001)
        buzzer.duty_u16(0)
        
while True:
    pico_pong_main()

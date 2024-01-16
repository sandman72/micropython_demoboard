# PicoGame.py by YouMakeTech
# A class to easily write games for the Raspberry Pi Pico RetroGaming System
#
# Adapted to work with the Attraktor MicroPython Demo Board
# by Frank Hellmann 11.2023
#
# Original Code:
# https://github.com/YouMakeTech/PicoRetroGamingSystem
# 
from machine import Pin, PWM, I2C, Timer
from ssd1306 import SSD1306_I2C
from framebuf import FrameBuffer, MONO_HLSB
import time
import random

class PicoGame(SSD1306_I2C):
    def __init__(self):
        self.SCREEN_WIDTH = 128
        self.SCREEN_HEIGHT = 64
        self.__up = Pin(11, Pin.IN, Pin.PULL_DOWN)
        self.__down = Pin(14, Pin.IN, Pin.PULL_DOWN)
        self.__left = Pin(12, Pin.IN, Pin.PULL_DOWN)
        self.__right = Pin(13, Pin.IN, Pin.PULL_DOWN)
        self.__button_A = Pin(15, Pin.IN, Pin.PULL_DOWN)
        self.__buzzer = PWM(Pin(10))
        
        self.__i2c = I2C(0, sda=Pin(20), scl=Pin(21))
        super().__init__(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.__i2c)
        
        self.__fb=[] # Array of FrameBuffer objects for sprites
        self.__w=[]
        self.__h=[]
    
    def center_text(self, s, color = 1):
        x = int(self.width/2)- int(len(s)/2 * 8)
        y = int(self.height/2) - 8
        self.text(s, x, y, color)
        
    def top_right_corner_text(self, s, color = 1):
        x = self.width - int(len(s) * 8)
        y = 0
        self.text(s, x, y, color)
        
    def add_sprite(self, buffer, w, h):
        fb = FrameBuffer(buffer, w, h, MONO_HLSB)
        self.__fb.append(fb)
        self.__w.append(w)
        self.__h.append(h)
       
    def sprite(self, n, x, y):
        self.blit(self.__fb[n], x, y)
        
    def sprite_width(self,n):
        return self.__w[n]
    
    def sprite_height(self,n):
        return self.__h[n]
        
    def button_up(self):
        return self.__up.value()==1
    
    def button_down(self):
        return self.__down.value()==1
    
    def button_left(self):
        return self.__left.value()==1
    
    def button_right(self):
        return self.__right.value()==1
    
    def button_A(self):
        return self.__button_A.value()==1
    
    def button_B(self):
        # MicroPython Demo Board only has 5 Buttons
        return self.__button_A.value()==1
    
    def any_button(self):
        # returns True if any button is pressed
        button_pressed=False
        if self.button_up():
            button_pressed = True
        if self.button_down():
            button_pressed = True
        if self.button_left():
            button_pressed = True
        if self.button_right():
            button_pressed = True
        if self.button_A():
            button_pressed = True
        if self.button_B():
            button_pressed = True
        return button_pressed
    
    def sound(self, freq, duty_u16 = 2000):
        # Make a sound at the selected frequency in Hz
        if freq>0:
            self.__buzzer.freq(freq)
            self.__buzzer.duty_u16(duty_u16)
        else:
            self.__buzzer.duty_u16(0)
   
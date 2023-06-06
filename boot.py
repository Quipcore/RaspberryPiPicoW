# boot.py -- run on boot-up

from machine import Pin, Timer

onBoardLed = Pin(25, Pin.OUT)
onBoardLed.value(1)

led = Pin(15, Pin.OUT)
timer = Timer()

def blink(timer):
    led.toggle()

timer.init(freq=2.5, mode=Timer.PERIODIC, callback=blink)
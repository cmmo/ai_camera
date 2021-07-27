from gpiozero import *
from time import sleep
led = LED(21)
button = Button(4)

while True:
    button.wait_for_press()
    led.toggle()
    sleep(0.5)

from gpiozero import *
from time import sleep
from multiprocessing import Process, Value
import sys
import os
from signal import pause

green = LED(5)
red = LED(12)
led = LED(21)
pid = 0
green_button = Button(4)
red_button = Button(22)
error_frame_count = 0
normal_frame_count = 0
alarm_manual_stopped = False
error_frame_count_threshhold = 20
normal_frame_count_threshhold = 20

def led01():
    sys.stderr.write("*** ff01 *** alarm_start ***")
    while True:
        led.toggle()
        sleep(0.1)
    sys.stderr.write("*** ff01 *** alarm_end ***")
#
# --------------------------------------------------------------------
def alarm_start():
    global pid
    global led
    global green
    global red
    global error_frame_count
    global normal_frame_count
    global error_frame_count_threshhold
    global normal_frame_count_threshhold

    green.off()
    red.on()

    if pid: #alarm already started
        pass
    else:
        error_frame_count += 1				    
			   
        #print("Error", "error:", error_frame_count, "normal:", normal_frame_count)			
        if error_frame_count > error_frame_count_threshhold:			   
            normal_frame_count = 0			
			
            pp3 = Process(target=led01,)			
            pp3.start()			
            pid = pp3.pid			
            print(pid, "alarm_start")			
            pp3.join(1)			

def alarm_stop():
    global pid
    global led
    global green
    global red
    global error_frame_count
    global normal_frame_count
    global alarm_manual_stopped
    global error_frame_count_threshhold
    global normal_frame_count_threshhold

    green.on()
    red.off()

    if pid:
        if alarm_manual_stopped:
            os.kill(pid, 9)
            print(pid, "Manual killed")
            pid = 0
            led.off()
            error_frame_count = 0
            normal_frame_count = 0
            return

        print("Normal", "error:", error_frame_count, "normal:", normal_frame_count)
        normal_frame_count += 1

        if normal_frame_count > normal_frame_count_threshhold:
            error_frame_count = 0

            os.kill(pid, 9)
            print(pid, "killed")
            pid = 0
            led.off()
    else:
        error_frame_count = 0

#
# --------------------------------------------------------------------
sys.stderr.write("alarm init\n")
#

def alarm_init():
    green.on()

    green_button.when_pressed = alarm_manual_start 
    red_button.when_pressed = alarm_manual_stop 

def alarm_manual_start():
    global alarm_manual_stopped
    alarm_manual_stopped = False
    alarm_start()
    sys.stderr.write("Manual started\n")

def alarm_manual_stop():
    global alarm_manual_stopped
    alarm_manual_stopped = True
    alarm_stop()
    sys.stderr.write("Manual stopped\n")

#alarm_init()
#pause()


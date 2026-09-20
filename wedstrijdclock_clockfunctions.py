# Script with functions to communicate with the clock via the IR led
# See also https://github.com/kentwait/ircodec
# Created 29-8-2026 by Jan

# Inputs
delay = 0.05

import time as timesleep
from datetime import datetime, time, date
import pigpio
from ircodec.command import CommandSet

pi = pigpio.pi()
clockremote = CommandSet.load('wedstrijdklokcommandos_v1.json')

def resetclock():
    # Resets the clock to show the current time
    timesleep.sleep(delay)
    clockremote.emit('exitt')
    timesleep.sleep(delay)
    clockremote.emit('ok')
    timesleep.sleep(delay)
    clockremote.emit('clock')
    return None

def toggle10sectimer():
    # Toggles the 10 sec countdown timer
    resetclock()
    timesleep.sleep(delay)
    clockremote.emit('updn')
    timesleep.sleep(delay)
    clockremote.emit('10s')
    timesleep.sleep(delay)
    clockremote.emit('clock')
    return None

def transmitcount(stringtime,direction):
    # Transmits a countdown or -up time depending on the direction
    # Inputs:
    # - stringtime: str format "HH:MM:SS"
    # - direction: str format "up" or "down"
    print("Transmitting count ",stringtime)
    resetclock()
    timesleep.sleep(delay)
    if direction == "up":
        clockremote.emit('arrow_up')
    else:
        clockremote.emit('arrow_down')
    timesleep.sleep(delay)
    clockremote.emit('edit')
    for digit in stringtime:
        if not digit == ':':
            print(digit)
            timesleep.sleep(delay)
            clockremote.emit(digit)
    timesleep.sleep(delay)
    clockremote.emit('edit')
    timesleep.sleep(delay)
    clockremote.emit('ok')
    return None
    
    

# Script with functions to communicate with the clock via the IR led
# See also https://github.com/kentwait/ircodec
# Created 29-8-2026 by Jan

# Inputs
delay = 0.05

import time as timesleep
import pigpio
from ircodec.command import CommandSet

pi = pigpio.pi()
clockremote = CommandSet.load('wedstrijdklokcommandos_v1.json')
static = False

def updateclockAPIdata(HF, HCU, HCD, HL, showlaps):
    # Updates clock based on last start, heat count up and down
    # Input:
    # - HF: heat finished bool
    # - HCU: count up time from previous start ("HH:MM:SS")
    # - HCD: count down time to next start ("HH:MM:SS")
    # - HL: laps to go shown statically ("LL:00:00")
    # - showlaps: decide to show HCU/HCD or HL bool
    if showlaps:
        transmitlaps(HL)
    else:
        if HF:
            transmitcount(HCD,"down")
        else:
            transmitcount(HCU,"up") 
    return None

def resetclock(static):
    # Resets the clock to show the current time
    # Input:
    # - static: if static (in edit mode), two times ok needed to reset bool
    timesleep.sleep(delay)
    clockremote.emit('exitt')
    timesleep.sleep(delay)
    clockremote.emit('ok')
    if static:
        timesleep.sleep(11) # In case 10 sec timer is on
        timesleep.sleep(delay)
        clockremote.emit('ok')
    timesleep.sleep(delay)
    clockremote.emit('clock')
    return None

def toggle10sectimer():
    global static
    # Toggles the 10 sec countdown timer
    resetclock(static)
    timesleep.sleep(delay)
    clockremote.emit('updn')
    timesleep.sleep(delay)
    clockremote.emit('10s')
    timesleep.sleep(delay)
    clockremote.emit('clock')
    return None

def transmitlaps(laptime):
    global static
    # Transmits a static display of the laps
    # Inputs:
    # - laptime: str format "LL:00:00"
    print("Transmitting lap ",laptime)
    resetclock(static)
    timesleep.sleep(delay)
    clockremote.emit('arrow_up')
    timesleep.sleep(delay)
    clockremote.emit('edit')
    for digit in laptime:
        if not digit == ':':
            print(digit)
            timesleep.sleep(delay)
            clockremote.emit(digit)
    timesleep.sleep(delay)
    clockremote.emit('edit')
    static = True
    return None
    
def transmitcount(stringtime,direction):
    # Transmits a countdown or -up time depending on the direction
    # Inputs:
    # - stringtime: str format "HH:MM:SS"
    # - direction: str format "up" or "down"
    global static
    print("Transmitting count ",stringtime)
    resetclock(static)
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
    static = False
    return None
    
    

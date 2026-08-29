# Script with functions of the standalone version to interact with web interface
# Based on wedstrijdclock_standalone.py
# Created 29-8-2026 by Jan

# Default inputs (will be used upon boot)
hostip = "192.168.12.11"
APIkeyLS = "7HUD0KZI591RKFXN9YBX59IR7XK8PD2E" # Last start
APIkeyHF = "08AKUIWFO68J2NWCFPEF130NIBG7BD6X" # Heat finished
APIkeyNS = "YVP26HP04JD9CWEKHTOBIQGLPCBOFI44" # Next start
bluepin = 16
greenpin = 6
redpin = 5

import requests
import xml.etree.ElementTree as ET
import time as timesleep
from datetime import datetime, time, date
import pigpio
from ircodec.command import CommandSet

# prevLS = datetime.now()
# prevHF = None
# prevNS = datetime.now()
pi = pigpio.pi()
clockremote = CommandSet.load('wedstrijdklokcommandos_v1.json')
pi.write(bluepin,0)
pi.write(redpin,0)
pi.write(greenpin,0)

def resetclock():
    # Resets the clock to show the current time
    timesleep.sleep(0.5)
    clockremote.emit('exitt')
    timesleep.sleep(0.5)
    clockremote.emit('ok')
    timesleep.sleep(0.5)
    clockremote.emit('clock')
    return None

def toggle10sectimer():
    # Toggles the 10 sec countdown timer
    resetclock()
    timesleep.sleep(0.5)
    clockremote.emit('updn')
    timesleep.sleep(0.5)
    clockremote.emit('10s')
    timesleep.sleep(0.5)
    clockremote.emit('clock')
    return None

def transmitcount(stringtime,direction):
    # Transmits a countdown or -up time depending on the direction
    # Inputs:
    # - stringtime: str format "HH:MM:SS"
    # - direction: str format "up" or "down"
    print("Transmitting count ",stringtime)
    resetclock()
    timesleep.sleep(0.5)
    if direction == "up":
        clockremote.emit('arrow_up')
    else:
        clockremote.emit('arrow_down')
    timesleep.sleep(0.5)
    clockremote.emit('edit')
    for digit in stringtime:
        if not digit == ':':
            print(digit)
            timesleep.sleep(0.5)
            clockremote.emit(digit)
    timesleep.sleep(0.5)
    clockremote.emit('edit')
    timesleep.sleep(0.5)
    clockremote.emit('ok')
    return None

def updateclockLSNS(LS,NS,HF):
    if HF:
        TTS = NS-datetime.now()
        direction = "down"
    else:
        TTS = datetime.now()-LS
        direction = "up"
        
    if TTS.days < 0:
        TTS = "00:00:00"
    
    if TTS.seconds < 10*60*60:
        TTS = '0'+str(TTS)[:7]
    else:
        TTS = str(TTS)[:8]
        
    timesleep.sleep(1)
    transmitcount(TTS,direction)
    
    return None

def fetchtime(url):
    try:
        response = requests.get(url,timeout=1)
        root = ET.fromstring(response.content)
        for i,item in enumerate(root):
            if i == 0:
                for subitem in item:
                    value = datetime.combine(date.today(),time(int(subitem.text[0:2]),int(subitem.text[3:5]),int(subitem.text[6:7])))
        e = None
        
    except Exception as e:
        print(e)
        value = None
        
    return value, e

def fetchbool(url):
    try:
        response = requests.get(url,timeout=1)
        root = ET.fromstring(response.content)
        for i,item in enumerate(root):
            if i == 0:
                for subitem in item:
                    value = bool(int(subitem.text))
    except Exception as e:
        print(e)
        value = None
    return value

# 
# while True:
#     update = False
#     timesleep.sleep(5)
#     baseURL = "http://"+hostip+"/_SLFCT/api/"
#     LS = fetchtime(baseURL+APIkeyLS)
#     HF = fetchbool(baseURL+APIkeyHF)
#     NS = fetchtime(baseURL+APIkeyNS)
# #     print(NS)
# #     print(LS)
# #     print(HF)
#     if None in [LS,HF,NS]:
#         print("Fetch failed")
#         pi.write(redpin,0)
#         pi.write(greenpin,0)
#         pi.write(bluepin,1)   
#         clockremote.emit('ok')
#         clockremote.emit('clock')
#     else:
#         pi.write(redpin,0)
#         pi.write(greenpin,1)
#         pi.write(bluepin,0)
#         if prevHF != HF:
#             prevHF = HF
#             update = True
#         if prevLS != LS:
#             prevLS = LS
#             update = True
#         if prevNS != NS:
#             prevNS = NS
#             update = True
#         if update:
#             ok = updateclock(LS,NS,HF)
#             if not ok:
#                 print("Clock update failed")
#                 pi.write(redpin,1)
#                 pi.write(greenpin,0)
#                 pi.write(bluepin,0)
    

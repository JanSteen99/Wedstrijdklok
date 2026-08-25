# Script to perform repeated xml reading and parsing to communicate with rr api
# Based on read_xml_test.py
# Created 25-8-2026 by Jan

# Input
hostip = "192.168.12.11"
APIkeyLS = "7HUD0KZI591RKFXN9YBX59IR7XK8PD2E" # Last start
APIkeyHF = "08AKUIWFO68J2NWCFPEF130NIBG7BD6X" # Heat finished
APIkeyNS = "YVP26HP04JD9CWEKHTOBIQGLPCBOFI44" # Next start

import requests
import xml.etree.ElementTree as ET
import time as timesleep
from datetime import datetime, time, date

prevLS = datetime.now()
prevHF = None
prevNS = datetime.now()

def updateclock(LS,NS,HF):
    print("Update!")
    return None

while True:
    update = False
    timesleep.sleep(1)
    # Fetch XMLs
    urlLS = "http://"+hostip+"/_SLFCT/api/"+APIkeyLS
    response = requests.get(urlLS)
    root = ET.fromstring(response.content)
    for i,item in enumerate(root):
        if i == 0:
            for subitem in item:
                LS = datetime.combine(date.today(),time(int(subitem.text[0:2]),int(subitem.text[3:5]),int(subitem.text[6:7])))
#                 print(LS)
    urlHF = "http://"+hostip+"/_SLFCT/api/"+APIkeyHF
    response = requests.get(urlHF)
    root = ET.fromstring(response.content)
    for i,item in enumerate(root):
        if i == 0:
            for subitem in item:
                HF = bool(subitem.text)
#                 print(HF)
    urlNS = "http://"+hostip+"/_SLFCT/api/"+APIkeyNS
    response = requests.get(urlNS)
    root = ET.fromstring(response.content)
    for i,item in enumerate(root):
        if i == 0:
            for subitem in item:
                NS = datetime.combine(date.today(),time(int(subitem.text[0:2]),int(subitem.text[3:5]),int(subitem.text[6:7])))
#                 print(NS)
    print(NS-LS)
    if prevHF != HF:
        prevHF = HF
        update = True
    if prevLS != LS:
        prevLS = LS
        update = True
    if prevNS != NS:
        prevNS = NS
        update = True
    
    if update:
        updateclock(LS,NS,HF)
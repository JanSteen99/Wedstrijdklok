# Script with functions to interact with the raceresult API through requests
# Created 20-9-2026 by Jan

import requests
import json
import xml.etree.ElementTree as ET
from datetime import datetime, time, date

# Inputs
IP = "192.168.178.38"  # RR server IP Ziggo
# IP = "192.168.12.11"  # RR server IP TPLink

def fetcheventidAPIkey():

    eventid = 0
    APIkey = "0"

    url1 = f"http://{IP}/api/local/eventlist"
    foundAPI = True
    try:
        r = requests.get(url1, params={"lang": "en"}, timeout=5)
    except Exception as e:
        print(e)
        foundAPI = False

    if foundAPI:
        
        eventid = r.json()[0]["ID"]
        print(eventid)

        url2 = f"http://{IP}/_{eventid}/api/simpleapi/get"
        
        try:
            r = requests.get(url2, params={"lang": "en", "pw": "0"}, timeout=5)
        
        except Exception as e:
            print(e)
            foundAPI = False
        
        if foundAPI:
            
            APIkey = r.json()[0]["Key"]
            print(APIkey)
    
    return foundAPI, eventid, APIkey

def updateclockAPIdata(LS,HF,NS):
    # Updates clock based on last start, heat finished and next start
    # Input:
    # - LS: last start datetime.datetime
    # - HF: heat finished bool
    # - NS: next start datetime.datetime
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

def fetchdata(url):
    response = requests.get(url,timeout=1)
    root = ET.fromstring(response.content)
    elem = root[0]
    HF = bool(int(elem[0].text))
    HCUtxt= elem[1].text
    HCU = datetime.combine(date.today(),time(int(HCUtxt[0:2]),int(HCUtxt[3:5]),int(HCUtxt[6:7])))
    HCDtxt= elem[2].text
    HCD = datetime.combine(date.today(),time(int(HCDtxt[0:2]),int(HCDtxt[3:5]),int(HCDtxt[6:7])))
    return HF, HCU, HCD

# foundAPI, eventid, APIkey = fetcheventidAPIkey()
# url = "http://"+IP+"/_"+eventid+"/api/"+APIkey
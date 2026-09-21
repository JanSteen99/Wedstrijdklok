# Script with functions to interact with the raceresult API through requests
# Created 20-9-2026 by Jan

import requests
import json
import xml.etree.ElementTree as ET

# Inputs
# IP = "192.168.178.38"  # RR server IP Ziggo
IP = "192.168.12.11"  # RR server IP TPLink

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


def fetchdata(url):
    response = requests.get(url,timeout=1)
    root = ET.fromstring(response.content)
    elem = root[0]
    HF = bool(int(elem[0].text))
    HCUtxt= elem[1].text
    if HCUtxt is not None:
        HCU = HCUtxt[0:8]
    else:
        HCU = "00:00:00" 
    HCDtxt= elem[2].text
    if HCDtxt is not None:
        HCD = HCDtxt[0:8]
    else:
        HCD = "00:00:00"    
    return HF, HCU, HCD

# foundAPI, eventid, APIkey = fetcheventidAPIkey()
# url = "http://"+IP+"/_"+eventid+"/api/"+APIkey
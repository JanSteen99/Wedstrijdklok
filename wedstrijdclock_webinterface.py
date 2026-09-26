### Main script to host a local webpage, to read out the API and to interact with the RPI controlling the wedstrijdclock
### See also https://www.aranacorp.com/en/create-a-web-interface-to-control-your-raspberry-pi/
### Created on 29-08-2026 by Jan

import os
import pigpio
from flask import Flask, render_template, Response, request, jsonify
import threading

import wedstrijdclock_clockfunctions as clock
import wedstrijdclock_APIfunctions as API
import time

# Inputs
bluepin = 16 #GPIO pin
greenpin = 6 #GPIO pin
redpin = 5 #GPIO pin
eventid = "0"
APIkey = "0"
autoupdate = False
showlaps = False

# Script
pi = pigpio.pi()
dataPin=[i for i in range(2,28)]
for dp in dataPin:
    pi.set_mode(dp,pigpio.OUTPUT)

def autoupdate_checker():
    url = "http://"+API.IP+"/_"+eventid+"/api/"+APIkey
    HF, HCU, HCD, HL = API.fetchdata(url)
    HFold = HF
    HLold = HL
    
    while True:
        
        if autoupdate:
            print("Autoupdate is enabled - checking changes in HF or HL")
            
            try:
                url = "http://"+API.IP+"/_"+eventid+"/api/"+APIkey
                HF, HCU, HCD, HL = API.fetchdata(url)
                if showlaps:
                    if HLold != HL:
                        clock.updateclockAPIdata(HF, HCU, HCD, HL, showlaps)
                        HLold = HL
                else:
                    if HFold != HF:
                        clock.updateclockAPIdata(HF, HCU, HCD, HL, showlaps)
                        HFold = HF
            except Exception as e:
                print(e)
                pi.write(redpin,1)
                pi.write(greenpin,0)
                pi.write(bluepin,0)

        time.sleep(5)  # check every 10 seconds for a change

templateData={
    'title':'RPi Wedstrijdklok Web Interface'
}

app=Flask(__name__,template_folder='.',static_folder='static',static_url_path='/static')
# 
@app.route('/')

def index():
    #return 'hello world!'
    templateData={
        'title':'Raspberry Pi 3B+ Web Controller'
    }
    #return render_template('rpi_index.html',**templateData)
    return render_template('rpi_webcontroller_v2.html',**templateData)
#     return "Flask is working!"
# @app.route("/testjquery")
# def testjquery():
#     return app.send_static_file("jquery.min.js")
@app.route('/<actionid>')
def handleRequest(actionid):
    global eventid, APIkey, connectionfound, autoupdate, showlaps
    
    if not actionid == "favicon.ico":
        
        errorfound=False
        
        try:
            
            print("Button pressed with action id: ",actionid)
            
            text = request.args.get("text",'')
            print("Text received: ",text)
            timeuser = request.args.get("time",'')
            print("Time received: ",timeuser," type ",type(timeuser))
            checked = request.args.get("checked")
            print("Check received: ",checked," type ",type(checked))
            
            if actionid == "resetclock":
                clock.resetclock()
            elif actionid == "toggle10sec":
                clock.toggle10sectimer()
                
            elif actionid == "showkeyid":
                print("Sending eventID and API keys to HTML")
                return jsonify(text1=eventid,
                               text2=APIkey)
            elif actionid == "sendeventid":
                print("Setting event id from HTML")
                eventid = str(text)
            elif actionid == "sendAPIkey":
                print("Setting API key from HTML")
                APIkey = str(text)
            elif actionid == "fetchkeyid":
                print("Retry fetching eventid and APIkey from RR webapp")
                foundAPI, eventid, APIkey = API.fetcheventidAPIkey()
                if foundAPI:
                    connectionfound = True
                else:
                    connectionfound = False
            
            elif timeuser:
                if actionid == "senduserup":
                    clock.transmitcount(timeuser,"up")
                else:
                    clock.transmitcount(timeuser,"down")
                    
            elif actionid == "autoAPIupdate":
                if checked == "true":
                    autoupdate = True
                else:
                    autoupdate = False
            elif actionid == "showinglaps":
                if checked == "true":
                    showlaps = True
                else:
                    showlaps = False    
            elif actionid == "getAPIdata":
                print("Sending API data to HTML")
                url = "http://"+API.IP+"/_"+eventid+"/api/"+APIkey
                HF, HCU, HCD, HL = API.fetchdata(url)
                return jsonify(text1=HF,
                               text2=HCU,
                               text3=HCD,
                               text4=HL)
            
            elif actionid == "setAPIdata":
                print("Updating clock based on API data!")
                url = "http://"+API.IP+"/_"+eventid+"/api/"+APIkey
                HF, HCU, HCD, HL = API.fetchdata(url)
                clock.updateclockAPIdata(HF, HCU, HCD, HL, showlaps)
        
        except Exception as e:
            print(e)
            errorfound=True
            
        if errorfound:
            pi.write(redpin,1)
            pi.write(greenpin,0)
            pi.write(bluepin,0)
        else:
            if not connectionfound:
                pi.write(redpin,0)
                pi.write(greenpin,0)
                pi.write(bluepin,1)
            else:
                pi.write(redpin,0)
                pi.write(greenpin,1)
                pi.write(bluepin,0)
                
    return "OK 200"   
                              
if __name__=='__main__':
#     os.system("sudo rm -r  ~/.cache/chromium/Default/Cache/*")
    
    ## Initialize
    clock.resetclock(clock.static)
    clock.resetclock(not clock.static)
    clock.toggle10sectimer()
    clock.transmitcount("00:00:00","up")
    time.sleep(11)
    clock.resetclock(clock.static)
    
    pi.write(redpin,0)
    pi.write(greenpin,0)
    pi.write(bluepin,0)
#     print(app.url_map)
#     print(app.static_folder)
#     print(os.path.exists(os.path.join(app.static_folder,"jquery.min.js")))
    try:
        foundAPI, eventid, APIkey = API.fetcheventidAPIkey()
        if foundAPI:
            connectionfound = True
            pi.write(redpin,0)
            pi.write(greenpin,1)
            pi.write(bluepin,0)
        else:
            connectionfound = False
            pi.write(redpin,0)
            pi.write(greenpin,0)
            pi.write(bluepin,1)
        
        updater = threading.Thread(target=autoupdate_checker,daemon=True)
        updater.start()
                
    except Exception as e:
        print(e)
        pi.write(redpin,1)
        pi.write(greenpin,0)
        pi.write(bluepin,0)
    ## Run web application
    app.run(debug=True, port=5000, host='0.0.0.0',threaded=True, use_reloader=False)
    #local web server http://192.168.1.200:5000/
    #after Port forwarding Manipulation http://xx.xx.xx.xx:5000/
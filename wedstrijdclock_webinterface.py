### Main script to host a local webpage, to read out the API and to interact with the RPI controlling the wedstrijdclock
### See also https://www.aranacorp.com/en/create-a-web-interface-to-control-your-raspberry-pi/
### Created on 29-08-2026 by Jan

import os
import pigpio
from flask import Flask, render_template, Response, request, jsonify
import datetime

import wedstrijdclock_clockfunctions as clock
import wedstrijdclock_APIfunctions as API

# Inputs
bluepin = 16
greenpin = 6
redpin = 5
eventid = "0"
APIkey = "0"

# Script
pi = pigpio.pi()
dataPin=[i for i in range(2,28)]
for dp in dataPin:
    pi.set_mode(dp,pigpio.OUTPUT)

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
    return render_template('rpi_webcontroller.html',**templateData)           
# @app.route("/testjquery")
# def testjquery():
#     return app.send_static_file("jquery.min.js")
@app.route('/<actionid>')
def handleRequest(actionid):
    global eventid, APIkey, connectionfound
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
                    print("Yey im ticked")
                    pass
                else:
                    print("No im un-ticked")
                    pass
            elif actionid == "getAPIdata":
                print("Sending API data to HTML")
                url = "http://"+API.IP+"/_"+eventid+"/api/"+APIkey
                HF, HCU, HCD = API.fetchdata(url)
                return jsonify(text1=HF,
                               text2=HCU.strftime("%H:%M:%S"),
                               text3=HCD.strftime("%H:%M:%S"))
            elif actionid == "setAPIdata":
                print("Updating clock based on API data!")
                LS, HF, NS, ex = clock.fetchAPIdata()
                if ex == None:
                    clock.updateclockAPIdata(LS,HF,NS)
                else:
                    print("Couldn't due to error")
          
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
    clock.resetclock()
    clock.toggle10sectimer()
    pi.write(redpin,0)
    pi.write(greenpin,0)
    pi.write(bluepin,0)
#     print(app.url_map)
#     print(app.static_folder)
#     print(os.path.exists(os.path.join(app.static_folder,"jquery.min.js")))
    foundAPI, eventid, APIkey = API.fetcheventidAPIkey()
    if foundAPI:
        connectionfound = True
    else:
        connectionfound = False
    ## Run web application
    app.run(debug=True, port=5000, host='0.0.0.0',threaded=True, use_reloader=False)
    #local web server http://192.168.1.200:5000/
    #after Port forwarding Manipulation http://xx.xx.xx.xx:5000/
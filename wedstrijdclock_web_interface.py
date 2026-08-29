### Code to test and host a local webpage to interact with the RPI controlling the wedstrijdclock
### Based on https://www.aranacorp.com/en/create-a-web-interface-to-control-your-raspberry-pi/
### Created on 29-08-2026 by Jan

import os
import pigpio
from flask import Flask, render_template, Response, request, jsonify
import datetime
import wedstrijdclock_functions as piclock

pi = pigpio.pi()
dataPin=[i for i in range(2,28)]
for dp in dataPin:
    pi.set_mode(dp,pigpio.OUTPUT)

    
data=[]
now=datetime.datetime.now()
timeString=now.strftime("%Y-%m-%d %H:%M")
templateData={
    'title':'RPi Wedstrijdklok Web Interface',
    'time':timeString,
    'data':data,
}

def getData():
    data=[]
#     for dp in dataPin:
#         data.append(pi.read(dp))
    return data

app=Flask(__name__,template_folder='.',static_folder='static',static_url_path='/static')
# 
@app.route('/')

def index():
    #return 'hello world!'
    now=datetime.datetime.now()
    timeString=now.strftime("%Y-%m-%d %H:%M")
    data=getData()
    templateData={
        'title':'Raspberry Pi 3B+ Web Controller',
        'time':timeString,
        'data':data,
    }
    #return render_template('rpi_index.html',**templateData)
    return render_template('rpi_webcontroller.html',**templateData)           
# @app.route("/testjquery")
# def testjquery():
#     return app.send_static_file("jquery.min.js")
@app.route('/<actionid>')
def handleRequest(actionid):
    if not actionid == "favicon.ico":
        print("Button pressed: ",actionid)
        text = request.args.get("text",'')
        print("Text received: ",text)
        timeuser = request.args.get("time",'')
        print("Time received: ",timeuser," type ",type(timeuser))
        if actionid == "resetclock":
            piclock.resetclock()
        elif actionid == "toggle10sec":
            piclock.toggle10sectimer()
        elif actionid == "getkeys":
            print("Sending API keys to HTML")
            return jsonify(text1=piclock.APIkeyLS,
                           text2=piclock.APIkeyHF,
                           text3=piclock.APIkeyNS)
        elif actionid == "sendLSkey":
            print("Setting LS key from HTML")
            piclock.APIkeyLS = text
        elif actionid == "sendHFkey":
            print("Setting HF key from HTML")
            piclock.APIkeyHF = text
        elif actionid == "sendNSkey":
            print("Setting NS key from HTML")
            piclock.APIkeyNS = text
        elif timeuser:
            if actionid == "senduserup":
                piclock.transmitcount(timeuser,"up")
            else:
                piclock.transmitcount(timeuser,"down")
        elif actionid == "getAPIdata":
            print("Sending API data to HTML")
            LS, HF, NS, ex = piclock.fetchAPIdata()
            if ex == None:
                ex = "No error"
            return jsonify(text1=LS,
                           text2=HF,
                           text3=NS,
                           text4=ex)
        elif actionid == "setAPIdata":
            print("Updating clock based on API data!")
            LS, HF, NS, ex = piclock.fetchAPIdata()
            if ex == None:
                piclock.updateclockAPIdata(LS,HF,NS)
            else:
                print("Couldn't due to error")
            
        
    return "OK 200"   
                              
if __name__=='__main__':
#     os.system("sudo rm -r  ~/.cache/chromium/Default/Cache/*")
    piclock.resetclock()
    piclock.toggle10sectimer()
    pi.write(piclock.redpin,1)
    pi.write(piclock.greenpin,0)
    pi.write(piclock.bluepin,0)
    print(app.url_map)
    print(app.static_folder)
    print(os.path.exists(os.path.join(app.static_folder,"jquery.min.js")))
    app.run(debug=True, port=5000, host='0.0.0.0',threaded=True, use_reloader=False)
    #local web server http://192.168.1.200:5000/
    #after Port forwarding Manipulation http://xx.xx.xx.xx:5000/
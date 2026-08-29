### Code to test and host a local webpage to interact with the RPI controlling the wedstrijdclock
### Based on https://www.aranacorp.com/en/create-a-web-interface-to-control-your-raspberry-pi/
### Created on 29-08-2026 by Jan

import os
import pigpio
from flask import Flask, render_template, Response
import datetime

pi = pigpio.pi()
dataPin=[i for i in range(2,28)]
for dp in dataPin:
    pi.set_mode(dp,pigpio.OUTPUT)

    
data=[]
now=datetime.datetime.now()
timeString=now.strftime("%Y-%m-%d %H:%M")
templateData={
    'title':'Raspberry Pi 3B+ Web Controller',
    'time':timeString,
    'data':data,
}

def getData():
    data=[]
    for dp in dataPin:
        data.append(pi.read(dp))
    return data

app=Flask(__name__,template_folder='.',static_folder='.')
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
    return render_template('rpi3b_webcontroller_test.html',**templateData)           

@app.route('/<actionid>')

def handleRequest(actionid):
    print("Button pressed :",actionid)
    if actionid[:3] == "dig":
        if actionid.endswith("on"):
            pi.write(int(actionid[3:-2]),1)
        else:
            pi.write(int(actionid[3:-3]),0)
    return "OK 200"   
                              
if __name__=='__main__':
#     os.system("sudo rm -r  ~/.cache/chromium/Default/Cache/*")
    app.run(debug=True, port=5000, host='0.0.0.0',threaded=True, use_reloader=False)
    #local web server http://192.168.1.200:5000/
    #after Port forwarding Manipulation http://xx.xx.xx.xx:5000/
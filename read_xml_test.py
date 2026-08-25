# Script to test the xml reading and parsing to communicate with rr api
# Based on https://www.zyte.com/learn/a-practical-guide-to-xml-parsing-with-python/
# Created 23-8-2026 by Jan
hostip = "192.168.12.11"
APIkey = "7HUD0KZI591RKFXN9YBX59IR7XK8PD2E"
import requests
import xml.etree.ElementTree as ET

# Fetch XML from a URL
url = "http://"+hostip+"/_SLFCT/api/"+APIkey
print(url)
response = requests.get(url)
root = ET.fromstring(response.content)

# Print root tag
print(root.tag)

# Orint first item and its subitem containing the time
for i,item in enumerate(root):
    if i == 0:
        for subitem in item:
            print(subitem.text)

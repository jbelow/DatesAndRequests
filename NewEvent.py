from picamera import PiCamera
from datetime import datetime
import requests
import json
from gpiozero import Button
from time import sleep
import random

# init button
# button = Button(8)
# button.when_released = log

button = Button(25)
camera = PiCamera()

camera.start_preview()
while True:
    try:
        button.wait_for_press()
        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%dT%H:%M:%S")
        date = now.strftime("%Y-%m-%d")
        camera.annotate_text = dt_string
        print("New photo: " + dt_string)
        camera.capture('//home/pi/adv-web-services/photos/photo%s.jpg' % dt_string)

        ranLocation = random.randint(1, 3) 
        
        # create a new event - replace with your API
        url = 'https://modas-jsg.azurewebsites.net/api/event/'
        headers = { 'Content-Type': 'application/json'}
        payload = { 'timestamp': dt_string, 'flagged': False, 'locationId': ranLocation }
        print(payload)
        # post the event
        r = requests.post(url, headers=headers, data=json.dumps(payload))
        print(r.status_code)
        print(r.json())
        
        print("printed to log file")
        filename = "//home/pi/adv-web-services/" + date + ".log"
        f = open(filename, "a")
        f.write(dt_string + ",False" + str(ranLocation)+"," + str(r.status_code) + "\n")
        f.close()
        
    except KeyboardInterrupt:
        camera.stop_preview()
        break


try:
    # program loop
    while True:
        sleep(.001)
# detect Ctlr+C
except KeyboardInterrupt:
    print("goodbye")

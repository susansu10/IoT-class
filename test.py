import time, requests, random
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)
p = GPIO.PWM(12, 50)

from gpiozero import LED, DistanceSensor
from time import sleep
sensor = DistanceSensor(echo=27, trigger=17)

import threading, sys    #
import json

R_pin = 33
G_pin = 35
B_pin = 37

GPIO.setup(R_pin, GPIO.OUT)
GPIO.setup(G_pin, GPIO.OUT)
GPIO.setup(B_pin, GPIO.OUT)

R_pwm = GPIO.PWM(R_pin, 800)
G_pwm = GPIO.PWM(G_pin, 800)
B_pwm = GPIO.PWM(B_pin, 800)
# use python RPi.GPIO, square wave is 70k Hz
# use python wiringpi2 or bindings, square wave is 28k Hz
# use C wiringPi, square wave is 4.1-4.6M Hz

R_pwm.start(0)
G_pwm.start(0)
B_pwm.start(0)

def get_data():

    url = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001"
    params = {
        "Authorization": "CWB-3446C69D-5075-433C-9F01-6A6C4F5D8925",
        "format": "JSON",
        "locationName": "花蓮縣"
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        # print(response.text)
        data = json.loads(response.text)
        weather_elements = data["records"]["location"][0]["weatherElement"]
        rain_prob = weather_elements[1]["time"][0]["parameter"]["parameterName"]
        print("降雨機率 = ", rain_prob, "%")
        if int(rain_prob) > 10:
            GPIO.setmode(GPIO.BOARD)
            p.start(50)
            p.ChangeFrequency(659)
            time.sleep(1)
            p.stop()
    else:
        print("Can't get data!")

try:
    while(1):
        dis = sensor.distance * 100
        print('{0:.1f}cm'.format(dis))
        if dis < 10:
            print("distance < 10")
            R_pwm.ChangeDutyCycle(0)
            G_pwm.ChangeDutyCycle(100)
            B_pwm.ChangeDutyCycle(100)
            get_data()
        else:
            print("distance > 10")
            R_pwm.ChangeDutyCycle(100)
            G_pwm.ChangeDutyCycle(0)
            B_pwm.ChangeDutyCycle(0)
        sleep(1)
   
except Exception as e:
    print(e)
    
finally:
    GPIO.cleanup()
sys.exit( ); 

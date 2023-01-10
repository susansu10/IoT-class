import time, requests, random
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)
p = GPIO.PWM(12, 50)

from gpiozero import LED, DistanceSensor
from time import sleep
sensor = DistanceSensor(echo=27, trigger=17)
sensor2 = DistanceSensor(echo=6, trigger=5)

import threading, sys    #
import json

R_pin = 33
G_pin = 35
B_pin = 37
R_pin2 = 36
G_pin2 = 40
B_pin2 = 38

GPIO.setup(R_pin, GPIO.OUT)
GPIO.setup(G_pin, GPIO.OUT)
GPIO.setup(B_pin, GPIO.OUT)
GPIO.setup(R_pin2, GPIO.OUT)
GPIO.setup(G_pin2, GPIO.OUT)
GPIO.setup(B_pin2, GPIO.OUT)

R_pwm = GPIO.PWM(R_pin, 800)
G_pwm = GPIO.PWM(G_pin, 800)
B_pwm = GPIO.PWM(B_pin, 800)
R_pwm2 = GPIO.PWM(R_pin2, 800)
G_pwm2 = GPIO.PWM(G_pin2, 800)
B_pwm2 = GPIO.PWM(B_pin2, 800)
# use python RPi.GPIO, square wave is 70k Hz
# use python wiringpi2 or bindings, square wave is 28k Hz
# use C wiringPi, square wave is 4.1-4.6M Hz

R_pwm.start(0)
G_pwm.start(0)
B_pwm.start(0)
R_pwm2.start(0)
G_pwm2.start(0)
B_pwm2.start(0)

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
            print("降雨機率 > 10")
            print("Buzzer yes")
            GPIO.setmode(GPIO.BOARD)
            p.start(50)
            p.ChangeFrequency(659)
            time.sleep(1)
            p.stop()
        else:
            print("降雨機率 <= 10")
            print("Buzzer no")
    else:
        print("Can't get data!")

try:
    while(1):
        dis = sensor.distance * 100
        print("----rain_weather----")
        print('{0:.1f}cm'.format(dis))
        if dis < 10:
            print("People Come, distance < 10")
            R_pwm.ChangeDutyCycle(0)
            G_pwm.ChangeDutyCycle(100)
            B_pwm.ChangeDutyCycle(100)
            get_data()
        else:
            print("No People, distance >= 10")
            R_pwm.ChangeDutyCycle(100)
            G_pwm.ChangeDutyCycle(0)
            B_pwm.ChangeDutyCycle(0)
        sleep(1)
        dis2 = sensor2.distance * 100
        print("----water----")
        print('{0:.1f}cm'.format(dis2))
        if dis2 < 5.2:
            print("water : high")
            R_pwm2.ChangeDutyCycle(0)
            G_pwm2.ChangeDutyCycle(100)
            B_pwm2.ChangeDutyCycle(100)
        else:
            print("water : low")
            R_pwm2.ChangeDutyCycle(100)
            G_pwm2.ChangeDutyCycle(0)
            B_pwm2.ChangeDutyCycle(100)
        sleep(1)
   
except Exception as e:
    print(e)
    
finally:
    GPIO.cleanup()
sys.exit( ); 

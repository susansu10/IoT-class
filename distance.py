from gpiozero import LED, DistanceSensor
from time import sleep

sensor = DistanceSensor(echo=27, trigger=17)

try:
    while True:
        dis = sensor.distance * 100
        print('{0:.1f}cm'.format(dis))
        if dis < 10:
            print("distance < 10")
        else:
            print("distance > 10")
        sleep(1)
except KeyboardInterrupt:
    pass

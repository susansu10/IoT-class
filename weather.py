#  need DAN.py  and csmapi.py
import time, requests, random 
import threading, sys    #
import json

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

        location = data["records"]["location"][0]["locationName"]

        weather_elements = data["records"]["location"][0]["weatherElement"]
        start_time = weather_elements[0]["time"][0]["startTime"]
        end_time = weather_elements[0]["time"][0]["endTime"]
        rain_prob = weather_elements[1]["time"][0]["parameter"]["parameterName"]
        min_tem = weather_elements[2]["time"][0]["parameter"]["parameterName"]
        max_tem = weather_elements[4]["time"][0]["parameter"]["parameterName"]

        print(location)
        print(start_time)
        print(end_time)
        print("降雨機率 = ", rain_prob, "%")
        print("最低溫 = ", min_tem)
        print("最高溫 = ", max_tem)

    else:
        print("Can't get data!")

get_data()
sys.exit( ); 
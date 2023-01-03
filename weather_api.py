import http.server
import socketserver
from urllib.parse import urlparse
from urllib.parse import parse_qs
import json
from datetime import datetime
import os

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Sending an '200 OK' response
        self.send_response(200)

        # Setting the header
        self.send_header("Content-type", "text/html")

        # Whenever using 'send_header', you also have to call 'end_headers'
        self.end_headers()

        # Extract query param
        tempf = 'World'
        query_components = parse_qs(urlparse(self.path).query)
		
		#break out the data from the GET into individual variables. you might not have temp1f or temp2f if you don't have extra sensors.
        if 'tempf' in query_components:
            tempf = query_components["tempf"][0]
            humidity = query_components["humidity"][0]
            baromrelin = query_components["baromrelin"][0]
            dailyrainin = query_components["dailyrainin"][0]
            solarradiation = query_components["solarradiation"][0]
            windspeed = query_components["windspeedmph"][0]
            dateutc = query_components["dateutc"][0]
            tempinf = query_components["tempinf"][0]
            humidityin = query_components["humidityin"][0]
            humidity2 = query_components["humidity2"][0]
            baromabsin = query_components["baromabsin"][0]
            winddir = query_components["winddir"][0]
            windgustmph = query_components["windgustmph"][0]
            maxdailygust = query_components["maxdailygust"][0]
            hourlyrainin = query_components["hourlyrainin"][0]
            eventrainin = query_components["eventrainin"][0]
            weeklyrainin = query_components["weeklyrainin"][0]
            monthlyrainin = query_components["monthlyrainin"][0]
            totalrainin = query_components["totalrainin"][0]
            uv = query_components["uv"][0]
            temp1f = query_components["temp1f"][0]
            temp2f = query_components["temp2f"][0]
            batt1 = query_components["batt1"][0]
            batt2 = query_components["batt2"][0]
            batt_co2 = query_components["batt_co2"][0]
            battout = query_components["battout"][0]

        #your access token. usually set by $ export INFLUX_TOKEN=<your db token>
        token = os.getenv("INFLUX_TOKEN")
        org = "home"
        bucket = "weatherstation"
        json_payload = []
		#create a payload from the variables we set above, I'm sure there is an easier way to do this...
        data = {
            "measurement": "weather",
            "tags": {
                     "station": "Station_1" 
                    },
            "time": dateutc,
            "fields": {
                       'tempf': float(tempf),
                       'humidity': float(humidity),
                       'baromrelin': float(baromrelin),
                       'dailyrainin': float(dailyrainin),
                       'solarradiation': float(solarradiation),
                       'windspeed': float(windspeed),
                       'tempinf': float(tempinf),
                       'humidityin': float(humidityin),
                       'humidity2' : float(humidity2),
                       'baromabsin': float(baromabsin),
                       'winddir': float(winddir),
                       'windgustmph': float(windgustmph),
                       'maxdailygust': float(maxdailygust),
                       'hourlyrainin': float(hourlyrainin),
                       'eventrainin': float(eventrainin),
                       'weeklyrainin': float(weeklyrainin),
                       'monthlyrainin': float(monthlyrainin),
                       'totalrainin': float(totalrainin),
                       'uv': float(uv),
                       'temp1f': float(temp1f),
                       'temp2f': float(temp2f),
                       'batt1': float(batt1),
                       'batt2': float(batt2),
                       'batt_co2': float(batt_co2),
                       'battout': float(battout),
                       }
                }
        json_payload.append(data)

        with InfluxDBClient(url="<IP of DB server or URL>:8086", token=token, org=org) as client:
             write_api = client.write_api(write_options=SYNCHRONOUS)
             write_api.write(bucket, org, json_payload)
        client.close()

		#write select data to a text file for FFMPEG to use when it writes to the webcam image
        path = '/weather/weather.txt'
        weather = open(path,'w')
        data = "Temp:"+tempf+"\°F. Humidity:"+humidity+"\%. Pressure:"+baromrelin+" inHg. Daily Rain:"+dailyrainin+" in.\nSolar Radation:"+solarradiation+" W/m² Wind Speed:"+windspeed+" mph"
        weather.write(data)
        print(data)
        weather.close()

        # Writing the HTML contents with UTF-8
        #self.wfile.write(bytes(html, "utf8"))

        return

# Create an object of the above class
handler_object = MyHttpRequestHandler

PORT = 8088
my_server = socketserver.TCPServer(("", PORT), handler_object)

# Star the server
my_server.serve_forever()

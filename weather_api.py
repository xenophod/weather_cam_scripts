import http.server
import socketserver
from urllib.parse import urlparse
from urllib.parse import parse_qs

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
        if 'tempf' in query_components:
            tempf = query_components["tempf"][0]
            humidity = query_components["humidity"][0]
            baromrelin = query_components["baromrelin"][0]
            dailyrainin = query_components["dailyrainin"][0]
            solarradiation = query_components["solarradiation"][0]
            windspeed = query_components["windspeedmph"][0]

        path = '/home/xenophod/weather.txt'
        weather = open(path,'w')
        data = "Temp:"+tempf+"\‹F. Humidity:"+humidity+"\%. Pressure:"+baromrelin+" inHg. Daily Rain:"+dailyrainin+" in.\nSolar Radation:"+solarradiation+" W/m2 Wind Speed:"+windspeed+" mph"
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

# Start the server
my_server.serve_forever()
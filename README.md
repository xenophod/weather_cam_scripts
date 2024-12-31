# weather_cam_scripts
###### Collection of scripts used to add WS-2902C weather station data as overlays to webcam images
![Example image](https://xenophod.org/image.jpg)

### Description
These are some scripts and configurations I've used to create a "weather cam" using Linux/ffmpeg and an Ambient Weather WS-2902C weather station. Using ffmpeg on Linux, I capture an image, and then overlay select weather data over the image and upload to the Ambient Weather site as well as other servers. 

I have two scripts that make up the weather cam system:
* weather_api.py
* webcam.sh

A third, optional script makes a timelapse movie and uploads to youtube (however the youtube part apparently is against the TOS, they get locked after a few uploads):
* weathercam_timelapse.sh

### weather_api.py
This script starts a web server that listens on the port 8088, gets the json data feed from the WS-2902C base station and writes a text file called "weather.txt" every 16 seconds for use in the image overlay.

### webcam.sh
This script grabs an image either from a webcam or a streaming video feed, takes the weather.txt data and writes it over the image and then uploads it to one or more servers.

### Configure the base station
Follow the directions to get attached to your wifi network using the awnet app. You used to need an iOS device to configure the last page, the Android was updated to allow access to the last page. The screenshot below shows how I have it configured. All of this can be changed for your needs, just edit the config to refelct your server's IP and the scripts to reflect the port you want to use.

![AWNET config](https://xenophod.org/awnet.png)

Once you have the base station sending data to your server, start the python script and wait for data to come in.

```
~$ python3 weather_api.py
192.168.1.238 - - [16/Jan/2022 14:38:28] "GET /data/report/?stationtype=AMBWeatherV4.3.2&PASSKEY=xxxx&dateutc=2022-01-16+19:38:27&tempinf=67.1&humidityin=22&baromrelin=29.684&baromabsin=29.752&tempf=21.2&battout=1&humidity=93&winddir=263&windspeedmph=1.3&windgustmph=3.4&maxdailygust=9.2&hourlyrainin=0.000&eventrainin=0.000&dailyrainin=0.000&weeklyrainin=0.000&monthlyrainin=3.441&totalrainin=23.720&solarradiation=13.33&uv=0&temp2f=68.4&humidity2=26&batt2=1&batt_co2=1 HTTP/1.1" 200 -
Temp:21.2\‹F. Humidity:93\%. Pressure:29.684 inHg. Daily Rain:0.000 in.
Solar Radation:13.33 W/m2 Wind Speed:1.3 mph
192.168.1.238 - - [16/Jan/2022 14:38:44] "GET /data/report/?stationtype=AMBWeatherV4.3.2&PASSKEY=xxxxx&dateutc=2022-01-16+19:38:43&tempinf=67.3&humidityin=22&baromrelin=29.684&baromabsin=29.752&tempf=21.2&battout=1&humidity=93&winddir=272&windspeedmph=3.1&windgustmph=4.5&maxdailygust=9.2&hourlyrainin=0.000&eventrainin=0.000&dailyrainin=0.000&weeklyrainin=0.000&monthlyrainin=3.441&totalrainin=23.720&solarradiation=12.97&uv=0&temp2f=68.4&humidity2=26&batt2=1&batt_co2=1 HTTP/1.1" 200 -
Temp:21.2\‹F. Humidity:93\%. Pressure:29.684 inHg. Daily Rain:0.000 in.
Solar Radation:12.97 W/m2 Wind Speed:3.1 mph
```

If you have "screen" installed, I'd start a screen session, then start the script and detach the session. like
```
#Start a session called "weather"
$ screen -S weather
#run the script
$ python3 weather_api.py
#detach from the session
$ CTRL a CTRL d
#check the sessions is running
$screen -ls
There is a screen on:
        7891.weather    (01/16/22 14:38:14)     (Detached)
1 Socket in /run/screen/S-xenophod.
```

Now when you run the webcam.sh script (after editing it for paths and overlay images and stuff) it should capture an image and add the weather.txt info over the captured image.

I've added the webcam script to my crontab and it runs every minute. 1 minute also happens to be the smallest interval for uploading to the Ambient Weather FTP site.

add the script to your crontab (replace /home/xenophod with your own path to the script) by typing crontab -e
```
* * * * * /home/xenophod/webcam.sh
```

This image gets over written with a new image every 60 seconds: https://xenophod.org/image.jpg

### weathercam_timelapse.sh
The timelapse script will take a collection of timestamped images and create an mp4 video. I have this running on my NAS/Plex server since it has a ton of space and the AtomicPi that captures the video has little space left. Here's an example of a timelapse video: https://youtu.be/2EbXHAB-k44


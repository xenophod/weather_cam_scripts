#!/bin/bash

### This script evolved from capturing a images from a webcam to capturing a security camera's network feed.
### I've left the older commands commented out in case I need to revert back at some point

### Use fswebcam to capture the inital image from a USB webcam.
###/usr/bin/fswebcam --no-banner -r 1280x720 --delay 3 --skip 100 --jpeg 99 /home/xenophod/start.jpg

### Use ffmpeg to capture inital image from a USB webcam.
###/usr/bin/yes | /usr/bin/ffmpeg -ss 3 -f v4l2 -input_format mjpeg -video_size 1280x720 -i /dev/video0 -vframes 7 /home/xenophod/start.jpg

### Use ffmpeg to capture inital image from a video feed streaming over rtsp. Specifically the Amcrest IP8M-2496EW-V2.
/usr/bin/ffmpeg -y -i 'rtsp://admin:defaultpassword@192.168.2.145:554/cam/realmonitor?channel=1&subtype=0' -frames:v 3 -r 1 /home/xenophod/start.jpg


### Use ffmpeg to modify the inital image and add the weather data text as an overlay and a semitransparent black background for better visability.
/usr/bin/yes | /usr/bin/ffmpeg -i /home/xenophod/start.jpg -vf drawtext="fontfile=/usr/share/fonts/truetype/freefont/FreeSerif.ttf: textfile=/home/xenophod/weather.txt: x=0: y=0: fontsize=38: fontcolor=white@0.6: box=1: boxcolor=black@0.4" /home/xenophod/output1.jpg

### Use ffmpeg to add the "spotsy.png" overlay to the bottom right corner of the image with the weather data overlay.
/usr/bin/yes | /usr/bin/ffmpeg -i /home/xenophod/output1.jpg -i /home/xenophod/spotsy.png -filter_complex "[1]lut=a=val*0.5[a];[0][a]overlay=949:520" /home/xenophod/output.jpg

### Use ffmpeg to create the last overlay with the location information and the time/date, also with a semitransparent black background for better visability.
/bin/echo "Spotsylvania, VA  " $(/bin/date -R) > /home/xenophod/timedate.txt; /usr/bin/yes | /usr/bin/ffmpeg -i /home/xenophod/output.jpg -vf drawtext="fontfile=/usr/share/fonts/truetype/freefont/FreeSerif.ttf: textfile=/home/xenophod/timedate.txt: x=0: y=681: fontsize=38: fontcolor=white@0.6: box=1: boxcolor=black@0.4" /home/xenophod/image.jpg

### FTP/Upload the final image to your ambientweather account. Make sure you edit ID:CODE with your personalized data when you added a web cam to your account.
/usr/bin/curl --user ID:CODE --upload-file /home/xenophod/image.jpg ftp://ftp.ambientweather.net/

### Secure Copy (scp) the final image to your personal linux website using an ssh key for authentication.
/usr/bin/scp -i /home/xenophod/server.key /home/remote-server/image.jpg remote-userID@remote-server-IP-or-name:/var/www/website/html/path-to-images/uploads/.

### Secure Copy (scp) the initial and final images to another linux server on the local network.
### My AtomicPi doesn't have a lot of space, so I copy the images to my NAS in order to make timelapse videos of the day's weather.
/usr/bin/scp -i /home/xenophod/.ssh/id_rsa /home/xenophod/image.jpg xenophod@192.168.1.9:/home/xenophod/timelapse/image.`date +%Y-%m-%d-%T`.jpg
/usr/bin/scp -i /home/xenophod/.ssh/id_rsa /home/xenophod/start.jpg xenophod@192.168.1.9:/home/xenophod/timelapse/start.`date +%Y-%m-%d-%T`.jpg
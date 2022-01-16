#/bin/bash

ffmpeg -r 20 -pattern_type glob -i "/home/xenophod/timelapse/image.`date --date="yesterday" +%Y-%m-%d`-*.jpg" -s:v 1280x720 -c:v libx264 -crf 17 -pix_fmt yuv420p /srv/plex_media/learning/timelapse/weathercam_data.`date --date="yesterday" +%Y-%m-%d`.mp4

ffmpeg -r 20 -pattern_type glob -i "/home/xenophod/timelapse/start.`date --date="yesterday" +%Y-%m-%d`-*.jpg" -s:v 1280x720 -c:v libx264 -crf 17 -pix_fmt yuv420p /srv/plex_media/learning/timelapse/weathercam.`date --date="yesterday" +%Y-%m-%d`.mp4

DaySuffix() {
  case `date --date=yesterday +%-d` in
    1|21|31) echo "st";;
    2|22)    echo "nd";;
    3|23)    echo "rd";;
    *)       echo "th";;
  esac
}
date --date=yesterday "+%B %-d`DaySuffix`, %Y" > /home/xenophod/date.txt


#/usr/local/bin/youtube-upload --title="`cat date.txt`" --description="This video was automatically generated using fswebcam, ffmpeg and Python on Linux.   To see the current weather conditions visit my website at: https://xenophod.org/image.jpg    Auto uploaded to YouTube using https://github.com/tokland/youtube-upload" --tags="ffmpeg,linux,weather station,WS-2902C,python,time lapse,spotsylvania,virginia,AtomicPi" --category="Science & Technology" --default-language="en" --default-audio-language="en" --playlist="Weather Cam Time Lapse" /srv/plex_media/learning/timelapse/weathercam_data.`date --date="yesterday" +%Y-%m-%d`.mp4

#/usr/local/bin/youtube-upload --title="`cat /home/xenophod/date.txt`" --description="This video was automatically generated using fswebcam, ffmpeg and Python on Linux. To see the current weather conditions visit my website at: https://xenophod.org/image.jpg  Auto uploaded to YouTube using https://github.com/tokland/youtube-upload" --tags="fswebcan,ffmpeg,linux,weather station,WS-2902C,python,time lapse,spotsylvania,virginia,AtomicPi,ubuntu,youtube-upload" /srv/plex_media/learning/timelapse/weathercam_data.`date --date="yesterday" +%Y-%m-%d`.mp4

#rm -rf /home/xenophod/timelapse/*.`date --date="yesterday" +%Y-%m-%d`-*.jpg
#!/bin/bash
cd /opt/parking_spaces/parks_data
timestamp="`date +%s%3N`"
filename="${timestamp}.json"
weather_filename="${timestamp}_weather.json"
echo ${timestamp}
curl --user-agent "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.1" "https://www.gov.je/_layouts/15/C5.Gov.Je.CarParks/proxy.aspx?_=${timestamp}" > ${filename}
source /opt/parking_spaces/.venv/bin/activate
python get_current_weather.py > ${weather_filename}
python file_uploader.py -f ${filename}
if [ $? -eq 0 ]; then
        echo 'Upload succeeded'
        rm ${filename}
else
        echo 'Upload failed'
fi
python file_uploader.py -w -f ${weather_filename}
if [ $? -eq 0 ]; then
        echo 'Upload weahter succeeded'
        rm ${filename}
else
        echo 'Upload weather failed'
fi

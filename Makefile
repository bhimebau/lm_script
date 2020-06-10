all: 

settime: settime.py lm.py
	./settime.py -p /dev/ttyACM0

gettime: gettime.py lm.py
	./gettime.py -p /dev/ttyACM0

cal: cal.py lm.py
	./cal.py -p /dev/ttyACM0 -l /dev/ttyACM1

verify_cal: verify_cal.py lm.py 
	./verify_cal.py -p /dev/ttyACM0 -o vcal.csv

read_cal: read_cal.py lm.py
	./read_cal.py -p /dev/ttyACM0 

get_uid: get_uid.py lm.py
	./get_uid.py -p /dev/ttyACM0

led_cal: sqm.py lm.py led_source_cal.py
	./led_source_cal.py -p /dev/ttyACM0 -q /dev/ttyUSB0 -o led_data_3.csv

c2i: ledcal2include.py
	./ledcal2include.py -i ./led_cal_data/led_data_3.csv -o ./led_cal_data/skydata

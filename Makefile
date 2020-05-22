\all: 

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

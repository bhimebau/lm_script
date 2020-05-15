all: 

settime: settime.py lm.py
	./settime.py -p /dev/ttyACM0

gettime: gettime.py lm.py
	./gettime.py -p /dev/ttyACM0





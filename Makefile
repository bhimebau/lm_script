SENSOR_PORT = /dev/ttyUSB0
LIGHT_SOURCE_PORT = /dev/ttyUSB1
SQM_PORT = /dev/ttyACM1 

CALIBRATION_FILE = sensors/201b.csv
CAL_TEMP = 21
PPM = 300

all: 

settime: settime.py lm.py
	./settime.py -p ${SENSOR_PORT}

gettime: gettime.py lm.py
	./gettime.py -p ${SENSOR_PORT}

cal: cal.py lm.py
	./cal.py -p ${SENSOR_PORT} -l ${LIGHT_SOURCE_PORT}

check: cal.py lm.py
	./check.py -p ${SENSOR_PORT} -l ${LIGHT_SOURCE_PORT} -n 201b

verify_cal: verify_cal.py lm.py 
	./verify_cal.py -p ${SENSOR_PORT} -o vcal.csv

read_cal: read_cal.py lm.py
	./read_cal.py -p ${SENSOR_PORT} -n 201c

get_uid: get_uid.py lm.py
	./get_uid.py -p ${SENSOR_PORT}

get_data: get_data.py lm.py
	./get_data.py -p ${SENSOR_PORT} -o ./data_pulls

led_cal: sqm.py lm.py led_source_cal.py
	./led_source_cal.py -p ${LIGHT_SOURCE_PORT} -q ${SQM_PORT} -o led_data_3.csv

led_table: sqm.py lm.py led_table.py
	./led_table.py -p ${SENSOR_PORT} -q ${LIGHT_SOURCE_PORT} -o led_table_out_1.csv

write_cal: write_cal.py lm.py
	./write_cal.py -p ${SENSOR_PORT} -c ${CALIBRATION_FILE} -t ${CAL_TEMP} -m ${PPM}

deploy: settime.py write_cal.py lm.py
	./settime.py -p ${SENSOR_PORT}
	./write_cal.py -p ${SENSOR_PORT} -c ${CALIBRATION_FILE} -t ${CAL_TEMP} -m ${PPM}
	./temp_offset.py -p ${SENSOR_PORT} -l ${LIGHT_SOURCE_PORT}
	./data_erase.py -p ${SENSOR_PORT} 


c2i: ledcal2include.py
	./ledcal2include.py -i ./led_cal_data/led_data_3.csv -o ./led_cal_data/skydata
	cp ./led_cal_data/skydata.c ../lm_application/Src
	cp ./led_cal_data/skydata.h ../lm_application/Inc

parse_data: parse_data.py
	./parse_data.py -s 12/31/2020 -e 1/6/2021 -l "003,004,005" -d "./data_pulls" -o outfile.csv

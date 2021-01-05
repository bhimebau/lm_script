#!/usr/bin/env python3

""" Lightmon Calibration Program

This program will calibrate the sensor using a light tube. 

It assumes that there is a light source on one end of the tube. 
This sensor will be accessible through the serial port. 

Similarly the sensor will be connected to the other end of the tube. 
This sensor will also be accessible through the serial port. 

"""
import lm
import argparse
import time
import numpy as np
from twilio.rest import Client

if __name__ == "__main__":
    account_sid = 'AC073919b600761868be304dbce85d1d8b'
    auth_token='1ad3627e21bccd97b6638428b9527b39'
    
    client = Client(account_sid, auth_token)
   
    parser = argparse.ArgumentParser(description='Set LightMon time and date')
    parser.add_argument('-p',
                        dest='port',
                        help='Serial port device where sensor is connected, example: /dev/ttyACM0',
                        required=True)
    parser.add_argument('-l',
                        dest='led',
                        help='Serial port device where light source is connected: /dev/ttyACM1',
                        required=True)

    
    args = parser.parse_args()
    print("Initializing the Sensor")
    sensor = lm.LightMon(args.port)
    print("Initializing the Light Source")
    light = lm.LightMon(args.led)

    print("Erasing the Flash")
    sensor.cal_erase()                        # Erase the flash page for cal to -1  
    print("Loading the initial values from flash to SRAM")
    sensor.cal_load()                         # Load -1 from the flash to SRAM
    print("Taking the calibration temperature")
    temperature = int(sensor.cal_temperature())
    print("Writing temperature and sensor ppm values to sensor cal")
    sensor.cal_write_temp_comp(temperature,400)
    
#    array = np.arange(15.3,26.1,.1)          # Create an array of possible light values
    array = np.arange(15.3,24.1,.1)           # Create an array of possible light values
    for sky in array:                         # Step through each value
        value = np.around(sky,1)
        light.sky_write(value)
        sensor_data = int(sensor.tsl237_read_raw())
        sensor.cal_write(value,sensor_data)
    sensor.cal_store()
    sensor.close_port()
    light.close_port()
    message = client.messages \
                    .create(
                        body="Done with Calibration",
                        from_='12562697917',
                        to='+18123256673'
                    )
    
    

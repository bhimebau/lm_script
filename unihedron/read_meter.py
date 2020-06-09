#!/usr/bin/env python

""" Utility to read the unihedron meter

"""
import lm
import argparse
import time
import numpy as np

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Read SQM LU Meter')
    parser.add_argument('-p',
                        dest='port',
                        help='Serial port device where sensor is connected, example: /dev/ttyUSB0',
                        required=True)
    
    args = parser.parse_args()
    print "Connecting to the Sensor"
    sensor = lm.LightMon(args.port)
    print "Initializing the Light Source"
    light = lm.LightMon(args.led)

    print "Erasing the Flash"
    sensor.cal_erase()                        # Erase the flash page for cal to -1  
    print "Loading the initial values from flash to SRAM"
    sensor.cal_load()                         # Load -1 from the flash to SRAM 
    array = np.arange(19.4,24.2,.1)           # Create an array of possible light values
    for sky in array:                         # Step through each value
        value = np.around(sky,1)
        light.sky_write(value)
        sensor_data = int(sensor.tsl237_read_raw())
        sensor.cal_write(value,sensor_data)
    sensor.cal_store()
    sensor.close_port()
    light.close_port()

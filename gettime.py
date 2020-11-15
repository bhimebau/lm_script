#!/usr/bin/env python3

""" Lightmon Time/Date Reporting Program

This program reports the current date/time on the sensor 

"""
import lm
import argparse
import time

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Set LightMon time and date')
    parser.add_argument('-p',
                        dest='port',
                        help='Serial port device where sensor is connected, example: /dev/ttyACM0',
                        required=True)
    args = parser.parse_args()
    sensor = lm.LightMon(args.port)
    print("Sensor's Current Date/Time:",sensor.gettime())
    print("Time Delta (Sensor Time-System Time):",sensor.difftime(),"seconds")
    
    sensor.close_port()    

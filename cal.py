#!/usr/bin/env python

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

if __name__ == "__main__":

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
    sensor = lm.LightMon(args.port)
    light = lm.LightMon(args.led)

    instr

    
    light.sky_write(20.2)
    print "Sensor's Current Date/Time:",sensor.gettime()
    print "Error (Sensor Time-System Time):",sensor.difftime(),"seconds"
    
    sensor.close_port()
    light.close_port()

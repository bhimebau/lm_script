#!/usr/bin/env python

""" Lightmon Time/Date Setting Program

Sets the light sensors time and date to be the same as the system 

"""
import lm
import argparse
                 
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Set LightMon time and date')
    parser.add_argument('-p',
                        dest='port',
                        help='Serial port device where sensor is connected, example: /dev/ttyACM0',
                        required=True)
    args = parser.parse_args()
    sensor = lm.LightMon(args.port)
    print "Sensor's Old Date/Time:",sensor.gettime()
    sensor.settime()
    print "Sensor's New Date/Time:",sensor.gettime()
    sensor.close_port()    

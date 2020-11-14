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
import numpy as np
from twilio.rest import Client

if __name__ == "__main__":

    account_sid = 'AC073919b600761868be304dbce85d1d8b'
    auth_token='56fa4d513f8a3d09d8466c11eac6b999'
    
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

    parser.add_argument('-n',
                        dest='num',
                        help='Serial number of the sensor',
                        required=True)
        
    args = parser.parse_args()
    print "Initializing the Sensor"
    sensor = lm.LightMon(args.port)
    print "Initializing the Light Source"
    light = lm.LightMon(args.led)

    outfile = open("./sensors/%s_check.csv"%(args.num),"w+")
#    outfile = open("%s_check.csv"%(sensor.get_uid().rstrip()),"w+")

#    outfile = open(args.output,"w+")
    
    array = np.arange(15.4,23.3,.1)           # Create an array of possible light values
    for sky in array:                         # Step through each value
        value = np.around(sky,1)
        light.sky_write(value)
        sensor_data = float(sensor.tsl237_read_mag())
        outstr =  "%2.1f,%2.2f,%f\n"%(value,sensor_data,value-sensor_data)
        outfile.write(outstr)
        print outstr,
    outfile.close()
    sensor.close_port()
    light.close_port()
    message = client.messages \
                    .create(
                        body="Done with Check",
                        from_='12562697917',
                        to='+18123256673'
                    )

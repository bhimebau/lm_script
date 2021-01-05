#!/usr/bin/env python3

""" Calibration Writing Program 

This program sweeps light sensor values through the calibration to confirm the performance
of the calibration. 

"""
import lm
import argparse
import time
import numpy

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Programs the calibration into the sensor')
    parser.add_argument('-p',
                        dest='port',
                        help='Serial port device where sensor is connected, example: /dev/ttyACM0',
                        required=True)

    parser.add_argument('-c',
                        dest='cal',
                        help='Master Calibration File: this stores data is the base calibration for all sensors.',
                        required=True)

    parser.add_argument('-t',
                        dest='temperature',
                        help='Temperature in C used to create the cal',
                        required=True)

    parser.add_argument('-m',
                        dest='ppm',
                        help='Accuracy of the sensor',
                        required=True)

        
    args = parser.parse_args()
    sensor = lm.LightMon(args.port)

    sensor.cal_write_temp_comp(int(args.temperature),int(args.ppm))
    calfile = open(args.cal,"r")
    lines = calfile.readlines()
    for line in lines:
        elements = line.strip().split(',')
        sky = float(elements[0])
        counts = int(elements[1])
        if (counts != -1):
            sensor.cal_write(sky,counts)
            print("%2.1f %d"%(sky,counts))
    sensor.cal_store()
    calfile.close()
    sensor.close_port()

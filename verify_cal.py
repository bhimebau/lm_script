#!/usr/bin/env python3

""" Lightmon Calibration Program

This program sweeps light sensor values through the calibration to confirm the performance
of the calibration. 

"""
import lm
import argparse
import time
import numpy

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Verify the calibration table')
    parser.add_argument('-p',
                        dest='port',
                        help='Serial port device where sensor is connected, example: /dev/ttyACM0',
                        required=True)

    parser.add_argument('-o',
                        dest='output',
                        help='file to store the csv data',
                        required=True)
        
    args = parser.parse_args()
    sensor = lm.LightMon(args.port)
    outfile = open(args.output,"w+")

    for value in range(400000,50000000,100000):
        datastr =  "%s,%d"%(sensor.cal_lookup(value).rstrip(),value)
        outfile.write("%s\n"%(datastr))
        print(datastr)
    outfile.close()
    sensor.close_port()

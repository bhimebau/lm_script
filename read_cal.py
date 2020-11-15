#!/usr/bin/env python3

""" Lightmon Read Calibration Table

Reads the calibration table and writes it to a csv file named uid_cal.csv. 


"""
import lm
import argparse
import time
import numpy

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Read and Store Calibration Table')
    parser.add_argument('-p',
                        dest='port',
                        help='Serial port device where sensor is connected, example: /dev/ttyACM0',
                        required=True)

    parser.add_argument('-n',
                        dest='num',
                        help='ID number of the sensor',
                        required=True)
    
    args = parser.parse_args()
    sensor = lm.LightMon(args.port)
    outfile = open("./sensors/%s.csv"%(args.num),"w+")
    datastr = sensor.cal_read()
#    print(datastr)
    outfile.write(datastr)
 
#
#    for value in range(400000,50000000,100000):
#        datastr =  "%s,%d"%(sensor.cal_lookup(value).rstrip(),value)
#        outfile.write("%s\n"%(datastr))
#        print(datastr)
    outfile.close()
    sensor.close_port()

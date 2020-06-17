#!/usr/bin/env python

""" Enables the Calibration of the LED Light Source

"""
import lm
import argparse
import time
import numpy as np
import sqm

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Set LightMon time and date')
    parser.add_argument('-p',
                        dest='led_port',
                        help='Serial port device where precision led source is connected: /devttyACM0',
                        required=True)
    parser.add_argument('-q',
                        dest='sqm_port',
                        help='Serial port device where the SQM LU is connected: /dev/ttyUSB0',
                        required=True)

    parser.add_argument('-o',
                        dest='ofile',
                        help='file to write the collected data',
                        required=True)

    
    args = parser.parse_args()
    print "Initializing the Sensor"
    led = lm.LightMon(args.led_port)
    print "Initializing the Light Source"
    sqm = sqm.SQM_LU(args.sqm_port)
    print "Opening Output File"
    outfile = open(args.ofile,"w+")
    sky = np.arange(15.3,26.0+.1,.1)
    outfile.write("LS,SQM")
    for value in sky:
        led.dac_write_table(value)
        sqm.read_raw()
        outstr = "%2.1f,%2.2f"%(value,sqm.mpsas)
        print outstr
        outfile.write(outstr)
    outfile.close()
    led.close_port()
    sqm.close_port()

#!/usr/bin/env python3

""" Enables the Calibration of the LED Light Source

"""
import lm
import argparse
import time
import numpy as np
import sqm

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Calibrate the LED precision light source')
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
    print("Initializing precision LED source ...")
    led = lm.LightMon(args.led_port)
    print("Initializing the SQM ...")
    sqm = sqm.SQM_LU(args.sqm_port)
    print(f"Opening Output File: {args.ofile}")
    outfile = open(args.ofile,"w+")
    rawfile = open("raw_"+args.ofile,"w+")
    for dac in range(200,4100,100):
        values=[]
        raw=[]
        for rg in range(0,4,1):
            led.dac_write_raw(dac,rg)
            sqm.read_raw()
            values.append(sqm.mpsas)
            raw.append(sqm.count)
            raw.append(sqm.period)
            outstr = "%d,%d,%2.2f,%d,%f"%(rg,dac,sqm.mpsas,sqm.count,sqm.period)
            print(outstr)
        file_str = "%d,%2.2f,%2.2f,%2.2f,%2.2f\n"%(dac,
                                                   values[0],
                                                   values[1],
                                                   values[2],
                                                   values[3])
        raw_str = "%d,%d,%d,%d,%d,%2.2f,%2.2f,%2.2f,%2.2f\n"%(dac,
                                                              raw[0],
                                                              raw[2],
                                                              raw[4],
                                                              raw[6],
                                                              raw[1],
                                                              raw[3],
                                                              raw[5],
                                                              raw[7])
        outfile.write(file_str)
        rawfile.write(raw_str)
    outfile.close()
    led.close_port()
    sqm.close_port()

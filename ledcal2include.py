#!/usr/bin/env python

""" Program to convert Led Source Cal into include file for LED source

This program assumes that the led_cal program has been run. This program causes the 
light sensor to sweep the dac values of the led source across all 4 of the possible resistance
ranges (316, 1k, 10k, 47.6k). The program then asks an SQM-LU meter to report the light 
being output by the source in mpsas. The values for each of these ranges is captured into a 
file that will be the input to this program. This data looks like the following: 

200,20.96,23.22,19.56,19.56
300,20.17,22.39,19.56,19.56
400,19.58,21.82,19.56,19.56
500,19.14,21.38,19.52,19.56
600,18.78,21.02,27.11,19.56

...

3700,15.36,17.40,21.96,25.57
3800,15.32,17.35,21.90,25.47
3900,15.27,17.31,21.86,25.38
4000,15.21,17.24,21.80,25.30

The columns are as follows: 

* DAC value (0-4096): This is directly proportional to LED current as this voltage controls
a current source. 
* 316 Ohm Values: This resistor controls the scale of the V-I converter. This resistor 
enables the largest currents which correspond to the brightest values
* 1k Ohm Values
* 10k Ohm Values
* 47.6K Ohm Values: This resistor provides the smallest currents and as such provides
the lowest light values. 

The program will take this input and transform it into a file that looks like the following: 

#define DARKEST_VALUE_ALLOWED 25
#define BRIGHTEST_VALUE_ALLOWED 15

/* The skydata data include is a 16 bit value that includes the following data: 

bits 0-11 12-bit value used to set the DAC
bits 12-15 4-bit value used to set the proper resistor to control the current range 

uint16_t skydata[(((int) DARKEST_VALUE_ALLOWED- (int) BRIGHTEST_VALUE_ALLOWED)*10)+1] = {
  1805, // 15.0
  1715, // 15.1
  1640, // 15.2
  1600, // 15.3

...

  450,  // 24.5
  440,  // 24.6
  430,  // 24.7
  420,  // 24.8
  410,  // 24.9
  400,  // 25.0
};

"""
import lm
import argparse
import time
import numpy as np

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Set LightMon time and date')
    parser.add_argument('-i',
                        dest='infile',
                        help='csv input file from led_cal program',
                        required=True)
    parser.add_argument('-o',
                        dest='outfile',
                        help='c file to create: example skydata.c',
                        required=True)

    
    args = parser.parse_args()
    infile_handle = open(args.infile,"r")
    outfile_handle = open(args.outfile,"w+")
    
    
    
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

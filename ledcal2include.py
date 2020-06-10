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
from scipy import interpolate

def minmax(array):
    minval = 5000
    maxval = 0
    for element in array:
        if (element == 19.56 or
            element == 19.54 or
            element == 19.52 or
            element == 19.50):
            pass
        else:
            if element < minval:
                minval = element
            if element > maxval:
                maxval = element
    return (minval,maxval)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Set LightMon time and date')
    parser.add_argument('-i',
                        dest='infile',
                        help='csv input file from led_cal program',
                        required=True)
    parser.add_argument('-o',
                        dest='outfile',
                        help='basename of c/h files to create: example skydata where skydata.c and skydata.h will be created',
                        required=True)

    
    args = parser.parse_args()
    infile_handle = open(args.infile,"r")
    c_outfile_handle = open(args.outfile+".c","w+")
    h_outfile_handle = open(args.outfile+".h","w+")
    line = infile_handle.readline()
    dac = []
    r_316 = []
    r_1000 = []
    r_10000 = []
    r_47600 = []
       
    while line:
#        print line,
        line_list = line.split(",")
        dac.append(float(line_list[0]))
        r_316.append(float(line_list[1]))
        r_1000.append(float(line_list[2]))
        r_10000.append(float(line_list[3]))
        r_47600.append(float(line_list[4]))
        line = infile_handle.readline()
    dac = np.array(dac)
    r_316 = np.array(r_316)
    r_1000 = np.array(r_1000)
    r_10000 = np.array(r_10000)
    r_47600 = np.array(r_47600)

    mins = []
    mins.append(minmax(r_316)[0])
    mins.append(minmax(r_1000)[0])
    mins.append(minmax(r_10000)[0])
    mins.append(minmax(r_47600)[0])
    mins = np.array(mins)
    lowest_val = round(minmax(mins)[0]+.1,1)
    if lowest_val < 15:
        lowest_val = 15
    # print lowest_val 

    maxs = []
    maxs.append(minmax(r_316)[1])
    maxs.append(minmax(r_1000)[1])
    maxs.append(minmax(r_10000)[1])
    maxs.append(minmax(r_47600)[1])
    maxs = np.array(maxs)
    highest_val = round(minmax(maxs)[1]-.1,1)
    if highest_val > 26:
        highest_val = 26
   #  print highest_val 
    
    steps = np.arange(lowest_val,highest_val+.1,.1)
    steps = steps[::-1]

    f_316 = interpolate.interp1d(r_316, dac)
    f_1000 = interpolate.interp1d(r_1000, dac)
    f_10000 = interpolate.interp1d(r_10000, dac)
    f_47600 = interpolate.interp1d(r_47600, dac)

    out_array = []
    range_res = 3
    for step in steps:
        if step < mins[range_res]:
            range_res = range_res - 1
            if range_res < 0:
                range_res = 0
        if range_res == 3:
            yval = f_47600(step)
        elif range_res == 2:
            yval = f_10000(step)
        elif range_res == 1:
            yval = f_1000(step)
        else:
            yval = f_316(step)
        out_array.append([round(step,1), int(yval), range_res, "0x%04x"%(yval+(4096*range_res))])

    # Reverse array to allow C file generation from brightest to darkest
    out_array = out_array[::-1]
    
    h_outfile_handle.write("#define DARKEST_VALUE_ALLOWED %d\n"%(int(out_array[-1][0]*10)))
    h_outfile_handle.write("#define BRIGHTEST_VALUE_ALLOWED %d\n\n"%(int(out_array[0][0]*10)))

    h_outfile_handle.write("extern uint16_t skydata[];\n")


    c_outfile_handle.write("#include \"skydata.h\"\n\n")
    c_outfile_handle.write("uint16_t skydata[DARKEST_VALUE_ALLOWED-BRIGHTEST_VALUE_ALLOWED+1] = {\n")
    for element in out_array:
        if element[0]!=out_array[-1][0]:
            c_outfile_handle.write("  %s, // %2.1f\n"%(element[3],element[0]))
        else:
            c_outfile_handle.write("  %s  // %2.1f\n"%(element[3],element[0]))
    c_outfile_handle.write("};\n")
    infile_handle.close()
    c_outfile_handle.close()
    h_outfile_handle.close()

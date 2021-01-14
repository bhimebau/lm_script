#!/usr/bin/env python3

""" Parse Data Commands

This command is used to align data from the sensors. 

"""
import lm
import argparse
import time
import numpy
import glob

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Break files down by data, sensor, and field')
    parser.add_argument('-s',
                        dest='startdate',
                        help='date to start processing, format = mm/dd/yyyy',
                        required=True)

    parser.add_argument('-e',
                        dest='enddate',
                        help='date to end processing, format = mm/dd/yyyy',
                        required=True)

    parser.add_argument('-l',
                        dest='sensorlist',
                        help='sensors to consider in a comma delimited list, if not provided the all is assumed',
                        required=False)

    parser.add_argument('-d',
                        dest='datadir',
                        help='directory that contains the data files from each sensor',
                        required=True)

    parser.add_argument('-o',
                        dest='outfile',
                        help='base name of the output file, <outfile>_temp,<outfile>_mag, and <outfile>_batt will be created. Extension .csv will be added',
                        required=True)
    args = parser.parse_args()
    for key in vars(args).keys():
        print(key,vars(args)[key])
    files_list = []

    # Determine names of the sensor data files
    # Create a list of the filenames
    for sensor in vars(args)['sensorlist'].split(','):
        sensor_string = "002%02d"%(int(sensor))
        for file in glob.glob(f'{args.datadir}/Sensor_{sensor_string}_*.csv'):
            files_list.append([sensor_string,file])
    print(files_list)
    

    

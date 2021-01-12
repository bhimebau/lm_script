#!/usr/bin/env python3

""" Parse Data Commands

This command is used to parse the data from the light sensors 

"""
import lm
import argparse
import time
import numpy

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
                        help='name of the output file, .csv will be added',
                        required=True)

    serial_number = input("Enter the serial number of the sensor: 00")
    args = parser.parse_args()
    sensor = lm.LightMon(args.port)
    uid = sensor.get_uid()
    fd = open(f"{args.write_dir.strip()}/Sensor_00{serial_number}_{uid.strip()}.csv","w")
    fd.write(sensor.get_data())
    fd.close()
    sensor.close_port()

#!/usr/bin/env python3

""" Lightmon Data Read Command 

This script reads the data from the light sensor. 

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
                        dest='write_dir',
                        help='directory to store the data from the sensor',
                        required=True)

    serial_number = input("Enter the serial number of the sensor: 00")
    args = parser.parse_args()
    sensor = lm.LightMon(args.port)
    uid = sensor.get_uid()
    fd = open(f"{args.write_dir.strip()}/Sensor_00{serial_number}_{uid.strip()}.csv","w")
    fd.write(sensor.get_data())
    fd.close()
    sensor.close_port()

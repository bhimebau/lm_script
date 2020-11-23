#!/usr/bin/env python3

""" Erase the sensor's data and log area in the flash
"""
import lm
import argparse
import time

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Sets the calibration temp and offset')
    parser.add_argument('-p',
                        dest='port',
                        help='Serial port device where sensor is connected, example: /dev/ttyACM0',
                        required=True)
    args = parser.parse_args()
    print("Initializing the Sensor")
    sensor = lm.LightMon(args.port)
    sensor.data_erase()
    sensor.close_port()
    

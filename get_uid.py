#!/usr/bin/env python

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

    args = parser.parse_args()
    sensor = lm.LightMon(args.port)
    print sensor.uid
    sensor.close_port()

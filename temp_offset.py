#!/usr/bin/env python3

""" Writes the calibration temperature and the offset
"""
import lm
import argparse
import time
import numpy as np

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Sets the calibration temp and offset')
    parser.add_argument('-p',
                        dest='port',
                        help='Serial port device where sensor is connected, example: /dev/ttyACM0',
                        required=True)
    parser.add_argument('-l',
                        dest='led',
                        help='Serial port device where light source is connected: /dev/ttyACM1',
                        required=True)

    args = parser.parse_args()
    print("Initializing the Sensor")
    sensor = lm.LightMon(args.port)
    print("Initializing the Light Source")
    light = lm.LightMon(args.led)

    sensor.cal_write_offset_comp(0,1)
    light.sky_write(21.2)
    sensor_mag = float(sensor.tsl237_read_mag())
    print(sensor_mag)
    offset = 21.2-sensor_mag
    print("Storing offset %f to flash"%(offset))
    sensor.cal_write_offset_comp(offset,1)
    sensor.cal_store()
    sensor.close_port()
    light.close_port()
 

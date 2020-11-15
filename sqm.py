#!/usr/bin/env python3

""" Unihedron Communication Primatives 
Class to enable sending and receiving from the SQM LU

"""
import serial
import base64
import sys
import re
import time
from datetime import datetime
import os
import pytz
import re

class SQM_LU:
    def __init__(self,sqm_serial='/dev/ttyUSB0',baud=115200):
        self.timeout = 2   # Timeout value for the serial port 
        if (self.open_port(sqm_serial,baud)!=True):
            sys.exit(1)
        self.command_return_string = ""
        self.mpsas = 0
        self.freq = 0
        self.count = 0
        self.period = 0
        self.temp = 0

    def close_port(self):
        """ Close serial port used to communicate with the xDot """
        self.port.close()

    def open_port(self,serial_port,baud): 
        """ Open the serial port connected to the LightMon board"""
        try:
            self.port = serial.Serial(serial_port, baud, timeout = self.timeout)
            return True
        except serial.serialutil.SerialException:
            print("Error: Could not open",serial_port)
            return False
    
    def send_command(self,command_string):
        """ Send a command to the LightMon's command interpreter """
        tic = time.time()
        self.port.write(command_string)
        self.command_return_string = self.port.readline().strip()
        retval = True
        return(retval)
               
    def read_raw(self):
        self.send_command("u1x")
        while (re.search("S",self.command_return_string)):
            self.send_command("u1x")
            time.sleep(1)
        for i in range(3): 
            self.send_command("u1x")
            while (re.search("S",self.command_return_string)):
                self.send_command("u1x")
                time.sleep(1)
        fields = self.command_return_string.split(',')
        self.mpsas = float(fields[1].strip().split('m')[0])
        self.freq = int(fields[2].strip().split('H')[0])
        self.count = int(fields[3].strip().split('c')[0])
        self.period = float(fields[4].strip().split('s')[0])
        self.temp = float(fields[5].strip().split('C')[0])
        return (self.command_return_string)
    
if __name__ == "__main__":
    sqm = SQM_LU()
    sqm.read_raw()
    print(sqm.command_return_string)
    print(sqm.mpsas)
    print(sqm.freq)
    print(sqm.count)
    print(sqm.period)
    print(sqm.temp)
    sqm.close_port()    

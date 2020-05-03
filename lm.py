#!/usr/bin/env python

""" Lightmon Communication Primatives 
Class to enable sending and receiving from the Lightmom 

This class implements the following functions

1.) Run an arbitrary command line interpreter command on the lightmon

2.) Set Time 

"""
import serial
import base64
import sys
import re
import time
from datetime import datetime

class LightMon:
    def __init__(self,lm_serial='/dev/ttyACM0',baud=9600):
        self.timeout = 2   # Timeout value for the serial port 
        if (self.open_port(lm_serial,baud)!=True):
            sys.exit(1)
        if (self.check_comm()!=True):
            print "Lightmon failed to Respond to AT command "
            sys.exit(1)
        if (self.whoami()!=True):
            print "Lightmon failed to Respond to UID command"
            sys.exit(1)
        self.command_return_string = ""

    def close_port(self):
        """ Close serial port used to communicate with the xDot """
        self.port.close()

    def open_port(self,serial_port,baud): 
        """ Open the serial port connected to the LightMon board"""
        try:
            self.port = serial.Serial(serial_port, baud, timeout = self.timeout)
            return True
        except serial.serialutil.SerialException:
            print "Error: Could not open",serial_port
            return False
    
    def send_command(self,command_string):
        """ Send a command to the LightMon's command interpreter """
        tic = time.time()
        self.port.write(command_string + "\n")
        # Command Echo 
        response = self.port.readline().strip()
        response = ""
        self.command_return_string = ""
        while ((response != "OK") and (response != "NOK")):
            response = self.port.readline().strip()
            if ((time.time() - tic) > 3):
                print "Command Timeout" 
                return False
            if ((response != "") and (response != "OK") and (response != "ERROR") and (response != command_string)):
                self.command_return_string = self.command_return_string + response + "\n"
        if (response == "OK"):
            retval = True
        else:
            print "Received NOK"
            retval = False
        # Read over the time/date string that is part of the command prompt 
        tic = time.time()           
        time_date_string = ""
        while (time_date_string.find(">")==-1):
            time_date_string = time_date_string + self.port.read().strip()
            if ((time.time() - tic) > 3):
                print "Command Timeout looking for prompt" 
                return False
        return(retval)
               
    def check_comm(self):
        """ Use the attention command to confirm that communicating with the xDot is possible """
        if (self.send_command("@") == True):
            return True
        else:
            return False
    
    def whoami(self): 
        """ Read the light sensors unique processor ID (from STM32L432) """
        if (self.send_command("uid") == True):
            self.uid = self.command_return_string.strip()
            return True
        else:
            return False

    def settime(self):
        """ Sets the light sensor time to match the system time """
        now = datetime.now()
        print now
        ds_string = "ds,"+now.strftime("%d,%m,%y")
        lm.send_command(ds_string)
        ts_string = "ts," + now.strftime("%H,%M,%S")
        lm.send_command(ts_string)
                   
if __name__ == "__main__":
    lm = LightMon()
    print lm.uid
    lm.settime()
    lm.send_command("tr")
    print lm.command_return_string
    lm.close_port()    

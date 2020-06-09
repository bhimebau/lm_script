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
import os
import pytz

class LightMon:
    def __init__(self,lm_serial='/dev/ttyACM0',baud=9600):
        self.timeout = 2   # Timeout value for the serial port 
        if (self.open_port(lm_serial,baud)!=True):
            sys.exit(1)
        if (self.check_comm()!=True):
            print "Lightmon failed to Respond to AT command "
            sys.exit(1)

        self.uid = 0
        #        if (self.whoami()!=True):
#            print "Lightmon failed to Respond to UID command"
#            sys.exit(1)
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
    
    def send_command(self,command_string,timeout_seconds):
        """ Send a command to the LightMon's command interpreter """
        tic = time.time()
        self.port.write(command_string + "\n")
        # Receive Command Echo 
        response = self.port.readline().strip()

        # Receive Command Response Payload
        response = ""
        self.command_return_string = ""
        while ((response != "OK") and (response != "NOK")):
            response = self.port.readline().strip()
            if ((time.time() - tic) > timeout_seconds):
                print "Command Timeout" 
                return False
            if ((response != "") and (response != "OK") and (response != "ERROR") and (response != command_string)):
                self.command_return_string = self.command_return_string + response + "\n"
        if (response == "OK"):
            retval = True
#            print "Found OK"
        else:
            print "Received NOK"
            retval = False
#            print "Found NOK"

        # Receive the command prompt  
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
        if (self.send_command("@",3) == True):
            return True
        else:
            return False
    
    def whoami(self): 
        """ Read the light sensors unique processor ID (from STM32L432) """
        if (self.send_command("uid",3) == True):
            self.uid = self.command_return_string.strip()
            return True
        else:
            return False

    def get_data(self):
        """ Pull all of the data from the sensor"""
        self.send_command("data",300)
        return (self.command_return_string)

    def get_log(self):
        """ Pull the logs from the sensor"""
        self.send_command("log",300)
        return (self.command_return_string)
    
    def settime(self):
        """ Sets the light sensor time to match the system time """
        tz = pytz.timezone('US/Eastern')
        now = datetime.now(tz)
        ds_string = "ds,"+now.strftime("%m,%d,%y")
        self.send_command(ds_string,10)
        ts_string = "ts," + now.strftime("%H,%M,%S")
        self.send_command(ts_string,10)

    def gettime(self):
        """ Retreives the light sensor's time and date """
        self.send_command("tr",10)
        time_components = self.command_return_string.strip().split(',')
        self.send_command("dr",10)
        date_components = self.command_return_string.strip().split(',')
        return  "%s/%s/%s %s:%s:%s"%(date_components[1],
                                     date_components[2],
                                     date_components[3],
                                     time_components[1],
                                     time_components[2],
                                     time_components[3])

    def difftime(self):
        """ Computes the difference between the sensors time and the system time """

        os.environ['TZ'] = 'UTC'
        
        ## Compute the sensors time in epoch time 
        self.send_command("tr",10)
        time_components = self.command_return_string.strip().split(',')
        self.send_command("dr",10)
        date_components = self.command_return_string.strip().split(',')
        epoch_str =  "%s/%s/%s %s:%s:%s"%(date_components[1],
                                          date_components[2],
                                          date_components[3],
                                          time_components[1],
                                          time_components[2],
                                          time_components[3])
        pattern = '%m/%d/%Y %H:%M:%S'
        sensor_epoch = int(time.mktime(time.strptime(epoch_str,pattern)))
        ## Compute the system's time in epoch time
        tz = pytz.timezone('US/Eastern')
        system_epoch = int((datetime.now(tz) -
                            pytz.utc.localize(datetime(1970,1,1,0,0))).total_seconds())
        # 4 * 3600 needs to be added to the sensor time to account for UTC time error in computation
        
        return sensor_epoch + (4*3600) - system_epoch
        
    def sky_write(self,mag):
        mag = round(mag,1)
        if ((mag<19.4) or (mag>24.1)):
            return (-1)
        cmd_str = "sky,%.1f"%(mag)
        print cmd_str
        self.send_command(cmd_str,10)

    def cal_write(self,mag,value):
        mag = round(mag,1)
        if ((mag<19.4) or (mag>24.1)):
            return (-1)
        cmd_str = "cal,write,%.1f,%d"%(mag,value)
        print cmd_str
        self.send_command(cmd_str,600)

    def cal_read(self):
        self.send_command("cal",600)
        return (self.command_return_string)

    def cal_erase(self):
        cmd_str = "ef,cal"
        self.send_command(cmd_str,300)
        
    def cal_store(self):
        cmd_str = "cal,store"
        self.send_command(cmd_str,300)

    def cal_load(self):
        cmd_str = "cal,load"
        self.send_command(cmd_str,300)
        
    def cal_complete(self):
        cmd_str = "cal,complete"
        self.send_command(cmd_str,300)

    def cal_lookup(self,value):
        cmd_str = "cal,lookup,%d"%(value)
        self.send_command(cmd_str,10)
        return (self.command_return_string)
                   
    def get_uid(self):
        self.send_command("uid",10)
        self.uid = self.command_return_string
        return (self.command_return_string)

    def tsl237_read_raw(self):
        self.send_command("tsl237,raw",600)
        return (self.command_return_string)

    def dac_write_raw(self,dac,rg):
        cmd_str = "sky,raw,%d,%d"%(int(dac),int(rg))
#        print cmd_str
        self.send_command(cmd_str,10)
        return (self.command_return_string)
   

if __name__ == "__main__":
    lm = LightMon()
    print lm.uid
    lm.settime()
    lm.send_command("tr",10)
    print lm.command_return_string
    data_string = lm.get_data()
    print data_string
    log_string = lm.get_log()
    print log_string
    
#   lm.send_command("data")
#    print lm.command_return_string
    lm.close_port()    

# Light Monitor Interface Scripts 
Python interface scripts for the light sensors and calibration tube. 

## Setting the Light Monitor's Time

Reads the system time and set's the sensor's time. This will allow the
sensor's time to match the system time within one second. 

**Script Name:** settime.py
**Argument(s):** 
* -p: serial port where the sensor is connected, e.g. /dev/ttyACM0 
**Example Usage:**

```bash
bhimebau@mercury:~/forge/outdoor-monitor/lm_script$ ./settime.py -p /dev/ttyACM0
Sensor's Old Date/Time: 05/15/2020 08:53:50
Sensor's New Date/Time: 05/15/2020 08:53:50
bhimebau@mercury:~/forge/outdoor-monitor/lm_script$
```

## Getting the Light Monitor's Time

Reads the sensor's current time and them compares it to the system
time. This should match within one second when checked close to
setting the time. This utility is intended to be used to check the
time when a significant drift is expected.

**Script Name:** gettime.py
**Argument(s):** 
* -p: serial port where the sensor is connected, e.g. /dev/ttyACM0 
**Example Usage:**

```bash
bhimebau@mercury:~/forge/outdoor-monitor/lm_script$ ./gettime.py -p /dev/ttyACM0
Sensor's Current Date/Time: 05/15/2020 08:53:00
Time Delta (Sensor Time-System Time): 0 seconds
bhimebau@mercury:~/forge/outdoor-monitor/lm_script$ 
```




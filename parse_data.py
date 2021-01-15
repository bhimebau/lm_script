#!/usr/bin/env python3

""" Parse Data Commands

This command is used to align data from the sensors.

"""
import argparse
import glob
import csv
from datetime import datetime
from datetime import timedelta
from collections import OrderedDict
from os.path import join

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Break files down by data, \
    sensor, and field')
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
                        help='sensors to consider in a comma delimited list,\
                        if not provided the all is assumed',
                        required=False)

    parser.add_argument('-d',
                        dest='datadir',
                        help='directory that contains the data files \
                        from each sensor',
                        required=True)

    parser.add_argument('-o',
                        dest='outfile',
                        help='base name of the output file, <outfile>_temp,\
                        <outfile>_mag, and <outfile>_batt will be created. \
                        Extension .csv will be added',
                        required=True)
    args = parser.parse_args()
    files_list = []

    startdate = datetime.strptime(f'{args.startdate},12:00:00',
                                  '%m/%d/%Y,%H:%M:%S')
    startdate -= timedelta(days=1)
    enddate = datetime.strptime(f'{args.enddate},12:00:00',
                                '%m/%d/%Y,%H:%M:%S')
    enddate += timedelta(days=1)
    # Determine names of the sensor data files
    # Create a list of the filenames
    for sensor in vars(args)['sensorlist'].split(','):
        sensor_string = "002%02d" % (int(sensor))
        for file in glob.glob(f'{args.datadir}/Sensor_{sensor_string}_*.csv'):
            files_list.append([sensor_string, file])
    batt = OrderedDict()
    batt['header'] = []
    temp = OrderedDict()
    temp['header'] = []
    light_raw = OrderedDict()
    light_raw['header'] = []
    light_mag = OrderedDict()
    light_mag['header'] = []
    for file in files_list:
        batt['header'].append(file[0])
        temp['header'].append(file[0])
        light_raw['header'].append(file[0])
        light_mag['header'].append(file[0])
        fh = open(file[1], 'r')
        lines = fh.read().split()
        for line in lines:
            fields = line.split(',')
            sampledate = datetime.strptime(f'{fields[2]},{fields[3]}',
                                           '%m/%d/%Y,%H:%M:%S')
            sampledate = sampledate.replace(minute=0, second=0)
            if (sampledate >= startdate) and (sampledate <= enddate):
                if sampledate not in batt:
                    batt[sampledate] = []
                if sampledate not in temp:
                    temp[sampledate] = []
                if sampledate not in light_raw:
                    light_raw[sampledate] = []
                if sampledate not in light_mag:
                    light_mag[sampledate] = []
                batt[sampledate].append(float(fields[4]))
                temp[sampledate].append(int(fields[5]))
                light_raw[sampledate].append(int(fields[6]))
                light_mag[sampledate].append(float(fields[7]))

    outfile_base = args.outfile.split('.')
    battfile = join(args.datadir, f'{outfile_base[0]}_batt.csv')
    tempfile = join(args.datadir, f'{outfile_base[0]}_temp.csv')
    lightrawfile = join(args.datadir, f'{outfile_base[0]}_lightraw.csv')
    lightmagfile = join(args.datadir, f'{outfile_base[0]}_lightmag.csv')

    records = 0
    with open(battfile, 'w', newline='') as fh:
        battwriter = csv.writer(fh, delimiter=',',
                                quotechar='|',
                                quoting=csv.QUOTE_MINIMAL)
        for key in batt.keys():
            row = []
            row.append(key)
            for item in batt[key]:
                row.append(item)
            battwriter.writerow(row)
            records += 1

    with open(tempfile, 'w', newline='') as fh:
        tempwriter = csv.writer(fh, delimiter=',',
                                quotechar='|',
                                quoting=csv.QUOTE_MINIMAL)
        for key in temp.keys():
            row = []
            row.append(key)
            for item in temp[key]:
                row.append(item)
            tempwriter.writerow(row)

    with open(lightrawfile, 'w', newline='') as fh:
        lightrawwriter = csv.writer(fh, delimiter=',',
                                    quotechar='|',
                                    quoting=csv.QUOTE_MINIMAL)
        for key in light_raw.keys():
            row = []
            row.append(key)
            for item in light_raw[key]:
                row.append(item)
            lightrawwriter.writerow(row)

    with open(lightmagfile, 'w', newline='') as fh:
        lightmagwriter = csv.writer(fh, delimiter=',',
                                    quotechar='|',
                                    quoting=csv.QUOTE_MINIMAL)
        for key in light_mag.keys():
            row = []
            row.append(key)
            for item in light_mag[key]:
                row.append(item)
            lightmagwriter.writerow(row)

    print(f"{records} records found between {startdate} and {enddate}...")
    print(f"Wrote {battfile}")
    print(f"Wrote {tempfile}")
    print(f"Wrote {lightrawfile}")
    print(f"Wrote {lightmagfile}")

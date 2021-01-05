#!/usr/bin/env python3

''' Weather Example

Uses pyowm (python wrapper for open weather map)
See https://github.com/csparpa/pyowm for an example

You must install pyowm and dependencies first

pip3 install pyowm

Documentation for V2.5 of the weather API
https://github.com/csparpa/pyowm/blob/2.10-LTS/sphinx/usage-examples-v2/weather-api-usage-examples.md#getting-currently-observed-weather-for-a-specific-location
'''

from pyowm import OWM
owm = OWM('8e9cca517eb8feeda141d0e9f6952d8c')
observation = owm.weather_at_place('Monroe,US')
w = observation.get_weather()
temp_dictionary = w.get_temperature(unit='fahrenheit')
outdoor_temperature = temp_dictionary['temp']
print(outdoor_temperature)



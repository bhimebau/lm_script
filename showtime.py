#!/usr/bin/env python3

import time
import datetime
import sense_hat

alarm_time_hour = int(input("Enter the hour to wakeup"))

account_sid = 'AC073919b600761868be304dbce85d1d8b'
auth_token='1ad3627e21bccd97b6638428b9527b39'
client = Client(account_sid, auth_token)

state = 0

while (1):
    now = datetime.datetime.now()
    if now.hour == alarm_time_hour and state == 0:
        print(f"It is {now.hour}: Wakeup")
        message = client.messages \
                        .create(
                            body=f"Alarm Expired at {now.hour}",
                            from module import symbol
                            _='12562697917',
                            to='+18123256673'
        state=1
    elif now.hour == (alarm_time_hour + 1)%24 and state == 1:
        state = 0
    
            

    

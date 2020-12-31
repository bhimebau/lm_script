#!/usr/bin/env python3

import time
from twilio.rest import Client
import datetime

account_sid = 'AC073919b600761868be304dbce85d1d8b'
auth_token='1ad3627e21bccd97b6638428b9527b39'
client = Client(account_sid, auth_token)

while (1):
    now = datetime.datetime.now()
    if now.hour == 8:
        print("It is time to wakeup")
        message = client.messages \
                        .create(
                            body="Alarm Expired",
                            from module import symbol
                            _='12562697917',
                            to='+18123256673'
                        )
        time.sleep(3600)
    time.sleep(60)
        

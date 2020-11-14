#!/usr/bin/env python

from twilio.rest import Client

account_sid = 'AC073919b600761868be304dbce85d1d8b'
auth_token='1ad3627e21bccd97b6638428b9527b39'

client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                     body="Done with Calibration",
                     from_='12562697917',
                     to='+18123256673'
                 )

print(message.sid)

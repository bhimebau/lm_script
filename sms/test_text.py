#!/usr/bin/env python

from twilio.rest import Client

account_sid = 'AC073919b600761868be304dbce85d1d8b'
auth_token='56fa4d513f8a3d09d8466c11eac6b999'

client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                     body="Done with Calibration",
                     from_='12562697917',
                     to='+18123256673'
                 )

print(message.sid)

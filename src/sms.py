#!/bin/env python
# -*- coding: utf-8 -*-
import requests
import json
def sms_send(receiver,msg,timeout):
    values = {'to' : receiver,
              'param' : msg,
              'flag' : '1' }
    headers = { 'cache-control':'no-cache','content-type':'application/json','postman-token' : '9f981ea5-35e7-9a18-1be5-1456050d4249'}
    data = requests.post(url='http://192.168.206.149:18005/sendMessage',data=json.dumps(values),headers=headers,timeout=timeout)
    return data.json()

if __name__ == '__main__':
    response = sms_send(receiver=17710399068,msg="test",timeout=5)
    print(response)

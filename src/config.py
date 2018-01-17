#!/usr/bin/env python
# encoding: utf-8

class Config(object):
    SMS_URI = 'http://192.168.206.149:18005/sendMessage'


class ProductionConfig(Config):
    DEBUG = False
    SET_OFF_DATE = u'2018-02-14'


class DevelopmentConfig(Config):
    DEBUG = True
    SET_OFF_DATE = u'2018-01-20'

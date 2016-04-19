#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
 This library offers an API to use Tacyt in a python environment.
 Copyright (C) 2015 Eleven Paths
'''

import json


class Error(object):

    def __init__(self, json_data):

        self.code = json_data['code']
        self.message = json_data['message']

    def get_code(self):
        return self.code

    def get_message(self):
        return self.message

    def to_json(self):
        return {"code" : self.code, "message" : self.message}

    def __repr__(self):
        return json.dumps(self.to_json())

    def __str__(self):
        return self.__repr__()
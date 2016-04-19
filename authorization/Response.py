#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
This library offers an API to use Tacyt in a python environment.
Copyright (C) 2015 Eleven Paths
'''

import json

from authorization import Error


class Response(object):
    '''
    This class models a response from any of the endpoints in the Tacyt API.
    It consists of a "data" and an "error" elements. Although normally only one of them will be
    present, they are not mutually exclusive, since errors can be non fatal, and therefore a response
    could have valid information in the data field and at the same time inform of an error.
    '''

    def __init__(self, data=None, error=None, json_string=None ):
        '''
        @param $json a json string received from one of the methods of the Tacyt API
        '''
        self.data = data
        self.error = error
        if json_string is not None:
            json_object = json.loads(json_string)
            if "data" in json_object:
                self.data = json_object["data"]
            else:
                self.data = ""
            if "error" in json_object:
                self.error = Error.Error(json_object["error"])
            else:
                self.error = ""

    def get_data(self):
        '''
        @return JsonObject the data part of the API response
        '''
        return self.data

    def set_data(self, data):
        '''
        @param $data the data to include in the API response
        '''
        self.data = json.loads(data)

    def get_error(self):
        '''
        @return Error the error part of the API response, consisting of an error code and an error message
        '''
        return self.error

    def set_error(self, error):
        '''
        @param $error an error to include in the API response
        '''
        self.error = Error.Error(error)

    def to_json(self):
        '''
        @return a Json object with the data and error parts set if they exist
        '''
        json_response = {}

        if hasattr(self, "data"):
            json_response["data"] = self.data

        if hasattr(self, "error"):
            json_response["error"] = self.error

        return json_response
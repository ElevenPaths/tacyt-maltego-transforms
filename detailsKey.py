#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Get all details from app.
:param key:
:return:
"""
from tacyt import TacytApp
from maltego.MaltegoTransform import *
from APIManagement import Tacyt
from maltego.Entities import TacytEntities as te

api = TacytApp.TacytApp(Tacyt.APP_ID, Tacyt.SECRET_KEY)
m = MaltegoTransform()

key = sys.argv[1]

try:
    result = api.get_app_details(key)
    data = result.get_data()

    if 'result' in data and data['result'] is not None:
        details = data['result']

        if 'packageName' in details:
            m.addEntity(te.FIELD, details['packageName'].encode('utf-8'), te.FIELD_NAME, 'packageName')

        if 'hashPath' in details:
            m.addEntity(te.HASH, details['hashPath'].encode('utf-8'), te.FIELD_NAME, 'hashPath or SHA-1')

        if 'md5' in details:
            m.addEntity(te.HASH, details['md5'].encode('utf-8'), te.FIELD_NAME, 'md5')

        if 'sha256' in details:
            m.addEntity(te.HASH, details['sha256'].encode('utf-8'), te.FIELD_NAME, 'sha256')

        if 'size' in details:
            size = details['size']
            m.addEntity(te.FIELD, str(size).encode('utf-8'), te.FIELD_NAME, 'size')


    else:
        m.addUIMessage("The search returns null results")

except Exception as e:
    m.addException(str(e))
    m.throwExceptions()

m.returnOutput()


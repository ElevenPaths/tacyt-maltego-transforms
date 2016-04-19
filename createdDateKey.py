#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Get create date from an app.

:param key:
:return:
"""
from datetime import datetime

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
        createDate = data['result']['createDate'].encode('utf-8')

        datetime = datetime.strptime(createDate, '%Y-%m-%dT%H:%M:%SZ')
        m.addEntity(te.FIELD, datetime.strftime('%Y-%m-%d %H:%M:%S'), te.FIELD_NAME, 'createDate')
        m.returnOutput()

    else:
        m.addException("The search returns null results")
        m.throwExceptions()

except Exception as e:
    m.addException(str(e))
    m.throwExceptions()


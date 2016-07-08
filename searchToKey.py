#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Search apps by emails

:param field: emails to find
:return: keys from the apps founds.
"""
from tacyt import TacytApp
from maltego.MaltegoTransform import *
from APIManagement import Tacyt
from maltego.Entities import TacytEntities as te

api = TacytApp.TacytApp(Tacyt.APP_ID, Tacyt.SECRET_KEY)
m = MaltegoTransform()

field = sys.argv[1]

try:
    query = "%s"%field
    result = api.search_apps(query=query,maxResults=100)
    data = result.get_data()

    if 'result' in data and data['result'] is not None and 'applications' in data['result'] and data['result']['applications']:
        for data in data['result']['applications']:
            if 'key' in data and data['key'] is not None:
                application = data['key']
                m.addEntity(te.KEY, application.encode('utf-8'))
            else:
                m.addUIMessage("The key is not found in the results")

    else:
        m.addUIMessage("The search returns null results")

except Exception as e:
    m.addException(str(e))
    m.throwExceptions()

m.returnOutput()
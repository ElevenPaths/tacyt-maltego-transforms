#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Search apps by title.

:param field: title title to find
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
    query = "title:%s" % field
    result = api.search_apps(query=query)
    data = result.get_data()

    if 'result' in data and data['result'] is not None and 'applications' in data['result'] and data['result']['applications']:
        for data in data['result']['applications']:
            if 'key' in data and data['key'] is not None:
                application = data['key']
                m.addEntity(te.KEY, application.encode('utf-8'))
            else:
                m.addException("The key is not found in the results")
                m.throwExceptions()

        m.returnOutput()

    else:
        m.addException("The search returns null results")
        m.throwExceptions()

except Exception as e:
    m.addException(str(e))
    m.throwExceptions()

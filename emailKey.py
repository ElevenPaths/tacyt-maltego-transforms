#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Get permission from app.

:param key: key from app
:return: keys from the apps founds.
"""
from tacyt import TacytApp
from maltego.MaltegoTransform import *
from APIManagement import Tacyt
from maltego.Entities import TacytEntities as te

api = TacytApp.TacytApp(Tacyt.APP_ID, Tacyt.SECRET_KEY)
m = MaltegoTransform()

app = sys.argv[1]


try:
    result = api.get_app_details(app)
    data = result.get_data()

    if 'result' in data and data['result'] is not None:
        details = data['result']

        if 'emails' in details:
            permissions = details['emails']
            for i in permissions:
                m.addEntity(te.EMAIL,i, te.FIELD_NAME, 'emails')

        m.returnOutput()

    else:
        m.addException("The search returns null results")
        m.throwExceptions()

except Exception as e:
    m.addException(str(e))
    m.throwExceptions()

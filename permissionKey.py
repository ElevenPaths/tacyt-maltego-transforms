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
        if 'nPermissions' in details:
            m.addEntity(te.FIELD, str(details['nPermissions']), te.FIELD_NAME, 'nPermissions')

        if 'permissionName' in details:
            permissions = details['permissionName']
            for i in permissions:
                m.addEntity(te.FIELD,i, te.FIELD_NAME, 'permissionName')

    else:
        m.addUIMessage("The search returns null results")

except Exception as e:
    m.addException(str(e))
    m.throwExceptions()


m.returnOutput()
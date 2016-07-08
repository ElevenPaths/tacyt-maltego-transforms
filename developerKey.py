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

        if 'developerName' in details:
            if len(details['developerName']) > 0:
                m.addEntity(te.ALIAS, str(details['developerName'].encode('utf-8')), te.FIELD_NAME, 'developerName')

        if 'developerPrivacy' in details:
            if len(details['developerPrivacy']) > 0:
                m.addEntity(te.DOMAIN, str(details['developerPrivacy'].encode('utf-8')), te.FIELD_NAME, 'developerPrivacy')

        if 'developerWeb' in details:
            if len(details['developerWeb']) > 0:
                m.addEntity(te.DOMAIN, str(details['developerWeb'].encode('utf-8')), te.FIELD_NAME, 'developerWeb')

        if 'developerEmail' in details:
            if len(details['developerEmail']) > 0:
                m.addEntity(te.EMAIL, str(details['developerEmail'].encode('utf-8')), te.FIELD_NAME, 'developerEmail')

    else:
       m.addUIMessage("The search returns null results")

except Exception as e:
    m.addException(str(e))
    m.throwExceptions()

m.returnOutput()
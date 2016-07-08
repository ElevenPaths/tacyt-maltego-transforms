#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Search certificate by key app.
For more information see User Manual.

:param key: key to search, for example: com.elevenpaths.android.latch11GooglePlay
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
        if 'certificateValidFrom' in details:
            if len(details['certificateValidFrom']) > 0:
                certificateValidFrom = details['certificateValidFrom']
                m.addEntity('maltego.Phrase', certificateValidFrom, te.FIELD_NAME, 'certificateValidFrom')


        if 'certificateValidTo' in details:
            if len(details['certificateValidTo']) > 0:
                certificateValidTo = details['certificateValidTo']
                m.addEntity('maltego.Phrase', certificateValidTo, te.FIELD_NAME, 'certificateValidTo')

        if 'certificateFingerprint' in details:
            if len(details['certificateFingerprint']) > 0:
                certificateFingerprint = details['certificateFingerprint']
                m.addEntity('maltego.Phrase', certificateFingerprint, te.FIELD_NAME, 'certificateFingerprint')

        if 'certificateSubjectCommonName' in details:
            if len(details['certificateSubjectCommonName']) > 0:
                m.addEntity(te.ALIAS, details['certificateSubjectCommonName'], te.FIELD_NAME, 'certificateSubjectCommonName')

        if 'certificateSubjectCountryName' in details:
            if len(details['certificateSubjectCountryName']) > 0:
                m.addEntity(te.FIELD, details['certificateSubjectCountryName'], te.FIELD_NAME, 'certificateSubjectCountryName')

        if 'certificateSubjectLocality' in details:
            if len(details['certificateSubjectLocality']) > 0:
                m.addEntity(te.FIELD, details['certificateSubjectLocality'], te.FIELD_NAME, 'certificateSubjectLocality')

        if 'certificateSubjectOrganizationName' in details:
            if len(details['certificateSubjectOrganizationName']) > 0:
                m.addEntity(te.ALIAS, details['certificateSubjectOrganizationName'], te.FIELD_NAME, 'certificateSubjectOrganizationName')

        if 'certificateSubjectOrganizationUnitName' in details:
            if len(details['certificateSubjectOrganizationUnitName']) > 0:
                m.addEntity(te.FIELD, details['certificateSubjectOrganizationUnitName'], te.FIELD_NAME, 'certificateSubjectOrganizationUnitName')

        if 'certificatePublicKeyInfo' in details:
            if len(details['certificatePublicKeyInfo']) > 0:
                certificatePublicKeyInfo = details['certificatePublicKeyInfo']
                m.addEntity('maltego.Phrase', certificatePublicKeyInfo, te.FIELD_NAME, 'certificatePublicKeyInfo')

        if 'certificateSignatureAlgorithm' in details:
            if len(details['certificateSignatureAlgorithm']) > 0:
                certificateSignatureAlgorithm = details['certificateSignatureAlgorithm']
                m.addEntity('maltego.Phrase', certificateSignatureAlgorithm,te.FIELD_NAME, 'certificateSignatureAlgorithm')


        if len(m.entities) > 0:
            m.returnOutput()

        else:
            m.addUIMessage("The search returns null results")

    else:
        m.addUIMessage("The search returns null results")

except Exception as e:
    m.addException(str(e))
    m.throwExceptions()


m.returnOutput()
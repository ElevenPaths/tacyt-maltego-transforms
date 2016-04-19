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
        if 'certificateFingerprint' in details:
            certificateFingerprint = details['certificateFingerprint']
            m.addEntity('maltego.Phrase', certificateFingerprint, te.FIELD_NAME, 'certificateFingerprint')

        if 'certificatePublicKey' in details:
            certificatePublicKey = details['certificatePublicKey']
            m.addEntity('maltego.Phrase', certificatePublicKey, te.FIELD_NAME, 'certificatePublicKey')

        if 'certificateSignatureAlgorithm' in details:
            certificateSignatureAlgorithm = details['certificateSignatureAlgorithm']
            m.addEntity('maltego.Phrase', certificateSignatureAlgorithm,te.FIELD_NAME, 'certificateSignatureAlgorithm')

        if 'certificateValidFrom' in details:
            certificateValidFrom = details['certificateValidFrom']
            m.addEntity('maltego.Phrase', certificateValidFrom, te.FIELD_NAME, 'certificateValidFrom')

        if 'certificateValidTo' in details:
            certificateValidTo = details['certificateValidTo']
            m.addEntity('maltego.Phrase', certificateValidTo, te.FIELD_NAME, 'certificateValidTo')

        if 'certificateIssuerCommonName' in details:
            certificateIssuerCommonName = details['certificateIssuerCommonName']
            m.addEntity('maltego.Phrase', certificateIssuerCommonName, te.FIELD_NAME, 'certificateIssuerCommonName')

        if 'certificateValidityGapRoundedYears' in details:
            certificateValidityGapRoundedYears = details['certificateValidityGapRoundedYears']
            m.addEntity('maltego.Phrase', str(certificateValidityGapRoundedYears), te.FIELD_NAME, 'certificateValidityGapRoundedYears')

        if 'certificateValidityGapSeconds' in details:
            certificateValidityGapSeconds = details['certificateValidityGapSeconds']
            m.addEntity('maltego.Phrase', str(certificateValidityGapSeconds), te.FIELD_NAME, 'certificateValidityGapSeconds')

        if 'certificateAutoSigned' in details:
            certificateAutoSigned = details['certificateAutoSigned']
            m.addEntity('maltego.Phrase', certificateAutoSigned, te.FIELD_NAME, 'certificateAutoSigned')

        if 'certificatePublicKeyInfo' in details:
            certificatePublicKeyInfo = details['certificatePublicKeyInfo']
            m.addEntity('maltego.Phrase', certificatePublicKeyInfo, te.FIELD_NAME, 'certificatePublicKeyInfo')

        if 'certificateVersion' in details:
            certificateVersion = details['certificateVersion']
            m.addEntity('maltego.Phrase', str(certificateVersion), te.FIELD_NAME, 'certificateVersion')

        if 'certificateSerialNumber' in details:
            certificateSerialNumber = details['certificateSerialNumber']
            m.addEntity('maltego.Phrase', certificateSerialNumber, te.FIELD_NAME, 'certificateSerialNumber')

        if 'certificateSubjectCommonName' in details:
            m.addEntity(te.FIELD, details['certificateSubjectCommonName'], te.FIELD_NAME, 'certificateSubjectCommonName')

        if 'certificateIssuerCountryName' in details:
            m.addEntity(te.FIELD, details['certificateIssuerCountryName'], te.FIELD_NAME, 'certificateIssuerCountryName')

        if 'certificateSubjectOrganizationUnitName' in details:
            m.addEntity(te.FIELD, details['certificateSubjectOrganizationUnitName'], te.FIELD_NAME, 'certificateSubjectOrganizationUnitName')

        if 'certificateIssuerOrganizationUnitName' in details:
            m.addEntity(te.FIELD, details['certificateIssuerOrganizationUnitName'], te.FIELD_NAME, 'certificateIssuerOrganizationUnitName')

        if 'certificateSubjectState' in details:
            m.addEntity(te.FIELD, details['certificateSubjectState'], te.FIELD_NAME, 'certificateSubjectState')

        if 'certificateSubjectCountryName' in details:
            m.addEntity(te.FIELD, details['certificateSubjectCountryName'], te.FIELD_NAME, 'certificateSubjectCountryName')

        if 'certificateIssuerState' in details:
            m.addEntity(te.FIELD, details['certificateIssuerState'], te.FIELD_NAME, 'certificateIssuerState')

        if 'certificateSubjectLocality' in details:
            m.addEntity(te.FIELD, details['certificateSubjectLocality'], te.FIELD_NAME, 'certificateSubjectLocality')

        if 'certificateIssuerOrganizationName' in details:
            m.addEntity(te.FIELD, details['certificateIssuerOrganizationName'], te.FIELD_NAME, 'certificateIssuerOrganizationName')

        if 'certificateSubjectOrganizationName' in details:
            m.addEntity(te.FIELD, details['certificateSubjectOrganizationName'], te.FIELD_NAME, 'certificateSubjectOrganizationName')

        if len(m.entities) > 0:
            m.returnOutput()

        else:
            m.addException("The search returns null results")
            m.throwExceptions()

    else:
        m.addException("The search returns null results")
        m.throwExceptions()

except Exception as e:
    m.addException(str(e))
    m.throwExceptions()



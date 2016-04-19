#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv

from tacyt import tacytapp
from maltego.MaltegoTransform import *


api = tacytapp.TacytApp()
m = MaltegoTransform()

c = csv.writer(open("detailsCertificate.csv", "wb"))
c.writerow(["certificateFingerprint", "certificatePublicKey", "certificateSignatureAlgorithm", "certificateValidFrom", "certificateValidTo", "certificateIssuerCommonName", "certificateValidityGapRoundedYears", "certificateValidityGapSeconds", "certificateAutoSigned", "certificatePublicKeyInfo", "certificateVersion", "certificateSerialNumber"])

app = sys.argv[1]

try:

    result = api.get_app_details(app)
    data = result.get_data()

    certificateFingerprint = data['result']['certificateFingerprint']
    m.addEntity('maltego.Phrase', certificateFingerprint)

    certificatePublicKey = data['result']['certificatePublicKey']
    m.addEntity('maltego.Phrase', certificatePublicKey)

    certificateSignatureAlgorithm = data['result']['certificateSignatureAlgorithm']
    m.addEntity('maltego.Phrase', certificateSignatureAlgorithm)

    certificateValidFrom = data['result']['certificateValidFrom']
    m.addEntity('maltego.Phrase', certificateValidFrom)

    certificateValidTo = data['result']['certificateValidTo']
    m.addEntity('maltego.Phrase', certificateValidTo)

    certificateIssuerCommonName = data['result']['certificateIssuerCommonName']
    m.addEntity('maltego.Phrase', certificateIssuerCommonName)

    certificateValidityGapRoundedYears = data['result']['certificateValidityGapRoundedYears']
    m.addEntity('maltego.Phrase', str(certificateValidityGapRoundedYears))

    certificateValidityGapSeconds = data['result']['certificateValidityGapSeconds']
    m.addEntity('maltego.Phrase', str(certificateValidityGapSeconds))

    certificateAutoSigned = data['result']['certificateAutoSigned']
    m.addEntity('maltego.Phrase', certificateAutoSigned)

    certificatePublicKeyInfo = data['result']['certificatePublicKeyInfo']
    m.addEntity('maltego.Phrase', certificatePublicKeyInfo)

    certificateVersion = data['result']['certificateVersion']
    m.addEntity('maltego.Phrase', str(certificateVersion))

    certificateSerialNumber = data['result']['certificateSerialNumber']
    m.addEntity('maltego.Phrase', certificateSerialNumber)




except Exception as e:
    m.addUIMessage(str(e))
m.returnOutput()

my_list = [certificateFingerprint, certificatePublicKey, certificateSignatureAlgorithm, certificateValidFrom, certificateValidTo, certificateIssuerCommonName, certificateValidityGapRoundedYears, certificateValidityGapSeconds, certificateAutoSigned, certificatePublicKeyInfo, certificateVersion, certificateSerialNumber]
c.writerow(my_list)

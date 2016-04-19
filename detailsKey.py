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

        if 'origin' in details:
            m.addEntity(te.FIELD, details['origin'].encode('utf-8'), te.FIELD_NAME, 'origin')

        if 'packageName' in details:
            m.addEntity(te.FIELD, details['packageName'].encode('utf-8'), te.FIELD_NAME, 'packageName')

        if 'developerEmail' in details:
            m.addEntity(te.MAIL, details['developerEmail'].encode('utf-8'), te.FIELD_NAME, 'developerEmail')

        if 'developerName' in details:
            m.addEntity(te.FIELD, details['developerName'].encode('utf-8'), te.FIELD_NAME, 'developerName')

        if 'developerWeb' in details:
            m.addEntity(te.URL, details['developerWeb'].encode('utf-8'), te.FIELD_NAME, 'developerWeb')

        if 'developerPrivacy' in details:
            m.addEntity(te.URL, details['developerPrivacy'].encode('utf-8'), te.FIELD_NAME, 'developerPrivacy')

        if 'categoryName' in details:
            m.addEntity(te.FIELD, details['categoryName'].encode('utf-8'), te.FIELD_NAME, 'categoryName')

        if 'certificateSubjectLocality' in details:
            m.addEntity(te.FIELD, details['certificateSubjectLocality'].encode('utf-8'), te.FIELD_NAME, 'certificateSubjectLocality')

        if 'hashPath' in details:
            m.addEntity(te.FIELD, details['hashPath'].encode('utf-8'), te.FIELD_NAME, 'hashPath or SHA-1')

        if 'title' in details:
            m.addEntity(te.FIELD, details['title'].encode('utf-8'), te.FIELD_NAME, 'title')

        if 'size' in details:
            size = details['size']
            m.addEntity(te.FIELD, str(size).encode('utf-8'), te.FIELD_NAME, 'size')

        if 'numDownloads' in details:
            numDownloads = details['numDownloads']
            m.addEntity(te.FIELD, str(numDownloads).encode('utf-8'), te.FIELD_NAME, 'numDownloads')

        if 'price' in details:
            price = details['price']
            m.addEntity(te.FIELD, str(price).encode('utf-8'), te.FIELD_NAME, 'price' )

        if 'links' in details:
            link = details['links']
            for i in link:
                m.addEntity(te.URL, i.encode('utf-8'), te.FIELD_NAME, 'link')

        if 'emails' in details:
            email_list = details['emails']
            for i in email_list:
                m.addEntity(te.MAIL, i.encode('utf-8'), te.FIELD_NAME, 'email')

        if 'marketLinks' in details:
            market_list = details['marketLinks']
            for i in market_list:
                m.addEntity(te.URL, i.encode('utf-8'), te.FIELD_NAME, 'marketLinks')


        if 'md5' in details:
            m.addEntity(te.FIELD, details['md5'].encode('utf-8'), te.FIELD_NAME, 'md5')

        if 'sha256' in details:
            m.addEntity(te.FIELD, details['sha256'].encode('utf-8'), te.FIELD_NAME, 'sha256')

        if 'nServices' in details:
            m.addEntity(te.FIELD, str(details['nServices']).encode('utf-8'), te.FIELD_NAME, 'nServices')

        if 'nActivities' in details:
            m.addEntity(te.FIELD, str(details['nActivities']).encode('utf-8'), te.FIELD_NAME, 'nActivities')

        if 'versionString' in details:
            m.addEntity(te.FIELD, str(details['versionString']).encode('utf-8'), te.FIELD_NAME, 'versionString')

        if 'versionCode' in details:
            m.addEntity(te.FIELD, str(details['versionCode']).encode('utf-8'), te.FIELD_NAME, 'versionCode')

        if 'marketSize' in details:
            m.addEntity(te.FIELD, str(details['marketSize']).encode('utf-8'), te.FIELD_NAME, 'marketSize')

        if 'createDate' in details:
            m.addEntity(te.FIELD, str(details['createDate']).encode('utf-8'), te.FIELD_NAME, 'createDate')

        if 'oldestDateFile' in details:
            m.addEntity(te.FIELD, str(details['oldestDateFile']).encode('utf-8'), te.FIELD_NAME, 'oldestDateFile')

        if 'deadDate' in details:
            m.addEntity(te.FIELD, str(details['deadDate']).encode('utf-8'), te.FIELD_NAME, 'deadDate')

        if 'newestDateFile' in details:
            m.addEntity(te.FIELD, str(details['newestDateFile']).encode('utf-8'), te.FIELD_NAME, 'newestDateFile')

        if 'updateDate' in details:
            m.addEntity(te.FIELD, str(details['updateDate']).encode('utf-8'), te.FIELD_NAME, 'updateDate')



        m.returnOutput()

    else:
        m.addException("The search returns null results")
        m.throwExceptions()

except Exception as e:
    m.addException(str(e))
    m.throwExceptions()




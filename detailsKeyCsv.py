#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv

from tacyt import tacytapp
from maltego.MaltegoTransform import *


api = tacytapp.TacytApp()
m = MaltegoTransform()

c = csv.writer(open("detailsKey.csv", "wb"))
c.writerow(["origin", "title", "developerEmail", "developerName", "developerWeb", "categoryName", "sha256", "hashPath", "packageName", "size(BYTES)", "numDownloads", "price(EUR)", "links", "developerPrivacy"])

app = sys.argv[1]

try:

    result = api.get_app_details(app)
    data = result.get_data()
    print data
    origin = data['result']['origin'].encode('utf-8')
    m.addEntity('maltego.Phrase', origin)

    packageName = data['result']['packageName'].encode('utf-8')
    m.addEntity('maltego.Phrase', packageName)

    developerEmail = data['result']['developerEmail'].encode('utf-8')
    m.addEntity('maltego.Email', developerEmail)

    developerName = data['result']['developerName'].encode('utf-8')
    m.addEntity('maltego.Person', developerName)

    developerWeb = data['result']['developerWeb'].encode('utf-8')
    m.addEntity('maltego.Website', developerWeb)

    categoryName = data['result']['categoryName'].encode('utf-8')
    m.addEntity('maltego.Phrase', categoryName)

    sha256 = data['result']['sha256'].encode('utf-8')
    m.addEntity('maltego.Location', sha256)

    hash = data['result']['hashPath'].encode('utf-8')
    m.addEntity('maltego.Phrase', hash)

    title = data['result']['title'].encode('utf-8')
    m.addEntity('maltego.Phrase', title)

    size = data['result']['size']
    s = str(size).encode('utf-8')
    m.addEntity('maltego.Phrase', s)

    numDownloads = data['result']['numDownloads']
    nD = str(numDownloads).encode('utf-8')
    m.addEntity('maltego.Phrase', nD)

    price = data['result']['price']
    p = str(price).encode('utf-8')
    m.addEntity('maltego.Phrase', p)

    link = data['result']['links']
    for i in link:

        m.addEntity('maltego.Website', i.encode('utf-8'))

    developerPrivacy = data['result']['developerPrivacy'].encode('utf-8')
    m.addEntity('maltego.Phrase', developerPrivacy)



except Exception as e:
    m.addUIMessage(str(e))
m.returnOutput()

myList = [origin, title, developerEmail, developerName, developerWeb, categoryName, sha256, hash, packageName, size, numDownloads, price, link, developerPrivacy]
c.writerow(myList)
# Copyright (C) 2014 Joao Carreira
import httplib
import os
from os import listdir
import shutil
import xml.etree.ElementTree as ET
import urllib
import urllib2
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers


def upload(repo, token, apk):
    fields = {"token": token, "repo": repo, "apk": open(apk, "rb"), "mode": "jason"}
    webservice = "https://www.aptoide.com/webservices/uploadAppToRepo"
    register_openers()
    datagen, headers = multipart_encode(fields)

    try:
        request = urllib2.Request(webservice, datagen, headers)
        response = urllib2.urlopen(request).read()
        print(response)
        os.remove(apks_downloaded)

    except httplib.BadStatusLine:
        print("Got BadStatusLine from Aptoide upload.")

    return()

total = 0
store = raw_input("Insert store name to download apps: ")
repo = raw_input("Insert your store name to upload the apps: ")
token = raw_input("Insert your dev token: ")
store_xml = "http://" + store + ".store.aptoide.com/info.xml"

for f in listdir("."):
    if f.endswith(".xml"):
        os.remove(f)

try:
    shutil.rmtree('apks')

except OSError:
    os.makedirs("apks")

urllib.urlretrieve(store_xml, "info.xml")
print ("info.xml - Downloaded")
tree = ET.parse('info.xml')
root = tree.getroot()
repository = root.findall('repository')
base_path = repository[0].find('basepath').text

for package in root.findall('package'):
    apk_path = package.find('path').text
    apks_downloaded = "apks/" + apk_path
    print ("Downloading: " + apk_path)

    try:
        urllib.urlretrieve(base_path + apk_path, apks_downloaded)
        print ("Download Successful")
        upload(repo, token, apks_downloaded)
        total += 1

    except IOError:
        print("Download Failed")


os.remove("info.xml")
total = str(total)
print ("Total of Downloaded and Downloaded Files: " + total)
raw_input("Press any key to continue...")
os.system("clear")
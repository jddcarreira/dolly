import httplib
import os
from os import listdir
import xml.etree.ElementTree as ET
import shutil
import filecmp
import urllib
import urllib2
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers

class AptoideUtils:

	def clean(self):
	    try:
	        os.remove('info.xml')
	        os.remove('apk_cache')
	        shutil.rmtree('apks')
	        os.makedirs("apks")
	        print("Cache: Cleared | Apks folder created")

	    except OSError:
	        os.makedirs("apks")
	        print("Cache: Cleared | Apks folder created")

	    return "Done"


	def download(self):
	    total = 0
	    store = raw_input("Insert store name: ")
	    store_xml = "http://" + store + ".store.aptoide.com/info.xml"

	    for f in listdir("."):
	        if f.endswith(".xml"):
	            os.remove(f)

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
	            total += 1

	        except IOError:
	            print("Download Failed")

	    os.remove("info.xml")
	    total = str(total)
	    print ("Total of Downloaded Files: " + total)
	    raw_input("Press any key to continue...")
	    os.system("clear")

	    return "Done"
	    

	def upload(self, repo, token):
	    try:
	        os.remove('apk_cache')
	        os.system("ls apks/*.apk > apk_cache")
	        apk_cache = open("apk_cache", "rw+")

	    except OSError:
	        os.system("ls apks/*.apk > apk_cache")
	        apk_cache = open("apk_cache", "rw+")

	    print ("APK Cache - Complete")

	    for apk_path in apk_cache:
	        apk_path = apk_path.strip()
	        #apk_name = apk_path.replace("apks/", "", 1)
	        fields = {
	                "token": token,
	                "repo": repo,
	                "apk": open(apk_path, "rb"),
	                "mode": "jason"
	                }
	        webservice = "https://www.aptoide.com/webservices/uploadAppToRepo"
	        register_openers()
	        datagen, headers = multipart_encode(fields)

	        try:
	            request = urllib2.Request(webservice, datagen, headers)
	            response = urllib2.urlopen(request).read()
	            print(response)
	            os.remove(apk_path)

	        except httplib.BadStatusLine:
	            print("Got BadStatusLine from Aptoide upload.")

	    apk_cache.close()
	    os.remove('apk_cache')

	    return "Done"
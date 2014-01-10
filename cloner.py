# Copyright (C) 2014 Joao Carreira
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


def clean():
    try:
        os.remove('info.xml')
        os.remove('apk_cache')
        shutil.rmtree('apks')
        os.makedirs("apks")
        print("Cache: Cleared | Apks folder created")

    except OSError:
        os.makedirs("apks")
        print("Cache: Cleared | Apks folder created")

    return menu()


def download():
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

    return menu()


def upload(repo, token):
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

    return menu()


def file_comparison():
    ffile = raw_input("Insert the path for the first file: ")
    sfile = raw_input("Insert the path for the second file: ")

    if filecmp.cmp(ffile, sfile):
        print ("The files are equal!")
        raw_input("Press any key to go back to the menu...")
    else:
        print ("The files are not equal!")
        raw_input("Press any key to go back to the menu...")

    return menu()


def menu():
    print ("1 - Download All Apps from Repo")
    print ("2 - Upload All Apps to Repo")
    print ("3 - File Comparison of Two Files")
    print ("9 - Setup/Clean Configuration Files")
    print ("0 - Exit")
    user_input = raw_input ("Choose an option: ")

    if user_input == "1":
        download ()
    elif user_input == "2":
        user_input_store = raw_input ("Insert your store name: ")
        user_input_token = raw_input ("Insert your store token: ")
        upload (user_input_store, user_input_token)
    elif user_input == "3":
        file_comparison()
    elif user_input == "9":
        clean ()
    elif user_input == "0":
        exit()
    else:
        menu()

    return

menu()

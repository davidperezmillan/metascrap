#!/usr/bin/env python
# -*- coding: utf-8 -*-


import urllib2
import time
import os.path

from urlparse import urlsplit



def url2name(url):
    return  os.path.basename(urlsplit(url)[2])

def download(url, path, localFileName = None):
    localName = url2name(url)
    req = urllib2.Request(url)
    r = urllib2.urlopen(req)
    if r.info().has_key('Content-Disposition'):
        # If the response has Content-Disposition, we take file name from it
        localName = r.info()['Content-Disposition'].split('filename=')[1]
        if localName[0] == '"' or localName[0] == "'":
            localName = localName[1:-1]
    elif r.url != url: 
        # if we were redirected, the real file name we take from the final URL
        localName = url2name(r.url)
    if localFileName: 
        # we can force to save the file as specified name
        localName = localFileName
    if  (not os.path.exists(path + localName+".added")) and (not os.path.exists(path + localName)) :
        f = open(path+localName, 'wb')
        f.write(r.read())
        f.close()
    else:
        print "El fichero {0} existe".format(localName)

def writeFile(texto, namefile):
    file = open(namefile, "w")
    file.write(texto)
    file.close()
    


#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from lxml import etree
import elemento


doc = "root"
registro = "reg"
fecharef = "fecharef"
item = "item"
fecha = "fecha"
nombre = "nombre"
descarga = "descarga"
origen = "origen"
basepath = "xmls/informe.xml"

'''
<root>
    <item>
        <fecha></fecha>
        <nombre></nombre>
        <descarga></descarga>
        <origen></origen>
    </item>
</root>
'''

def buildXML(lista, path = basepath):
    docElement = etree.Element(doc)
    fecha = etree.Element(fecharef)
    fecha.text = today()
    docElement.append(fecha)
    reg = etree.Element(registro)
    reg.text = str(len(lista))
    docElement.append(reg)
    for elemento in lista:
        docElement.append(additem(elemento))
    grabarFichero(etree.tostring(docElement, pretty_print=True), path);
    
    
def additem(elemento):
    element = etree.Element("item")
    element.append(addsubitem(fecha,elemento.fecha.strip()))
    element.append(addsubitem(nombre,elemento.nombre.strip()))
    element.append(addsubitem(descarga,elemento.descarga))
    element.append(addorigenelement(origen,elemento))
    return element


def addsubitem(subitem, value):
    element = etree.Element(subitem)
    element.text = value
    return element

def addorigenelement(subitem,value):
    element = etree.Element(subitem)
    oName = etree.Element("web")
    oName.text = value.origen.nombre
    element.append(oName)
    oEnlace = etree.Element("enlace")
    oEnlace.text = value.origen.enlace
    element.append(oEnlace)
    return element


def grabarFichero(texto, path):
    try:
        myXMLfile = open(path, 'w')
        myXMLfile.write(texto)
        myXMLfile.close()
        print "Fichero {0} generado".format(path)
    except Exception, ex:
        print "[ERROR]", ex


def today():
    x = datetime.datetime.now()
    return ("%s" % x)
    #return ("%s/%s/%s::%s:%s:%s" % (x.day, x.month, x.year,x.hour, x.month, x.second) )
        
    
'''
if __name__ == '__main__':
    
    lista = []
    for x in range(0, 5):
        item = elemento.elemento()
        item.nombre="mi {0} nombre".format(x)
        item.fecha="{0}".format(x)
        item.descarga="link {0}".format(x)
        item.origen="try"
        lista.append(item)
    print len(lista)

    
    buildXML(lista)
'''
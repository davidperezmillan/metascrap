#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lxml import etree
import elemento


doc = "root"
item = "item"
fecha = "fecha"
nombre = "nombre"
descarga = "descarga"
origen = "origen"
path = "xmls/informe.xml"

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

def buildXML(lista):
    docElement = etree.Element(doc)
    for elemento in lista:
        docElement.append(additem(elemento))
    grabarFichero(etree.tostring(docElement, pretty_print=True));
    
    
def additem(elemento):
    element = etree.Element("item")
    element.append(addsubitem(fecha,elemento.fecha.strip()))
    element.append(addsubitem(nombre,elemento.nombre.strip()))
    element.append(addsubitem(descarga,elemento.descarga))
    element.append(addsubitem(origen,elemento.origen.strip()))
    return element


def addsubitem(subitem, value):
    element = etree.Element(subitem)
    element.text = value
    return element

def grabarFichero(texto):
    try:
        myXMLfile = open(path, 'w')
        myXMLfile.write(texto)
        myXMLfile.close()
        print "Fichero {0} generado".format(path)
    except Exception, ex:
        print "[ERROR]", ex

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
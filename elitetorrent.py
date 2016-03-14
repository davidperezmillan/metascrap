#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import sys
import re

from lxml import html
from lxml import etree

from commun import ficheros
from commun import elemento
from commun import informe

from config.elitetorrent.logconfig import logger

urlfindnew = ["http://elitetorrent.net/categoria/17/peliculas-microhd/modo:listado", 
    "http://elitetorrent.net/categoria/13/peliculas-hdrip/modo:listado"]
max = 5

def build():
    
    lista = []
    
    for url in urlfindnew:
        listaparcial = []
        logger.info("URL %s"%(url))
        root = html.parse(url).getroot()
        tablas = root.xpath("//table[@class='fichas-listado']",
            namespaces={'re': "http://exslt.org/regular-expressions"})
        logger.debug("tabla(fichas-listado) %s"%(len(tablas[0])))  
        if len(tablas)>= 1:
            listaparcial = findnew(tablas[0])
        lista.extend(listaparcial)
    return lista

def findnew(tabla):
    lista = []
    rows = tabla.xpath("tr")
    logger.debug("Filas %s"%(len(rows)))
    contador = 0
    for row in rows:
        if contador >= max:
            break
        enlace = row.xpath("td[@class='nombre']/a[@class='icono-bajar boton']")
        nombre = row.xpath("td[@class='nombre']/a[@class='nombre']")
        fecha = row.xpath("td[@class='fecha']/text()",namespaces={'re': "http://exslt.org/regular-expressions"})[0]
        if nombre :
            logger.info(" %s --> %s  "%(nombre[0].text,fecha))
            archivoDescargar = 'http://elitetorrent.net{0}'.format(enlace[0].attrib['href'])
            item = elemento.elemento();
            item.nombre = nombre[0].text
            item.fecha = fecha
            item.descarga = archivoDescargar
            item.origen = "elitetorrent"
            lista.append(item)
        contador = contador + 1
    return lista
        
if __name__ == '__main__':
    informe.buildXML(build())

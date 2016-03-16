#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from lxml import html
from lxml import etree

from commun import ficheros
from commun import elemento
from commun import informe

from config.newpct1.logconfig import logger

urlBase = 'http://newpct1.com/series-hd/firefly/2330/pg/{0}'
paginacion = "1"
path = 'down/'

max = 50

ficheros.debug = False # True or False


def build (max=max, path=None):
    
    lista = []
    paginacion = 1
    while True: ## cuidado o montaremos un bucle infinito
        
        url = urlBase.format(paginacion)
        logger.info("URL %s"%(url))
        
        root = html.parse(url).getroot()
        ficheros.writeFile(etree.tostring(root, pretty_print=True),"response/newpct1_%s.html"%(paginacion))
        
        results = root.xpath("//ul[re:test(@class,'buscar-list')]/li",namespaces={'re': "http://exslt.org/regular-expressions"})
        
        if (len(results) <= 0):
            break;
            
        logger.debug("longitud del resultado {0}".format(len(results))) 
        
        
        for index in range(len(results)):
            result = results[index]
            
            ficheros.writeFile(etree.tostring(result, pretty_print=True),"response/newpct1_lista{%s_%s}.html"%(paginacion,index))
            
            item = elemento.elemento();
            
            nombre = result.xpath("div[re:test(@class,'info')]/a", namespaces={'re': "http://exslt.org/regular-expressions"})
            #criteria = nombre[0].xpath("h2/span[re:match(@text(),'^Es.*')]", namespaces={'re': "http://exslt.org/regular-expressions"}) if nombre else None
            if (nombre):
                name = nombre[0].get('title')
                
                #print etree.tostring(resul, pretty_print=True)
                enlace = result.xpath("a", namespaces={'re': "http://exslt.org/regular-expressions"})
                print "longitud del resultado enlace", len(enlace) 
                
                link =  enlace[0].attrib['href'] if len(enlace) >= 1  else None
                logger.info("-- %s --> %s" % (name,link))
                item.nombre = name;
                
                
                ## Primera pagina de descarga
                rootenlace = html.parse(link).getroot()
                ficheros.writeFile(etree.tostring(rootenlace, pretty_print=True),"response/newpct1_page{%s_%s}.html"%(paginacion,index))
                
                # f1-btn3
                enlaceDown = rootenlace.xpath("//a[re:test(@class,'f1-btn3')]", namespaces={'re': "http://exslt.org/regular-expressions"})
                #<span class="imp"><strong>Fecha:</strong> 09-03-2016</span>
                fecha = rootenlace.xpath("//span[@class='imp']/text()")[2]
                
                #print "longitud del resultado enlaceDown", len(enlaceDown)
                linkDown =  enlaceDown[1].attrib['href'] if len(enlace) >= 1  else None
                logger.debug("linkDown %s, %s" %(linkDown, fecha))
                item.fecha = fecha
                
                ## Segunda pagina de descarga
                rootenlace_2 = html.parse(linkDown).getroot()
                #ficheros.writeFile(etree.tostring(rootenlace_2, pretty_print=True),"response/newpct1_page{0}.html".format(contador))
                
                ### btn-torrent
                enlaceDown_2 = rootenlace_2.xpath("//a[re:test(@class,'btn-torrent')]", namespaces={'re': "http://exslt.org/regular-expressions"})
        
                #print "longitud del resultado enlaceDown", len(enlaceDown)
                linkDown_2 =  enlaceDown_2[0].attrib['href'] if len(enlace) >= 1  else None
                
                logger.debug("linkDown2 %s" %(linkDown_2))
                item.descarga = linkDown_2
        
                ficheros.download(linkDown_2,path) if path else None
                
                item.origen = item.origen("newpct1",url)
                lista.append(item)

        paginacion = paginacion + 1
    return lista;
    
if __name__ == '__main__':
    informe.buildXML(build(max, path), "xmls/infomefirefly.xml")

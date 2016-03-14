#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from lxml import html
from lxml import etree

#from commun import ficheros
from commun import elemento
from commun import informe

url = 'http://newpct1.com/peliculas'
max = 50


def build ():
    
    lista = []
    
    '''
    enlace = result.xpath("a[re:test(@href, '^/torrent')]",
    namespaces={'re': "http://exslt.org/regular-expressions"})
    '''

    root = html.parse(url).getroot()
    #ficheros.writeFile(etree.tostring(root, pretty_print=True),"response/newpct1.html")
    result = root.xpath("//ul[re:test(@class,'pelilist')]/li",namespaces={'re': "http://exslt.org/regular-expressions"})
    
    print "longitud del resultado ", len(result) 
    
    contador = 0
    for resul in result:
        if contador >= max:
            break
        item = elemento.elemento();
        
        nombre = resul.xpath("a/h2", namespaces={'re': "http://exslt.org/regular-expressions"})
        name = nombre[0].text
        
        #print etree.tostring(resul, pretty_print=True)
        enlace = resul.xpath("a", namespaces={'re': "http://exslt.org/regular-expressions"})
        #print "longitud del resultado enlace", len(enlace) 
        
        link =  enlace[0].attrib['href'] if len(enlace) >= 1  else None
        print "--",name , "--> ",link
        item.nombre = name;
        
        
        ## Primera pagina de descarga
        rootenlace = html.parse(link).getroot()
        #ficheros.writeFile(etree.tostring(rootenlace, pretty_print=True),"response/newpct1_page{0}.html".format(contador))
        # f1-btn3
        enlaceDown = rootenlace.xpath("//a[re:test(@class,'f1-btn3')]", namespaces={'re': "http://exslt.org/regular-expressions"})
        #<span class="imp"><strong>Fecha:</strong> 09-03-2016</span>
        fecha = rootenlace.xpath("//span[@class='imp']/text()")[2]
        
        #print "longitud del resultado enlaceDown", len(enlaceDown)
        linkDown =  enlaceDown[0].attrib['href'] if len(enlace) >= 1  else None
        print "linkDown",linkDown, fecha
        item.fecha = fecha
        
        ## Segunda pagina de descarga
        rootenlace_2 = html.parse(linkDown).getroot()
        #ficheros.writeFile(etree.tostring(rootenlace_2, pretty_print=True),"response/newpct1_page{0}.html".format(contador))
        
        ### btn-torrent
        enlaceDown_2 = rootenlace_2.xpath("//a[re:test(@class,'btn-torrent')]", namespaces={'re': "http://exslt.org/regular-expressions"})

        #print "longitud del resultado enlaceDown", len(enlaceDown)
        linkDown_2 =  enlaceDown_2[0].attrib['href'] if len(enlace) >= 1  else None
        print "linkDown2",linkDown_2
        item.descarga = linkDown_2
        #ficheros.download(linkDown_2, "response/")
        item.origen = "newpct1"
        lista.append(item)
        
        contador = contador + 1
    
    return lista;
    
    
if __name__ == '__main__':
    informe.buildXML(build())

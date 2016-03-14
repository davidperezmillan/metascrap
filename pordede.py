#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import requests 
from lxml import html
from lxml import etree 
from lxml import builder  
import datetime
import re
import sys

## propios
from config.pordede.logconfig import logger
from commun import ficheros
from commun import scrapping
#from resource import informexml
from config.pordede import config
from config.pordede import pattern


doc = etree.Element("pordede")


## UTILES
def decodeHtmlentities(string):
    string = entitiesfix(string)
    entity_re = re.compile("&(#?)(\d{1,5}|\w{1,8});")

    def substitute_entity(match):
        from htmlentitydefs import name2codepoint as n2cp
        ent = match.group(2)
        if match.group(1) == "#":
            return unichr(int(ent)).encode('utf-8')
        else:
            cp = n2cp.get(ent)

            if cp:
                return unichr(cp).encode('utf-8')
            else:
                return match.group()
                
    return entity_re.subn(substitute_entity, string)[0]
    
def entitiesfix(string):
    # Las entidades comienzan siempre con el símbolo & , y terminan con un punto y coma ( ; ).
    string = string.replace("&aacute","&aacute;")
    string = string.replace("&eacute","&eacute;")
    string = string.replace("&iacute","&iacute;")
    string = string.replace("&oacute","&oacute;")
    string = string.replace("&uacute","&uacute;")
    string = string.replace("&Aacute","&Aacute;")
    string = string.replace("&Eacute","&Eacute;")
    string = string.replace("&Iacute","&Iacute;")
    string = string.replace("&Oacute","&Oacute;")
    string = string.replace("&Uacute","&Uacute;")
    string = string.replace("&uuml"  ,"&uuml;")
    string = string.replace("&Uuml"  ,"&Uuml;")
    string = string.replace("&ntilde","&ntilde;")
    string = string.replace("&#191"  ,"&#191;")
    string = string.replace("&#161"  ,"&#161;")
    string = string.replace(";;"     ,";")
    return string



def main(parametro):
    session_requests = requests.session()
    
    xml_fecha_inicio = etree.Element("inicio")
    
    fecha_inicio = datetime.datetime.now()
    xml_fecha_inicio.text = fecha_inicio.isoformat()
    doc.append(xml_fecha_inicio);
    logger.info("Inicio de la aplicacion = %s" % fecha_inicio.isoformat())
    
    # Hacemos login
    login(session_requests);
    
    # recuperamos las series 
    bucket_elems = getListSeries(session_requests)
   
    if not bucket_elems: 
        return None
    
    # recuperamos info serie
    texto = getAllSeries(session_requests, bucket_elems, parametro)
   
   
    
    fecha_fin = datetime.datetime.now()
    logger.info("fin de la Aplicacion = %s" % fecha_fin.isoformat())
    # grabamos el fichero xml
    if texto is not None:
        grabarFichero(texto);
    
    
    
    #for seasons in seasons_elems:
    #    print seasons.text_content();
    #    chapters = seasons.findall(".//div[@class='modelContainer defaultPopup']/div[1]/span/span")
        #chapters_elem = [chapters.text_content().replace("\n", "").strip() for chapters_elem in chapters]
        #print chapters_elem
    
def grabarFichero(texto):
    try:
        myXMLfile = open(config.file_informe, 'w')
        myXMLfile.write(texto)
        myXMLfile.close()
        logger.info("Fichero "+config.file_informe+" generado")
    except Exception, ex:
        logger.error("[ERROR]")
        logger.error(ex)

def login(session_requests):
    # Get login csrf token
    """
    result = session_requests.get(LOGIN_URL)
    tree = html.fromstring(result.text)
    authenticity_token = list(set(tree.xpath("//input[@name='csrfmiddlewaretoken']/@value")))[0]
    """

    # Create payload
    payload = {
        "LoginForm[username]": config.USERNAME, 
        "LoginForm[password]": config.PASSWORD, 
       # "csrfmiddlewaretoken": authenticity_token
    }

    # Perform login
    result = scrapping.geturlpost(session_requests,config.LOGIN_URL,  payload, dict(referer = config.LOGIN_URL))


def getListSeries(session_requests):
    # Scrape url
    result = scrapping.geturlget(session_requests, config.URL, None, dict(referer = config.URL))
    # print result.content

    tree = html.fromstring(result.content)
    #<span class="title">
    bucket_elems = tree.findall(pattern.pattern_listseries)
   
    
    return bucket_elems
   

def getAllSeries(session_requests, bucket_elems, parametro):
    
    #bucket_names = [bucket_elem.get('href').strip() for bucket_elem in bucket_elems]

    # Bucle de Series 
    for bucket_elem in bucket_elems: 
    
        try:
            serie = bucket_elem.get('href').strip()
            url_serie = config.BASE_URL+serie
            result = scrapping.geturlget(session_requests,decodeHtmlentities(url_serie), None, dict(referer = decodeHtmlentities(url_serie)))
            #ficheros.writeFile(result.content)
            
            tree = html.fromstring(result.content)
            serie_name = tree.find(pattern.pattern_seriename).text
            
            xml_serie = etree.Element("serie")
            xml_serie.attrib["name"]=serie_name
    
            
            seasons_elems = tree.findall(pattern.pattern_listsesson)
            # bucle de temporadas
            for seasons in seasons_elems:
                #seasons1 = seasons_elems[0]
                seasons_name = seasons.find(pattern.pattern_nameSesson).text.strip()
            
                #print seasons_name
                
                xml_season = etree.Element("season")
                xml_season.attrib["name"]=seasons_name
                
                chapters_elems = seasons.findall("div[@class='modelContainer defaultPopup']")
                for chapters in chapters_elems:
                    #chapters1 = chapters_elems[0]
                    
                    title = chapters.find(pattern.pattern_infochapters)
                    chapters_name = title.find("span").text
                    chapters_id = title.find("span/span").text if title.find("span/span") is not None else 'No Definido'
                    #chapters_id = title.find("span/span").text
                    chapters_status = chapters.find(pattern.pattern_statuschapters)
                    status = chapters_status is not None
                    
                    """
                    print seasons_name
                    print chapters_id 
                    print chapters_name 
                    print status
                    print "---- EOC ----"
                    """
                    if False == parametro:
                       if False == status:
                        xml_chapter = etree.Element("chapter")
                        # nombre
                        xml_name = etree.Element("name")
                        xml_name.text = chapters_name
                        xml_chapter.append(xml_name)     
                        # id
                        xml_id = etree.Element("id")
                        xml_id.text = seasons_name + " X " +chapters_id
                        xml_chapter.append(xml_id)
                        # status
                        xml_chapter.attrib["status"] = str(status)
                        xml_season.append(xml_chapter)
                        break
                    else:
                        xml_chapter = etree.Element("chapter")
                        # nombre
                        xml_name = etree.Element("name")
                        xml_name.text = chapters_name
                        xml_chapter.append(xml_name)     
                        # id
                        xml_id = etree.Element("id")
                        xml_id.text = seasons_name + " X " +chapters_id
                        xml_chapter.append(xml_id)
                        # status
                        xml_chapter.attrib["status"] = str(status)
                        xml_season.append(xml_chapter)
                    
                
                # print "---- EOS ----"
                xml_serie.append(xml_season)  
        
            doc.append(xml_serie)
        except Exception, ex:
            logger.error("[ERROR]")
            logger.error(ex)
            
    
    logger.info("Scrapping finalizado")
    
    xml_fecha_fin = etree.Element("fin")
    fecha_fin = datetime.datetime.now()
    xml_fecha_fin.text = fecha_fin.isoformat()
    doc.append(xml_fecha_fin);
    
    logger.info("fin de la Scrapping = %s" % fecha_fin.isoformat())
    return etree.tostring(doc, pretty_print=True)

if __name__ == '__main__':
    parametro = ((True if sys.argv[1]=='-all' else False) if len(sys.argv) >= 2 else False)
    main(parametro)

    
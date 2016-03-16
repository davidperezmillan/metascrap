#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
import logging
import logging.handlers
import config
 
# Creamos una instancia al logger con el nombre especificado
logger=logging.getLogger(__name__)

 
# Indicamos el nivel máximo de seguridad para los mensajes que queremos que se
# guarden en el archivo de logs
# Los niveles son:
#   DEBUG - El nivel mas alto
#   INFO
#   WARNING
#   ERROR
#   CRITIAL - El nivel mas bajo
logger.setLevel(logging.DEBUG)

''' 
# Creamos una instancia de logging.handlers, en la cual vamos a definir el nombre
# de los archivos, la rotación que va a tener, y el formato del mismo
 
# Si maxBytes=0, no rotara el archivo por tamaño
# Si backupCount=0, no eliminara ningún fichero rotado
handler = logging.handlers.RotatingFileHandler(filename=config.file_log, mode='a', maxBytes=10240, backupCount=5)
 
# Definimos el formato del contenido del archivo de logs
formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',datefmt='%y-%m-%d %H:%M:%S')
# Añadimos el formato al manejador
handler.setFormatter(formatter)
 
# Añadimos el manejador a nuestro logging
logger.addHandler(handler)
''' 


handler_consola = logging.StreamHandler()
handler_consola.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(levelname)s - %(message)s")
#formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',datefmt='%y-%m-%d %H:%M:%S')
handler_consola.setFormatter(formatter)
logger.addHandler(handler_consola)

'''
handler = logging.handlers.RotatingFileHandler(filename=config.file_log, mode='a', maxBytes=10240, backupCount=5)
handler.setLevel(logging.INFO)
formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',datefmt='%y-%m-%d %H:%M:%S')
handler.setFormatter(formatter)    
logger.addHandler(handler)
'''

'''
# Añadimos mensajes al fichero de log
logger.debug('message debug')
logger.info('message info')
logger.warning('message warning')
logger.error('message error')
logger.critical('message critical')
'''
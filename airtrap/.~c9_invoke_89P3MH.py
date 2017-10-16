#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
import importlib
import logging
from logging.handlers import RotatingFileHandler
import argparse

from handler.data.databaseairtrap import DatabaseAirTrap

basepathlog = 'logs/'
loggername = 'airtrapdata'
defaulformatter = "%(asctime)s [%(levelname)s] - %(name)s - %(filename)s:%(lineno)d - %(message)s"
loggerfilename = basepathlog+loggername+'.log'


def getOperaciones(clazz=None):
    operaciones={'create':None, 'insert':None, 'select':None, 'truncate':None, 'update':None}
    if clazz is not None:
        for method_name in operaciones:
            try: 
                operaciones[method_name]=getattr(clazz, method_name)
            except:
                continue
    return operaciones


def proccesArgs():
    operaciones = getOperaciones()
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument('mode',  choices=operaciones, help="Define la operacion a realizar")
    parser.add_argument('-serie', nargs="+")
    
    # Podemos hacer que este argumento no sea obligatorio
    # parser.add_argument('mode',  action='store_const', const='check')
    
    # parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS, help='Mostrar este mensaje de ayuda y salir.')
    parser.add_argument("-v", "--verbose", help="Mostrar información de depuración", action="store_true")
    parser.add_argument("-t", "--test", help="No ser realizaran acciones [modo test]", action='store_true', default=False)
    parser.add_argument("--cron", help="Se define los parametros para ser lanzado", action="store_true")
    # parser.add_argument("-c", "--config", help="Definimos archivo de configuracion", default="config/config.json")
    parser.add_argument("--loglevel", help="Definimos el nivel de logs", default="DEBUG", choices=['DEBUG','debug','INFO','info','WARN', 'warn','ERROR', 'error'])
    parser.add_argument("--logfile", help="Definimos archivo de log", default=loggerfilename)
    
    # # Recuperamos las tareas, segun el parametro pasado anteriormente
    # parser.add_argument("--task", help="Define las tareas a realizar", nargs='+')
    
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')
    
    args = parser.parse_args()
    
    if args.test:
        args.loglevel="DEBUG"
    
    if args.cron:
        args.loglevel="INFO"

    return args


def buildlogger(args):
    global logger
    logger = logging.getLogger(loggername)
    logger.setLevel(logging.getLevelName(args.loglevel.upper()))
    formatter = logging.Formatter(defaulformatter)
    
    # handler = logging.FileHandler(mcbconstants.basepathlog+"mycrylog.out")
    handler = RotatingFileHandler(args.logfile, maxBytes=20000, backupCount=5)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)        
    logger.addHandler(ch)
    return logger

def listItems(response):
    for item in response:
        logger.info("tilte: %s -- episode: %s", item.title, item.epstart)
    


if __name__ == '__main__':
    
    args=proccesArgs()
    logger=buildlogger(args)
    logger.debug("Argumentos pasados %s",args)
    
    database="handler/data/followingseries.sqlite3"
    handler = DatabaseAirTrap(database, logger=logger)
    operaciones = getOperaciones()
    logger.debug(args.mode)
    if args.mode == "create":
        logger.debug("create:%s",args.mode)
        handler.create()
    if args.mode == "update":
        logger.debug("update:%s",args.mode)
        handler.update(args.serie[0], args.serie[1] if len(args.serie)>1 else "NRS00E00")
        logger.debug("select:%s",args.mode)
        listItems(handler.select("SELECT ROWID,* FROM SERIES;"))
    if args.mode == "insert": 
        logger.debug("insert:%s",args.mode)
        handler.insert(args.serie[0], args.serie[1] if len(args.serie)>1 else "NRS00E00")
    if args.mode == "select":
        logger.debug("select:%s",args.mode)
        listItems(handler.select("SELECT ROWID,* FROM SERIES;"))
    if args.mode == "truncate":
        logger.debug("truncate:%s",args.mode)
        handler.truncate()
    
        
    







































































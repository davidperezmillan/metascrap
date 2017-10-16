#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import logging
from logging.handlers import RotatingFileHandler
from prettytable import PrettyTable
import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from beans.databeans import ChatIdEntry, series

import conf.constantes as cons
 
basepathlog = cons.basepathlog
loggername = 'airtrap'
defaulformatter = "%(asctime)s [%(levelname)s] - %(name)s - %(filename)s:%(lineno)d - %(message)s"
loggerfilename = basepathlog+loggername+'.log'
Base = declarative_base() 
 
  
databaseDefaultName = "{0}/conf/data/followingseries.sqlite3".format(cons.basepath)

class DatabaseAirTrap(object):   
    
    
    def __init__(self, databaseName=databaseDefaultName, logger=None):
    
        self.databaseName = databaseName
        
        if (logger):
            self.logger = logger
        else:
            self.logger = logging.getLogger(loggername)
            self.logger.setLevel(logging.DEBUG)
            self.formatter = logging.Formatter(defaulformatter)
        
            # self.handler = RotatingFileHandler(loggerfilename, maxBytes=2000, backupCount=3)
            # self.handler.setFormatter(self.formatter)
            # self.logger.addHandler(self.handler)
            
            self.ch = logging.StreamHandler()
            self.ch.setFormatter(self.formatter)        
            self.logger.addHandler(self.ch)
        
        self.engine = create_engine('sqlite:///{0}'.format(self.databaseName))
        self.session = sessionmaker()
        self.session.configure(bind=self.engine)
        Base.metadata.create_all(self.engine)      

    

    def __display(self, tabla, statement):
    
        col_names = tabla.columns.keys()
        x = PrettyTable(col_names)
        for c in col_names:
            x.align[c] = 'l'
        x.padding_width = 2    
        for row in statement:
            fields = []
            for field in tabla.columns.keys():
                fields.append(getattr(row,field.lower()) or "")
            x.add_row(fields)
            
        tabstring = x.get_string()
        return tabstring
    
    
        
    def insert(self,serie, episode):
        try:
            s= self.session()
            serie = series(nombre=serie,quality=episode[:2], ep=episode)
            response = s.add(serie)
            s.commit()
            return response
            # self.select_all(True)
        except Exception as error:
            self.logger.error("Error al insert la tabla [%s]",error)
    
    def update(self, serie, episode):
        try:
            s=self.session()
            response = s.query(series).filter(series.nombre==serie).update({series.ep:episode, series.quality:episode[:2], series.ultima:datetime.datetime.now()})
            s.commit()
            return response
            # self.select_all(False)
        except Exception as error:
            self.logger.error("Error al update la tabla [%s]",error)
            
    def delete(self, serie=None, quality="NR", id=None):
        try:
            s=self.session()
            response = s.query(series).filter(series.nombre==serie, series.quality==quality).delete()
            s.commit()
            return response
        except Exception as error:
            self.logger.error("Error al delete de un registro [%s]",error)
    
    def truncate(self):
        try:
            s=self.session()
            statements = ["DELETE FROM SERIES;", "VACUUM;"]
            for statement in statements:
                s.execute(statement)
            s.commit()
        except Exception as error:
            self.logger.error("Error al vaciar la tabla [%s]",error)
    
    
    def view_chat_ids(self, display=False):
        try:    
            s= self.session()
            statement = s.query(ChatIdEntry).all()
            print self.__display(ChatIdEntry.metadata.tables['telegram_chat_ids'], statement ) if display else "No hay representacion grafica" 
            return statement
        except Exception as error:
            self.logger.error("Error al view_chat_ids la tabla [%s]",error)
    
    
    
    def select_all(self, display=False):
        try:    
            s= self.session()
            statement = s.query(series).all()
            print self.__display(series.metadata.tables['SERIES'], statement ) if display else "No hay representacion grafica" 
            return statement
        except Exception as error:
            self.logger.error("Error al selectAll la tabla [%s]",error)


    def select(self, display=False):
        return self.select_all(display)



    
    


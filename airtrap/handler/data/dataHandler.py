#!/usr/bin/env python
# -*- coding: utf-8 -*-
from beans.pluginsBeans import RequestPlugin
from beans.pluginsBeans import ResponsePlugin

from handler.data.databaseairtrap import DatabaseAirTrap


def getMockData():
    lrequest = [
            # RequestPlugin(title="Midnight Texas"), 
            RequestPlugin(title="Killjoys", epstart="NRS03E00"),
            RequestPlugin(title="La Vida en Piezas", epstart="HDS02E04")
        ]
    return lrequest
    
    
def getdatabase(logger=None, skip=False):
        # databaseName="handler/data/followingseries.sqlite3"
        database=DatabaseAirTrap(logger=logger)
        lobjData = database.select_all()
        response = []
        for objData in lobjData:
            response.append(RequestPlugin(title=objData.nombre, epstart=objData.ep_start, epend=objData.ep_end))
        return response
    
    
def convertArgsBean(args):
    serie = args.serie or None;
    if len(serie)>2:
        return [RequestPlugin(title=serie[0], epstart=serie[1], epend=serie[2])]
    if len(serie)>1:
        return [RequestPlugin(title=serie[0], epstart=serie[1])]
    return [RequestPlugin(title=serie[0])]
    

def convertArgsBeanFilm(args):
    film = args.film or None;
    if len(args.film)>1:
        return [RequestPlugin(title=film[0], quality=film[1])]
    return [RequestPlugin(title=film[0])]    
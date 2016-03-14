#!/usr/bin/env python
# -*- coding: utf-8 -*-

import newpct1
import elitetorrent
from commun import informe
from config.logconfig import logger

max = 10
path =None

if __name__ == '__main__':
    lista = []
    lista.extend(elitetorrent.build(max, path))
    lista.extend(newpct1.build(max, path))
    informe.buildXML(lista)
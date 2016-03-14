#!/usr/bin/env python
# -*- coding: utf-8 -*-

import newpct1
import elitetorrent
from commun import informe

max = 10

if __name__ == '__main__':
    lista = []
    lista.extend(newpct1.build(max))
    lista.extend(elitetorrent.build(max))
    informe.buildXML(lista)
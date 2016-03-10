#!/usr/bin/env python
# -*- coding: utf-8 -*-

import newpct1
import elitetorrent
from commun import informe


if __name__ == '__main__':
    lista = []
    lista.extend(newpct1.build())
    lista.extend(elitetorrent.build())
    informe.buildXML(lista)
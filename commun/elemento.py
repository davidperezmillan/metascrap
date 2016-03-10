#!/usr/bin/env python

class elemento:
    
    '''
    <root>
        <item>
            <fecha></fecha>
            <nombre></nombre>
            <descarga></descarga>
            <origen></origen>
        </item>
    </root>
    '''
    fecha = ""
    nombre = ""
    descarga = ""
    origen = ""

    #def init(self):


if __name__ == '__main__':
    
   
    
    lista = []
    for x in range(0, 5):
        item = elemento()
        item.nombre="mi {0} nombre".format(x)
        lista.append(item)
    print len(lista)
    for i in lista:
        print i.nombre


#!/usr/bin/env python

'''
<root>
    <item>
        <fecha></fecha>
        <nombre></nombre>
        <descarga></descarga>
        <origen>
            <nombre></nombre>
            <enlace></enlace>
        </origen>
    </item>
</root>
'''


class elemento:
    class origen:
        nombre = ""
        enlace = ""
        def __init__(self, nombre=None, enlace = None):
            self.nombre=nombre
            self.enlace=enlace
    
    fecha = ""
    nombre = ""
    descarga = ""
    
    def __init__(self):
        """ Constructor for the class elemento """
        origen = self.origen()
    
    def __str__(self):
        return "Nombre: %s :: origen.nombre: %s :: origen.enlace: %s"%(self.nombre,self.origen.nombre, self.origen.enlace)

    #def init(self):


if __name__ == '__main__':
    
   
    
    lista = []
    for x in range(0, 5):
        item = elemento()
        item.nombre="mi {0} nombre".format(x)
        item.origen= item.origen("mi {0} nombre".format(x), "mi {0} enlace".format(x))
        lista.append(item)
    print len(lista)
    for i in lista:
        print str(i)


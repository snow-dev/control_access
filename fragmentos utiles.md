##### Busqueda en un diccionario y campara valores para determianr la existencia o no de la clave valor en cuestion


```PYTHON

#!usr/bin/python

########################################
#    By: Kharl                          #
#    Copyleft: Creative Commons         #
#    Usa, modifica, distribuye          #
#    y no olvides referenciar.          #
#    El mundo es de los lo contruyen!!  #
########################################

usrMaquina = {}

for x in range(1,54):
    pc = 'PC_' + str(x)
    #print(pc)
    usrMaquina[x] = 0
    pass

usrMaquina[1] = 11590163
usrMaquina[23] = 11590198

nMaquina = int(input('ingrese maquina >>> '))
nControl = int(input('Ingrese numero de control >>> '))

print('\n')
print(usrMaquina)
print('\n')

for mq, usr in usrMaquina.items():
    if mq == nMaquina and usr == nControl:
        print('Maquina %d ocupada por el Usuario %d' %(nMaquina, usrMaquina.get(nMaquina)))
        print('Liberando maquina %d' %nMaquina)
        usrMaquina[nMaquina] = 0
        break
        pass
    elif mq == nMaquina and usr == 0:
        print('Maquina %d libre' %mq)
        usrMaquina[nMaquina] = nControl
        #print(nMaquina, ':', usr)
        pass
    elif mq == nMaquina and usr != nControl:
        print('Maquina %d ocupada!' %nMaquina)
    pass

print('\n', usrMaquina)

```
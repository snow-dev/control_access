#!usr/bin/python

########################################
#   By: K                              #
#   Copyleft: Creative Commons         #
#   Usa, modifica, distribuye          #
#   y no olvides referenciar.          #
#   El mundo es de los geeks!!         #
########################################

import sys
from PyQt6 import QtCore
from PyQt6 import QtGui
from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow

# Cargamos la interfaz de usuario

from registro import Ui_Usuario
from modulos.conexion import Conectar

# Importamos el modulode validacion.

from modulos.validar import Validar
# Importamos el modulo Escanner
# from modulos.escanner import Escanner
# Importamos la clase Hora, que nos regresara la fecha y hora actual.
from modulos.fecha import Tiempo


#################################################################
# Clase de inicializacion del modulo, se carga la interfaz      #
# y se conectan los eventos de los botones con sus respectivas  #
# funciones.                                                    #
#################################################################

class Registro(QMainWindow, Ui_Usuario):
    """docstring for Registro"""

    def __init__(self, *args, **kwargs):

        super(Registro, self).__init__(*args, **kwargs)

        self.setupUi(self)

        self.nControl.textChanged.connect(self.validarControl)
        # self.bIngresar.setEnabled(False)
        # self.textEdit.appendPlainText("\nSending a remote call to myFunction()...")
        self.plainLog.appendPlainText('Inicializando el sistema :)')
        self.plainLog.appendPlainText('Sistema listo...\n\n')

        # Configuraciones para el reloj
        self.tiempoActual = QtCore.QTime(0, 0, 0)
        self.reloj.display(self.tiempoActual.toString('hh:mm:ss'))
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.actualizarReloj)
        self.timer.start(1000)

        self.libres = []
        self.ocupadas = []
        self.labels = []

        for x in range(1, 54):
            self.libres.append(x)
            self.labels.append('PC_' + str(x))
            pass
        # print(self.labels)

        # Usamos un diccionario para controlar quienes estan usando cierta maquina,
        # y si esta esta libre u ocupada
        # para ello usamos un diccionario PC_XX : nControl, odnde cada PC esta asignada 
        # a un usuario en cierto momento.

        self.pcUser = {}

        # LLenamos le diccionario, donde el valor sera 0 para todas las maquinas.
        for x in range(1, 54):
            self.pcUser[x] = 0
            pass

        # conexion = serial.Serial('/dev/ttyUSB0', baudrate = 9600, timeout = 1.0)

        # Conectamos los eventos de los botones con sus respectivas 
        # funciones

        pass

    #################################################################
    # Mostramos la hora actual en el QLCDNumber                     #
    #################################################################
    def actualizarReloj(self):

        obtener = Tiempo()
        hora = obtener.hora()
        self.reloj.setDigitCount(8)
        self.reloj.display(hora)
        pass

    #################################################################
    # Realizamos la validacion del numero de control                #
    #################################################################
    def validarControl(self):
        # Obtenemos el texto del QLineEdit, nControl
        lineControl = self.nControl.text()

        # Revisamos que la cadena de caracteres se corresponda con la longitud
        # de un numero de control, cuando se cumple , se llama a verificarControl

        if len(lineControl) == 8:
            revisar = Validar()
            resultado = revisar.verificarControl(lineControl)
            if (resultado == True):
                print('\tNumero de control %s valido \n' % str(lineControl))
                self.plainLog.appendPlainText('\t\n\nNumero de control %s valido' % str(lineControl))
                self.plainLog.appendPlainText(
                    '-------------------------------------------------------------------------')
                # Ya que se ha verificado nControl, se obtiene la informacion
                # realcionadoa a dicho valor
                self.obtenerUsuario(lineControl)
                pass
            elif (resultado == False):
                print('\tNumero de control no valido!!')
                self.plainLog.appendPlainText('\tNumero de control no valido!!')
                self.plainLog.appendPlainText(
                    '-------------------------------------------------------------------------')

            pass
        pass

    #################################################################
    # Obtenemos los datos del alumno en base a su nume`ro de control #
    #################################################################
    def obtenerUsuario(self, nControl):

        # Instanciamos la clase Conectar
        llamar = Conectar()

        # Preparamos la consulta a realizar, en este caso los datos relacionados
        # al numeri de control introducido
        sentencia = "select nombre, pApellido, mApellido, carrera from alumnos where nControl = %d;" % int(nControl)

        print(sentencia)

        # Se llama a la funcion de condulta de la clase Conectar y pasamos
        # la consulta como parametro.
        resultado = llamar.consulta(sentencia)

        print(resultado)

        ''' Si bien se podria hacer de otra forma, como en este caso simplemente asignamos
        los resultados de la consulta a los campos correspondientes, es rapido y directo.
        '''
        if resultado:
            self.nombre.setText(resultado[0][0])
            self.apellidos.setText(resultado[0][1] + ' ' + resultado[0][2])
            self.carrera.setText(resultado[0][3])

            self.imagen.setPixmap(QtGui.QPixmap("./imagenes/resized/%s.jpg" % str(nControl)))

            # Eliminamos el contendo para evitar basura posterior
            resultado = ''

            # Cambiamos el cursor al campo de numero de maquina
            self.maquina.setFocus()
        else:
            print("No se encontro el alumno!: ", resultado)

    #################################################################
    # Obtenemos id_entrada y el numero de control                   #
    #################################################################
    def datosSalida(self, nMaquina, nControl):
        # Instanciamos la casle Conectar

        llamar = Conectar()

        # Preparamos la consulta
        sentencia = "select id_entrada as ID, nMaquina as Maquina, nControl as Control  from entrada where nControl = %d and nMaquina = %d;" % (
            nControl, nMaquina)
        resultado = llamar.consulta(sentencia)
        ultimo = len(resultado)

        idEntrada = resultado[ultimo - 1][0]
        maquina = resultado[ultimo - 1][1]
        control = resultado[ultimo - 1][2]

        print('ID: %s, Maquina %s, Control %s' % (idEntrada, maquina, control))

        datos = self.recolectarDatos()

        if nMaquina == maquina and nControl == control:
            print('Los datos conciden :)')
            sentencia = "INSERT INTO salida(id_entrada, nControl, fSalida, hSalida) VALUES(%d, %d, '%s', '%s')" % (
                idEntrada, control, datos[2], datos[3])
            intentar = Conectar()
            ok = intentar.insertar(sentencia)
            # Si se ha insertado correctamente limpiamos los campos, en caso contrario se avisa al usuario
            # y al encargado, se limpian los for
            if ok == True:
                print('Registro de salida exitoso :)')
                self.plainLog.appendPlainText('Registro de salida exitoso!!')

                # Limpiamos los campos
                self.limpiarCampos(0)
                pass
            elif ok == False:
                print('No se puedo registar la salida, checar problemas!!')
                self.plainLog.appendPlainText('No se pudo registar la salida,\nContacte con el encargado.')
                self.limpiarCampos(0)
                pass

            pass
        pass

    #################################################################
    # Validar numero de                                             #
    #################################################################
    def validarMaquina(self):

        # Obtenemos el texto del QLineEdit
        nMaquina = self.maquina.text()
        nControl = self.nControl.text()

        # Instanciamos la clase Validar
        opcion = Validar()
        # Hora validamos que posea una sintaxis valida
        # Usamos la instanciasion previa de la clase Validar
        # Obtenemos el rasultado de validarMaquina
        resultado = opcion.verificarMaquina(nMaquina)
        if resultado == True:
            Maquina = int(nMaquina)
            Control = int(nControl)

            # Revisamos si esta ocupada o no
            if (resultado == True and int(Maquina) <= int(len(self.libres))):

                for pc, usr in self.pcUser.items():

                    # Si el la la clave es igual a la Maquina y el valor a Control
                    # es por que la maquina esta ocupada
                    if pc == Maquina and usr == Control:
                        print('Maquina %s ocupada por  el usuario %s' % (Maquina, Control))
                        print('Liberada exitosamente :)')
                        self.plainLog.appendPlainText('Maquina %s ocupada por  el usuario %s' % (Maquina, Control))
                        self.plainLog.appendPlainText('Maquina %d Liberada exitosamente :)' % Maquina)

                        self.datosSalida(Maquina, Control)

                        # Liberamos  la maquina y le asignamos 0 al valor de la clasve
                        self.pcUser[Maquina] = 0

                        # Actualizamos el mapa
                        self.mapa(str(Maquina), 1)

                        # retornamos  True a esValida0
                        return
                        pass
                    # Si el pc = Maquina y usr = 0, es que la maquina esta libre
                    elif pc == Maquina and usr == 0:
                        print('\tMAaquina %s libre' % pc)
                        print('\tNumero de maquina valido')
                        self.plainLog.appendPlainText('\tMaquina %d valida.' % Maquina)

                        # Agregamos la Maquina al diccionario de maquinas ocupadas
                        self.pcUser[Maquina] = Control

                        # Cambiamos la maquina a N/D
                        self.mapa(str(Maquina), 0)

                        # retornamos  False a esValida
                        return False
                        pass

                    # Si la pc = Maquina y usr != Control, es que la maquina esta ocupada
                    # notese que no se comapra contre el Control introducido.
                    elif pc == Maquina and usr != Control:
                        print('Maquinaaaa %s ocupada' % Maquina)
                        self.plainLog.appendPlainText('Maquinaaaa %s ocupada' % Maquina)
                        return True
                    pass
                pass
            elif (resultado == True and int(Maquina) > int(len(self.libres))):
                print('\tEsta maquina aun no existe, :P!!')
                self.plainLog.appendPlainText('\tEsta maquina aun no existe :P!!')
                return True
                pass
            pass
        elif (resultado == False):
            print('\t Ups, creo eso no es un numero :}- \t Intenta nuevamente :)')
            self.plainLog.appendPlainText('\t Ups, creo que eso no es un numero :}- \n Intenta nuevamente :)')
            # Si el resultado es falso, ponemos el cursor sobre el TextEdit de maquina
            self.limpiarCampos(1)
            pass
        pass

    #################################################################
    # Marcamos la maquina como no dosponible en el mapa             #
    #################################################################
    def mapa(self, nMaquina, opcion):
        pc = 'PC_' + nMaquina

        # Marcamos la maquina como no disponible
        if opcion == 0:
            self.__dict__[pc].setText('N/D')
            pass
        # Regresamos el numero a la maquina
        elif opcion == 1:
            self.__dict__[pc].setText(nMaquina)
            pass

        pass

    #################################################################
    # Realizamos una insercion                                      #
    #################################################################
    def recolectarDatos(self):
        print('\tRecolectando datos de registro :)!')
        self.plainLog.appendPlainText('\tRecolectando datos de registro')
        self.plainLog.appendPlainText('-----------------------------------------------------------------------')
        # Obtenemos la hora y la fecha de la clase Tiempo
        datos = []

        obtener = Tiempo()

        control = self.nControl.text()
        datos.append(int(control))

        maquina = self.maquina.text()
        datos.append(int(maquina))

        dia = obtener.fecha()
        datos.append(dia)

        hora = obtener.hora()
        datos.append(hora)

        return datos
        pass

    #################################################################
    # Detectamos evento  si se presiona la tecla enter              #
    #################################################################
    def keyPressEvent(self, e):
        if e.key() == Qt.Key.Key_Enter:
            # self.bIngresar.setEnabled(True)
            # self.bIngresar.setFocus()
            # Validamos el numero de maquina
            esValida = self.validarMaquina()
            if not esValida:
                # Recolectamos la informacion de los formularios, por medio de la funcion recolectarDatos()
                datos = self.recolectarDatos()
                # Preparamos la consulta
                # INSERT INTO entrada(nControl, nMaquina, fentrada, hentrada) VALUES(11590198, 19, '23/05/15', '18:25:42')
                consulta = "INSERT INTO entrada(nControl, nMaquina, fentrada, hentrada) VALUES(%d, %d, '%s', '%s')" % (
                    int(datos[0]), int(datos[1]), datos[2], datos[3])

                # Realizamos el registro de entrada.
                print(consulta)
                intentar = Conectar()
                ok = intentar.insertar(consulta)
                # Si se ha insertado correctamente limpiamos los campos, en caso contrario se avisa al usuario
                # y al encargado, se limpian los for
                if ok == True:
                    print('Registro exitoso :)')
                    self.plainLog.appendPlainText('Registro exitoso!!')

                    # Limpiamos los campos
                    self.limpiarCampos(0)
                    pass
                elif ok == False:
                    print('No se puedo registar, checar problemas!!')
                    self.plainLog.appendPlainText('No se pudo registar,\nContacte con el encargado.')
                    self.limpiarCampos(0)
                    pass

                print('#############################################################')
                pass
            elif esValida == True:

                print('\tIntente con otra maquina')
                self.plainLog.appendPlainText('\tIntete con otra maquina')
                # Dado que no esta disponible enfocamos self.maquina y borramos el contenido previo
                self.limpiarCampos(1)
                print('#############################################################')
                self.plainLog.appendPlainText(
                    '-------------------------------------------------------------------------')
                pass
            # print('Ok, ahora recolectamos los datos :)')

            pass
        pass

    def mouseLabelPressEvent(self,e):
        self.__dict__.items()
        pass
    #################################################################
    # Funcion para limpiar los campos y poner el cursor en el       #
    # nControl.                                                     #
    # Si la opcion es 0, limoia todo, si es 1 solo el campo maquina #
    #################################################################
    def limpiarCampos(self, opcion):
        if opcion == 0:
            self.nControl.setFocus()
            self.nombre.setText('')
            self.apellidos.setText('')
            self.carrera.setText('')
            self.nControl.setText('')
            self.maquina.setText('')
            pass
        elif opcion == 1:
            self.maquina.setText('')
            self.maquina.setFocus()
            pass
        pass


#################################################################
# Ejecutamos la aplicacion                                      #
#################################################################

if __name__ == '__main__':
    # Creamos un objeto de tipo QApplication
    App = QtWidgets.QApplication([])
    # Instanciamos la clase Registro
    registro = Registro()
    # Hacemos visible la aplicacion

    registro.show()

    # Capturamos los eventos de la ventana(en este caso la salida)
    sys.exit(App.exec())

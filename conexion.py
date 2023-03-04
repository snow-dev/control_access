#!usr/bin/python2.7

########################################
#	By: K                              #
#	Copyleft: Creative Commons         #
#	Usa, modifica, distribuye          #
#	y no olvides referenciar.          #
#	El mundo es de los geeks!!         #
########################################

import pymysql

class Conectar(object):
	def __init__(self):
		pass

		self.conexion = pymysql.connect(host='localhost', port = 3306, user = 'root', passwd = 'd-music', db = 'registro')

		self.cur = self.conexion.cursor()
		pass
		
#####################################################################

	def insertar(self, consulta):
		try:
			self.cur = self.conexion.cursor()
			self.cur.execute(consulta)
			pass

		except Exception:
			self.conexion.rollback()
		pass

#####################################################################

	def consulta(self, consulta):
		try:
			self.cur.execute(consulta)
			datos = self.cur.fetchall()
			return datos
			pass
		except Exception:
			self.conexion.rollback()

		pass
	pass
'''
llamar = Conectar()

sentencia = "SELECT * FROM alumnos"

resultado = llamar.consulta(sentencia)

print(resultado[0])
'''	

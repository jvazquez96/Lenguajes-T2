# - *- coding: utf- 8 - *-
# Implementación de un parser
# Reconoce expresiones definidas en la gramatica:
# https://goo.gl/TVt1wP
# Autores:
# Daniel González González		A01280648
# José Luis Carvajal Carbajal 	A01280704
# Jorge Armando Vazquez Ortiz   A01196160
#---------------------------------------------------------


import sys
import scanner as scanner

# Compara el valor del token con un valor esperado
# si el token no corresponde o el token es error
# termina el program
def match(tokenEsperado):
	global token
	if token == tokenEsperado:
		token = scanner.scanner()
	elif token == scanner.ERR:
		error(">>ERROR LEXICO<<")
	else:
		error(">>ERROR SINTACTICO<<")

# Compara el token con un termino o constante
# si no es un error
def matchTermino():
	global token
	if token == scanner.CTE or token == scanner.VAR:
		token = scanner.scanner()
	else:
		error("token inesperado")

# Funcion principal manda a llamar a oraciones() si el ultimo token
# es final la oracion esta formada correctamente, en cualquier otro caso
# esta mal formada.
def parser():
	global token
	token = scanner.scanner()
	oraciones()
	if token == scanner.END:
		print ">>ENTRADA CORRECTA<<"
	elif token == scanner.ERR:
		error(">>ERROR LEXICO<<")
	else:
		error(">>ERROR SINTACTICO<<")

# Funcion que corresponde al simbolo no terminal oraciones
def oraciones():
		oracion()
		oraciones1()

# Funcion que corresponde al simbolo no terminal oraciones1
def oraciones1():
	if token == scanner.SEPA:
		match(token)
	elif token == scanner.COM:
		match(token)
		oracion()

# Funcion que corresponde al simbolo no terminal oracion
def oracion():
	if token == scanner.PUNI:
		match(token)       # Predicador Unario
		match(scanner.LRP) # (
		matchTermino()     # termino
		match(scanner.RRP) # )
		oracion1()
	elif token == scanner.BUNI:
		match(token)        # Predicado binario
		match(scanner.LRP)  # (
		matchTermino()      # termino
		match(scanner.COM)  # , Coma
		matchTermino()      # termino
		match(scanner.RRP)  # )
		oracion1()          # oracion1
	elif token == scanner.TIL:
		match(token)        # Tilde
		oracion()           # oracion
		oracion1()          # oracion1
	elif token == scanner.CTF:
		match(token)        # Cuantificador
		match(scanner.PUNT) # . Punto
		match(scanner.VAR)  # Variable
		oracion()           # oracion
		oracion1()          # oracion1
	elif token == scanner.VAR or token == scanner.CTE:
		matchTermino()      # Termino
		match(scanner.OND)  # Igual
		matchTermino()      # Termino
		oracion1()          # Oracion1
	elif token == scanner.LRP:
		match(token)        # (
		oracion()           # oracion
		match(scanner.RRP)  # )
		oracion1()          # oracion1
	elif token == scanner.ERR:
		error(">>ERROR LEXICO<<")

# Funcion que corresponde al simbolo no terminal oracion1
def oracion1():
	if token == scanner.OBI:
		match(token)       # Operador binario
		oracion()          # oracion
		oracion1()         # oracion1

# Termina con un mensaje de error
def error(mensaje):
   	print mensaje
   	sys.exit(1)

parser()

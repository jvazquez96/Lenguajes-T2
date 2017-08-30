# - *- coding: utf- 8 - *-
# Implementación de un parser

import sys
import scanner.py as scanner

def match(tokenEsperado):
	global token
	if token == tokenEsperado:
		token = scanner.scanner()
		if token == scanner.END:
			print "Entrada Correcta"
			sys.exit(1)
	else:
		error("Lexico")

def parser():
	global token
	token = scanner.scanner()
	oraciones()
	if token == scanner.END:
		print "Entrada Correcta"
	else:
		print "Error Sintactico"

def oraciones():
		oracion()
		oraciones1()


def oraciones1():
	if token == scanner.AMP:
		match(token)
	elif token == scanner.COM:
		match(token)
		oracion()

def oracion():
	if token == scanner.PUNI:
		match(token)
	elif token == scanner.BUI:
		match(token)
	elif token == scanner.TIL:
		match(token)
	elif token == scanner.CTF:
		match(token)


def oracion1():
	if token == scanner.CTF:
		match(token)


def termino():
	if token == scanner.VAR:
		match(VAR)
	elif token == scanner.CTE:
		match(CTE)


# Termina con un mensaje de error
def error(mensaje):
    print("ERROR:", mensaje)
    sys.exit(1)
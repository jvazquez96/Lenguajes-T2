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
	if token == scanner.PUNI || token == scanner.BUNI || token == scanner.TIL || token == scanner.CTF:
		match(token)
		oraciones1()

def oraciones1():
	if token == scanner.AMP:
		match(token)
	elif if token == scanner.COM:
		match(token)
		oraciones()

# Termina con un mensaje de error
def error(mensaje):
    print("ERROR:", mensaje)
    sys.exit(1)
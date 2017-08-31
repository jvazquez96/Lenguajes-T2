# - *- coding: utf- 8 - *-
# Implementación de un parser

import sys
import scanner.py as scanner

VAR  = 101 # Variable
CTE  = 102 # Constante
SEPA = 103 # Separador
LRP  = 104 # Parentesis izquierdo
RRP  = 105 # Parentesis derecho
COM =  106 # Coma
PUNT = 107 # Punto
PUNI = 108 # Predicado unario
BUNI = 109 # Predicado binario
CTF  = 110 # Cuantificador
TIL  = 111 # Tilde ~
AMP  = 112 # Amperson &
ORP  = 113 # Or |
ESP  = 114 # Espacio
OBI  = 115 # Operador binario
UND  = 116 # Guion bajo
OND  = 117 # Asignacion
ERR  = 200 # Error
END  = 300 # END

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
		match(token) # Predicador Unario
		match(token) # (
		match(token) # terminal
		match(token) # )
		oracion1()
	elif token == scanner.BUI:
		match(token) # Predicado binario
		match(token) # (
		match(token) # termino
		match(token) # ,
		match(token) # termino
		match(token) # )
		oracion()
	elif token == scanner.TIL:
		match(token) #
		oracion()
		oracion1()
	elif token == scanner.CTF:
		match(token) # Cuantificador
		match(token) # . Punto
		match(token) # Variable
		oracion()
		oracion1()



def oracion1():
	if token == scanner.OBI:
		match(token) # Operador binario
		oracion()
		oracion1()


def termino():
	if token == scanner.VAR:
		match(VAR)
	elif token == scanner.CTE:
		match(CTE)


### Falta Simbolo terminal "Termino"


# Termina con un mensaje de error
def error(mensaje):
    print("ERROR:", mensaje)
    sys.exit(1)
# - *- coding: utf- 8 - *-
# Implementación de un scanner mediante la codificación de un Autómata
# Finito Determinista como una Matríz de Transiciones

import sys

# tokens

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
# Matriz de transiciones: codificacion del AFD
# [renglon, columna] = [estado no final, transicion]

#		a-z  A-Z   0-9      @     A     D     C     T     I     E     O     R     U     B     Z     Q     ~      &     |      <    -	   .   " "    (      )      ,    >     _   =     ?     $     ¬¬¬
MT = [[  1,    2, ERR,     3,    2,    2,    2,    2,    2,    2,    2,    2,    2,    2,    2,    2,   TIL,   AMP,  ORP,    23,   24,  PUNT,    0,  LRP,  RRP,   COM,  ERR, ERR,  OND,  END, END,  26],  #0 Estado inicial
	 [  1,  ERR,   1,    ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,   VAR,   VAR,  VAR,   VAR,  ERR,   VAR,  VAR,  VAR,  VAR,   VAR,  ERR,   1,  OND,  VAR,  VAR,  VAR],  #1 Variables
	 [ERR,    2,   2,    CTE,    2,    2,    2,    2,    2,    2,    2,    2,    2,    2,    2,    2,   CTE,   CTE,  CTE,   CTE,  ERR,   CTE,  CTE,  CTE,  CTE,   CTE,  ERR,   2,  OND,  CTE,  CTE,  CTE],  #2 Constantes
	 [ERR,  ERR,  ERR,   ERR,    4,    7,   13,   16,   19,   22,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,   ERR,   ERR,  ERR,   ERR,  ERR,   ERR,  ERR,  ERR,  ERR,   ERR,  ERR, ERR,  OND,  ERR,  ERR,  26],  #3 Arroba @ (Estado parcial)
	 [ERR,  ERR,  ERR,   ERR,  ERR,    5,   13,   16,   19,   22,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,   CTF,   CTF,  CTF,   CTF,  CTF,   CTF,  CTF,  CTF,  CTF,   CTF,  CTF, CTF,  CTF,  CTF,  CTF,  CTF],  #4 @A (Cuantificador)
	 [ERR,  ERR,  ERR,   ERR,  ERR,  ERR,  ERR,  ERR,  ERR,    6,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,   ERR,   ERR,  ERR,   ERR,  ERR,   ERR,  ERR,  ERR,  ERR,   ERR,  ERR, ERR,  OND,  ERR,  ERR,  26],  #5 @AD (Estado parcial)
	 [ERR,  ERR,  ERR,   ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  PUNI,  PUNI, PUNI,  PUNI,  ERR,  PUNI, PUNI, PUNI, PUNI,  PUNI,  ERR, ERR,  OND,  PUNI, PUNI, PUNI],  #6 @ADE (Predicador binaro)
	 [ERR,  ERR,  ERR,   ERR,  ERR,  ERR,  ERR,  ERR,  ERR,    8,   11,  ERR,  ERR,  ERR,  ERR,  ERR,   ERR,   ERR,  ERR,   ERR,  ERR,   ERR,  ERR,  ERR,  ERR,   ERR,  ERR, ERR,  OND,  ERR,  ERR,  26],  #7 @D (Estado parcial)
	 [ERR,  ERR,  ERR,   ERR,  ERR,  ERR,  ERR,    9,  ERR,  ERR,  ERR,   10,  ERR,  ERR,  ERR,  ERR,   ERR,   ERR,  ERR,   ERR,  ERR,   ERR,  ERR,  ERR,  ERR,   ERR,  ERR, ERR,  OND,  ERR,  ERR,  26],  #8 @DE (Estado parcial)
	 [ERR,  ERR,  ERR,   ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  BUNI,  BUNI, BUNI,  BUNI,  ERR,  BUNI, BUNI, BUNI,  BUNI, BUNI,  ERR, ERR,  OND,  BUNI, BUNI, BUNI],  #9 @DET (Predicado binario)
	 [ERR,  ERR,  ERR,   ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  BUNI,  BUNI, BUNI,  BUNI,  ERR,  BUNI, BUNI, BUNI,  BUNI, BUNI,  ERR, ERR,  OND,  BUNI, BUNI, BUNI],  #10 @DER (Predicado binario)
	 [ERR,  ERR,  ERR,   ERR,  ERR,   12,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,   ERR,   ERR,  ERR,   ERR,  ERR,   ERR,  ERR,  ERR,   ERR,  ERR,  ERR, ERR,  OND,  ERR,  ERR,  26],  #11 @DO (Estado parcial)
	 [ERR,  ERR,  ERR,   ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  PUNI,  PUNI, PUNI,  PUNI,  ERR,  PUNI, PUNI, PUNI, PUNI,  PUNI,  ERR, ERR,  OND,  PUNI, PUNI, PUNI],  #12 @DOD (Predicado unario)
	 [ERR,  ERR,  ERR,   ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,   14,  ERR,  ERR,  ERR,   ERR,   ERR,  ERR,   ERR,  ERR,   ERR,  ERR,  ERR,  ERR,   ERR,  ERR, ERR,  OND,  ERR,  ERR,  26],  #13 @C (Estado parcial)
	 [ERR,  ERR,  ERR,   ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,   15,  ERR,  ERR,   ERR,   ERR,  ERR,   ERR,  ERR,   ERR,  ERR,  ERR,  ERR,   ERR,  ERR, ERR,  OND,  ERR,  ERR,  26],  #14 @CU (Estado parcial)
	 [ERR,  ERR,  ERR,   ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  PUNI,  PUNI, PUNI,  PUNI,  ERR,  PUNI, PUNI, PUNI,  PUNI, PUNI,  ERR, ERR,  OND,  PUNI, PUNI, PUNI],  #15 @CUB (Predicado Unario)
	 [ERR,  ERR,  ERR,   ERR,  ERR,  ERR,  ERR,  ERR,  ERR,   17,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,   ERR,   ERR,  ERR,   ERR,  ERR,   ERR,  ERR,  ERR,   ERR,  ERR,  ERR, ERR,  OND,  ERR,  ERR,  26],  #16 @T (Estado parcial)
	 [ERR,  ERR,  ERR,   ERR,  ERR,  ERR,  ERR,   18,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,   ERR,   ERR,  ERR,   ERR,  ERR,   ERR,  ERR,  ERR,   ERR,  ERR,  ERR, ERR,  OND,  ERR,  ERR,  26],  #17 @TE (Estado parcial)
	 [ERR,  ERR,  ERR,   ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  PUNI,  PUNI, PUNI,  PUNI,  ERR,  PUNI, PUNI, PUNI,  PUNI, PUNI,  ERR, ERR,  OND,  PUNI, PUNI, PUNI],  #18 @TET (Predicado unario)
	 [ERR,  ERR,  ERR,   ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,   20,  ERR,   ERR,   ERR,  ERR,   ERR,  ERR,   ERR,  ERR,  ERR,   ERR,  ERR,  ERR, ERR,  OND,  ERR,  ERR,  26],  #19 @I (Estado parcial)
	 [ERR,  ERR,  ERR,   ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,   21,   ERR,   ERR,  ERR,   ERR,  ERR,   ERR,  ERR,  ERR,   ERR,  ERR,  ERR, ERR,  OND,  ERR,  ERR,  26],  #20 @IZ (Estado parcial)
	 [ERR,  ERR,  ERR,   ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  BUNI,  BUNI, BUNI,  BUNI,  ERR,  BUNI, BUNI, BUNI,  BUNI, BUNI,  ERR, ERR,  OND,  BUNI, BUNI, BUNI],  #21 @IZQ (Predicado binario)
	 [ERR,  ERR,  ERR,   ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,   CTF,   CTF,  CTF,   CTF,  ERR,   CTF,  CTF,  CTF,  CTF,   CTF,  ERR, ERR,  OND,  CTF,  CTF,  CTF],  #22 @E (Cuantificador)
	 [ERR,  ERR,  ERR,   ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,   ERR,   ERR,  ERR,   ERR,  24,    ERR,  ERR,  ERR,  ERR,   ERR,  ERR, ERR,  OND,  ERR,  ERR,  26],  #23 < (Estado parcial)
	 [ERR,  ERR,  ERR,   ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,   ERR,   ERR,  ERR,   ERR,  ERR,   ERR,  ERR,  ERR,  ERR,   ERR,  OBI, ERR,  OND,  ERR,  ERR,  26],  #24 <- | - (Estado parcia;)
	 [OBI,  OBI,  OBI,   OBI,  OBI,  OBI,  OBI,  OBI,  OBI,  OBI,  OBI,  OBI,  OBI,  OBI,  OBI,  OBI,   OBI,   OBI,  OBI,   OBI,  ERR,   OBI,  OBI,  OBI,  OBI,   OBI,  ERR, ERR,  OND,  OBI,  OBI,  OBI], #25 <-> | -> (Operador binario)
	 [ERR,  ERR,  ERR,   ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,   ERR,    ERR,  ERR,   ERR,  ERR,   ERR,  ERR,  ERR,  ERR,   ERR,  ERR, ERR,  ERR,  ERR,  ERR,  ERR]]  #26 WTF


def filtro(c):
	global isAt
	if c >= 'a' and c <= 'z':
		return 0
	elif c >= 'A' and c <= 'Z':
		if isAt:
			if c == 'A':
				return 4
			elif c == 'D':
				return 5
			elif c == 'C':
				return 6
			elif c == 'T':
				return 7
			elif c == 'I':
				return 8
			elif c == 'E':
				return 9
			elif c == 'O':
				return 10
			elif c == 'R':
				return 11
			elif c == 'U':
				return 12
			elif c == 'B':
				return 13
			elif c == 'Z':
				return 14
			elif c == 'Q':
				return 15
			else:
				return 1
		else:
			return 1
	elif c >= '0' and c <= '9':
		return 2
	elif c == '@':
		isAt = 1
		return 3
	elif c == '~':
		return 16
	elif c == '&':
		return 17
	elif c == '|':
		return 18
	elif c == '<':
		return 19
	elif c == '-':
		return 20
	elif c == '.':
		return 21
	elif c == ' ' or ord(c) == 9 or ord(c) == 10 or ord(c) == 13:
		return 22
	elif c == '(':
		isAt = 0
		return 23
	elif c == ')':
		return 24
	elif c == ',':
		return 25
	elif c == '>':
		return 26
	elif c == '_':
		return 27
	elif c == '=':
		return 28
	elif c == '?':
		return 29
	elif c == '$':
		return 30
	else:
		return 31

_c = None
_leer = True

def scanner():
	global isAt
	edo = 0 # n.mero de estado en el aut.mata
	lexema = "" # palabra que genera el token
	global _c
	tokens = []
	global _leer # indica si se requiere leer un caracter de la entrada est.ndar
	isAt = 0
	while (True):
		while edo < 100:    # mientras el estado no sea ACEPTOR ni ERROR
			if _leer:
				_c = sys.stdin.read(1)
			else:
				_leer = True
			# print "Renglon", edo
			edo = MT[edo][filtro(_c)]
			# print "columna", filtro(c)
			if edo < 100 and edo != 0: lexema += _c
		if edo == VAR:
			_leer = False # ya se ley. el siguiente caracter
			print "Variable", lexema
			return VAR
		elif edo == CTE:
			_leer = False # ya se ley. el siguiente caracter
			print "Constante", lexema
			#return CTE
		elif edo == SEPA:
			lexema += _c  # el .ltimo caracter forma el lexema
			print "Separador", lexema
			return SEPA
		elif edo == LRP:
			lexema += _c  # el .ltimo caracter forma el lexema
			print "Delimitador", lexema
			return LRP
		elif edo == RRP:
			lexema += _c  # el .ltimo caracter forma el lexema
			print "Delimitador", lexema
			return RRP
		elif edo == COM:
			lexema += _c
			print "Coma", lexema
			return COM
		elif edo == PUNT:
			lexema += _c
			print "Punto", lexema
			return PUNT
		elif edo == PUNI:
			_leer = False
			print "Predicado Unario", lexema
			return PUNI
		elif edo == BUNI:
			_leer = False # el .ltimo caracter no es raro
			print "Predicado Binario", lexema
			return BUNI
		elif edo == CTF:
			_leer = False
			print "Cuantificador", lexema
			return CTF
		elif edo == TIL:
			print "Tilde", lexema
			return TIL
		elif edo == AMP:
			print "Amperson", lexema
			return AMP
		elif edo == ORP:
			print "Or", lexema
			return ORP
		elif edo == ESP:
			print "Espacio", lexema
			return ESP
		elif edo == OBI:
			lexema += _c
			print "Operador binario", lexema
			return OBI
		elif edo == UND:
			print "Guion bajo", lexema
			return UND
		elif edo == OND:
			print "Asignacion", lexema
			return OND
		elif edo == ERR:
			lexema += _c
			print "Error", lexema
			return ERR
			tokens.append(edo)
		if edo == END: return tokens
		lexema = ""
		edo = 0

# scanner()

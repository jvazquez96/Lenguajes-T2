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
COM = 106 # Coma
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
ERR  = 200 # Error

# Matriz de transiciones: codificacion del AFD
# [renglon, columna] = [estado no final, transicion]

#		a-z  A-Z   0-9     @     A     D     C     T     I     E     O     R     U     B     Z     Q    ~     &     |     <    -	    .   " "    (      )      ,    >   –
MT = [[  1,    2, ERR,     3,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  TIL,  AMP,  ORP,   23,   24,  PUNT,  ESP,  LRP,  RRP,   COM,  ERR, ERR],  # Estado inicial
	  [  1,  ERR,   1,   ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,   VAR,  VAR,  VAR,  VAR,   VAR,  ERR,   1],  # Variables
	  [ERR,    2,   2,   ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,   CTE,  CTE,  CTE,  CTE,   CTE,  ERR,   2],  # Constantes
	  [ERR,  ERR,  ERR,  ERR,    4,    7,   13,   16,   19,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,   ERR,  ERR,  ERR,  ERR,   ERR,  ERR, ERR],  # Arroba @ (Estado parcial)
	  [ERR,  ERR,  ERR,  ERR,  ERR,    5,   13,   16,   19,   22,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,   CTF,  CTF,  CTF,  CTF,   CTF,  ERR, ERR],  # @A (Cuantificador)
	  [ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,    6,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,   ERR,  ERR,  ERR,  ERR,   ERR,  ERR, ERR],  # @AD (Estado parcial)
	  [ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,   CTF,  CTF,  CTF,  CTF,   CTF,  ERR, ERR],  # @ADE (Predicador binaro)
	  [ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,    8,   11,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,   ERR,  ERR,  ERR,  ERR,   ERR,  ERR, ERR],  # @D (Estado parcial)
	  [ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,   10,  ERR,  ERR,  ERR,    9,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,   ERR,  ERR,  ERR,  ERR,   ERR,  ERR, ERR],  # @DE (Estado parcial)
	  [ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  BUNI, BUNI, BUNI,  BUNI, BUNI,  ERR, ERR],  # @DET (Predicado binario)
	  [ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  BUNI, BUNI, BUNI,  BUNI, BUNI,  ERR, ERR],  # @DER (Predicado binario)
	  [ERR,  ERR,  ERR,  ERR,  ERR,   12,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,   ERR,  ERR,  ERR,   ERR,  ERR,  ERR, ERR],  # @DO (Estado parcial)
	  [ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  BUNI, BUNI, BUNI,  BUNI, BUNI,  ERR, ERR],  # @DOD (Predicado binario)
	  [ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,   14,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,   ERR,  ERR,  ERR,  ERR,   ERR,  ERR, ERR],  # @C (Estado parcial)
	  [ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,   15,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,   ERR,  ERR,  ERR,  ERR,   ERR,  ERR, ERR],  # @CU (Estado parcial)
	  [ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  PUNI, PUNI, PUNI,  PUNI, PUNI,  ERR, ERR],  # @CUB (Predicado Unario)
	  [ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,   17,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,   ERR,  ERR,  ERR,   ERR,  ERR,  ERR, ERR],  # @T (Estado parcial)
	  [ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,   18,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,   ERR,  ERR,  ERR,   ERR,  ERR,  ERR, ERR],  # @TE (Estado parcial)
	  [ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  BUNI, BUNI, BUNI,  BUNI, BUNI,  ERR, ERR],  # @TET (Predicado binario)
	  [ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,   20,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,   ERR,  ERR,  ERR,   ERR,  ERR,  ERR, ERR],  # @I (Estado parcial)
	  [ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,   21,  ERR,  ERR,  ERR,  ERR,  ERR,   ERR,  ERR,  ERR,   ERR,  ERR,  ERR, ERR],  # @IZ (Estado parcial)
	  [ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  BUNI, BUNI, BUNI,  BUNI, BUNI,  ERR, ERR],  # @IZQ (Predicado binario)
	  [ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,   CTF,  CTF,  CTF,  CTF,   CTF,  ERR, ERR],  # @E (Cuantificador)
	  [ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  24,    ERR,  ERR,  ERR,  ERR,   ERR,  ERR, ERR],  # < (Estado parcial)
	  [ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,   CTF,  CTF,  CTF,  CTF,   CTF,   25, ERR],  # <- | - (Estado parcia;)
	  [ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,  ERR,   OBI,  OBI,  OBI,  OBI,   OBI,  ERR, ERR]]  # <-> | -> (Operador binario)

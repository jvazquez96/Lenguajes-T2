# - *- coding: utf- 8 - *-
# Implementación de un scanner mediante la codificación de un Autómata
# Finito Determinista como una Matríz de Transiciones

import sys

# tokens

VAR  = 101 # Variable
CTE  = 102 # Constante
SEPA = 103 # Separador
LRP  = 104 # Parentesis izquierdo
RRP  = 105 # PArentesis derecho
COMA = 106 # Coma
PUNT = 107 # Punto
PUNI = 108 # Predicado unario
BUNI = 109 # Predicado binario
CTF  = 110 # Cuantificador
TIL  = 111 # Tilde ~ 
ERR  = 200 # Error

# Matriz de transiciones: codificacion del AFD
# [renglon, columna] = [estado no final, transicion]
#      a-z  A-Z    0-9         _       @CUB  @TET  @DOD  @IZQ  @DER  @ADE   @DET    @A   @E    ~        &    |      ->     <->     $      (      )     ,     .   \t " "
MT = [[  1,   2, PENDIENTE, PENDIENTE,    3,    3,    3,    4,    4,    4,     4,   5,   5,   TIL,   SEPA, SEPA,  SEPA,   SEPA,  SEPA,  LRP,   RRP,  COM, PUNT,   END],
	  [1, ERR, 1, 1, VAR, VAR, VAR, VAR, VAR, VAR, VAR, VAR, VAR, TIL, VAR, VAR, VAR , VAR, VAR, VAR, VAR, VAR, VAR, VAR],
	  [ERR, 2, 2, 2, CTE, CTE, CTE, CTE, CTE, CTE, CTE, CTE, CTE, TIL, CTE, CTE, CTE, CTE, CTE, CTE, CTE, CTE, CTE, CTE],
	  [PUNI, PUNI, PUNI, PUNI, 3, 3, 3, PUNI, PUNI, PUNI, PUNI, PUNI, PUNI, TIL, PUNI, PUNI, PUNI, PUNI, PUNI, PUNI, PUNI, PUNI, PUNI, PUNI],
	  [BUNI, BUNI, BUNI, BUNI, BUNI, BUNI, BUNI, 4, 4, 4, 4, BUNI, BUNI, TIL, BUNI, BUNI, BUNI, BUNI, BUNI, BUNI, BUNI, BUNI],
	  [CTF, CTF, CTF, CTF, CTF, CTF, CTF, CTF, CTF, CTF, CTF, 5, 5, TIL, CTF, CTF, CTF, CTF, CTF, CTF, CTF, CTF, CTF, CTF], 
	  [ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR< ERR< ERR, ERR, ERR< ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR]]
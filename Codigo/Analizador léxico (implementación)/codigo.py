import ply.lex as lex
import os

# Lista de tokens
tokens = [
    'ID', 'ENT', 'FLOT', 'LARGO', 'CARAC', 'STRING', 'NUM', 
    'CLAVE_POR', 'CLAVE_HAZ', 'CLAVE_MIENTRAS', 'BOOL', 'CLAVE_SI', 
    'CLAVE_SINO', 'IMPRIMIR', 'LEER', 'RETORNAR', 'OP_IGUAL', 
    'OP_MENOR', 'OP_MAYOR', 'OP_IGUAL_QUE', 'OP_DIFERENTE_QUE', 
    'OP_NEGACION', 'OP_MAYORIGUAL', 'OP_MENORIGUAL', 'PAR_IZQ', 
    'PAR_DER', 'CORCH_IZQ', 'CORCH_DER', 'LLAVE_IZQ', 'LLAVE_DER', 
    'OP_SUMA', 'OP_RESTA', 'OP_MULTI', 'OP_DIVI', 'OP_MOD', 
    'OP_BOOL', 'SUMAUNOAUNO', 'COMENTARIOLINEAL', 'COMENTARIOMULTIPLE',
    'DOBLE', 'COMA', 'DPUNTOS', 'PUNTO', 'COMILLA', 'DCOMILLAS', 
    'PYCOMA', 'CLAVE_DEF', 'FINDELINEA', 'OR', 'AND'
]

# Expresiones regulares para tokens
t_OP_IGUAL_QUE = r'=='
t_OP_DIFERENTE_QUE = r'!='
t_OP_MAYOR = r'>'
t_OP_MENOR = r'<'
t_OP_MAYORIGUAL = r'>='
t_OP_MENORIGUAL = r'<='
t_OP_NEGACION = r'!'
t_OP_IGUAL = r'='
t_OP_SUMA = r'\+'
t_OP_RESTA = r'-'
t_OP_MULTI = r'\*'
t_OP_DIVI = r'/'
t_PAR_IZQ = r'\('
t_PAR_DER = r'\)'
t_LLAVE_IZQ = r'\{'
t_LLAVE_DER = r'\}'
t_COMILLA = r'"'
t_PYCOMA = r';'
t_COMA = r','
t_DPUNTOS = r':'
t_PUNTO = r'\.'
t_FINDELINEA = r'\n'

# regular expression for integers
def t_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t

# regular expression for identifiers
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t

# regular expression for boolean values
def t_BOOL(t):
    r'(true|false)'
    return t

# Rule to track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Rule for ignoring whitespace
t_ignore = ' \t'

# Error handling rule
def t_error(t):
    print(f"Carácter ilegal: '{t.value[0]}'")
    t.lexer.skip(1)

# Construir el lexer
lexer = lex.lex()

# Archivos de prueba
archivos_prueba = ["pruebas1.txt", "pruebas2.txt", "pruebas3.txt"]

# Analizar cada archivo de prueba
for archivo in archivos_prueba:
    # Leer contenido del archivo
    with open(archivo, 'r') as file:
        code = file.read()

    print(f"Tokens encontrados en {archivo}:")
    # Dar al lexer el código del archivo
    lexer.input(code)

    # Tokenizar el código del archivo
    for tok in lexer:
        print(tok)

    print()  # Agregar línea en blanco entre cada archivo

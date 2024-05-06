import ply.lex as lex

# Lista de palabras reservadas con sus correspondientes tokens
reserved = {
    'por': 'CLAVE_POR',
    'haz': 'CLAVE_HAZ',
    'mientras': 'CLAVE_MIENTRAS',
    'si': 'CLAVE_SI',
    'sino': 'CLAVE_SINO',
    'imprimir': 'IMPRIMIR',
    'leer': 'LEER',
    'retornar': 'RETORNAR',
    'def': 'CLAVE_DEF',
    'verdadero': 'BOOL_TR',
    'falso': 'BOOL_FS',
    'o': 'OR',
    'y': 'AND'
}

# Lista de tokens
tokens = [
    'ID', 'NUM', 'FLOT', 'CARAC', 'STRING',
    'OP_IGUAL_QUE', 'OP_DIFERENTE_QUE', 'OP_MAYOR', 'OP_MENOR',
    'OP_MAYORIGUAL', 'OP_MENORIGUAL', 'OP_NEGACION', 'OP_IGUAL',
    'OP_SUMA', 'OP_RESTA', 'OP_MULTI', 'OP_DIVI', 'OP_MOD',
    'SUMAUNOAUNO', 'COMENTARIOLINEAL',
    'DOBLE', 'COMA', 'DPUNTOS', 'PUNTO', 'COMILLA', 'DCOMILLAS',
    'PYCOMA', 'FINDELINEA', 'PAR_IZQ', 'PAR_DER', 'CORCH_IZQ', 'CORCH_DER','LLAVE_IZQ', 'LLAVE_DER',
    'PYCOMA'
] + list(reserved.values())


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
t_OP_MOD = r'%'
t_COMA = r','
t_DPUNTOS = r':'
t_PUNTO = r'\.'
t_FINDELINEA = r'\n'
t_PAR_IZQ = r'\('
t_PAR_DER = r'\)'
t_CORCH_IZQ = r'\['
t_CORCH_DER = r'\]'
t_LLAVE_IZQ = r'\{'
t_LLAVE_DER = r'\}'
t_PYCOMA = r';'


# Expresión regular para números enteros
def t_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Expresión regular para números flotantes
def t_FLOT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

# Expresión regular para identificadores
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')  # Comprueba si es una palabra reservada
    return t


# Expresión regular para cadenas
def t_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"'
    return t

# Expresión regular para caracteres
def t_CARAC(t):
    r'\'.\''
    return t

# Expresión regular para dobles caracteres
def t_DOBLE(t):
    r'\'\''
    return t

# Regla para rastrear números de línea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Regla para ignorar espacios en blanco
t_ignore = ' \t'

# Regla para manejar errores
def t_error(t):
    print(f"Carácter ilegal: '{t.value[0]}'")
    t.lexer.skip(1)

# Regla para comentarios
def t_COMENTARIOLINEAL(t):
    r'//.*'
    pass


# Construye el analizador léxico
lexer = lex.lex()

# Archivos de prueba
archivos_prueba = ["pruebas1.txt"]

# Expresión regular para paréntesis izquierdo
t_OPEN_PARENTHESES = r'\('

# Expresión regular para paréntesis derecho
t_CLOSE_PARENTHESES = r'\)'

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

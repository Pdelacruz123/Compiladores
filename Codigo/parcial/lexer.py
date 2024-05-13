import ply.lex as lex




 
tokens = [
    
    'MAIN',
    'FINMAIN',
    'DEF',
    'FINDEF',
    
    'ENT',
    'FLOT',
    'DOBLE',
    'CARAC',
    'BOOL',
    'STRING',
    
    'NUM',
    
    'BOOL_TR',
    'BOOL_FS',
    
    'SI',
    'SINO',
    'FINSI',
    'POR',
    'FINPOR',
    'MIENTRAS',
    'FINMIENTRAS',
    'COUT',
    'SLINEA',
    'CIN',
    'RETORNAR',
    

 
    'PAR_IZQ',
    'PAR_DER',
    'AND',
    'OR',
    'PYCOMA',
    'OP_SUMA',
    'OP_RESTA',
    'OP_MULTI',
    'OP_DIVI',
    'OP_IGUAL',  
    'OP_MAYOR',
    'OP_MENOR', 
    'OP_MAYORIGUAL',
    'OP_MENORIGUAL',
    'OP_IGUAL_QUE',
    'OP_DIFERENTE_QUE', 
    'CORCH_IZQ',
    'CORCH_DER',
    'COMENTARIOLINEAL',
    'COMILLA',
    'OP_MOD',
    'decimal',
    'OP_SUMAUNOAUNO',
    'OP_NEGACION',
    'COMA',
    'IMPRIMIR',
    'ID',
    
]


# Expresiones regulares

def t_MAIN(t):
  r'MAIN'
  return t

def t_FINMAIN(t):
  r'FINMAIN'
  return t

def t_DEF(t):
  r'DEF'
  return t

def t_FINDEF(t):
  r'FINDEF'
  return t

def t_ENT(t):
  r'ENT'
  return t

def t_FLOT(t):
  r'FLOT'
  return t

def t_CARAC(t):
  r'char'
  return t

def t_BOOL(t):
  r'BOOL'
  return t

def t_BOOL_TR(t):
  r'true'
  return t

def t_BOOL_FS(t):
  r'false'
  return t

def t_STRING(t):
  r'STRING'
  return t

###
def t_SI(t):
  r'SI'
  return t

def t_SINO(t):
  r'SINO'
  return t

def t_FINSI(t):
  r'FINSI'
  return t

def t_POR(t):
  r'POR'
  return t

def t_FINPOR(t):
  r'FINPOR'
  return t

def t_MIENTRAS(t):
  r'MIENTRAS'
  return t

def t_FINMIENTRAS(t):
  r'EndWhile'
  return t

def t_COUT(t):
  r'COUT'
  return t

def t_SLINEA(t):
  r'S'
  return t

def t_CIN(t):
  r'cin'
  return t

def t_RETORNAR(t):
  r'RETORNAR'
  return t



def t_IMPRIMIR(t):
    r'("[a-zA-Z0-9 ]*")'
    return t


def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9]*'
    return t


def t_NUM(t):
  r'\d+(\.\d+)?'
  if '.' in t.value:
      t.value = float(t.value)
  else:
      t.value = int(t.value)
  return t



 
t_OP_SUMA = r'\+'
t_OP_RESTA = r'-'
t_OP_MULTI = r'\*'
t_OP_DIVI = r'/'
t_PAR_IZQ = r'\('
t_PAR_DER = r'\)'
t_AND = r'&&' 
t_OR = r'\|\|'  
t_COMA = r','
t_OP_IGUAL = r'='
t_OP_MENOR = r'<'
t_OP_MAYOR = r'>'
t_OP_DIFERENTE_QUE = r'!='
t_OP_NEGACION = r'!'
t_OP_MAYORIGUAL = r'>='
t_OP_MENORIGUAL = r'<='
t_OP_IGUAL_QUE = r'=='
t_CORCH_IZQ = r'\['
t_CORCH_DER = r'\]'
t_COMENTARIOLINEAL = r'//.*'
t_COMILLA = r'\'.*?\''
t_OP_MOD = r'%'
t_OP_SUMAUNOAUNO = r'\+\+'
t_decimal = r'[0-9]+\.[0-9]+'


def t_whitespace(t):
    r'\s+'
    pass

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)


lexer = lex.lex()


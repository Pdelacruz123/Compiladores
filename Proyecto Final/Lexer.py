# ------------------------------------------------------------
# Lexer
# Piero De La Cruz
# ------------------------------------------------------------
import ply.lex as lex
# List of token names. This is always required
tokens = ('charlie','si','sino','bool','entero',
          'numero','flotante','decimal','print',
          'texto','ltexto','break','while',
          'devuelve','caract','lcaract',
          'mas','menos','por','y','o',
          'dividir','mayor','menor',
          'pizquierdo','pderecho','cizquierdo',
          'cderecho','coma','igual','menor_igual',
          'mayor_igual','diferente','identificador',
          'lizquierdo','lderecho','division','true',
          'false','modulo','pug','comparacion')

# Regular expression rules for simple tokens
t_charlie = r'charlie'
t_si = r'si'
t_sino = r'sino'
t_bool = r'bool'
t_entero = r'entero'
t_flotante = r'flotante'
t_print = r'print'
t_texto = r'texto'
t_break = r'break'
t_while = r'while'
t_devuelve = r'devuelve'
t_caract = r'caract'
t_pug = r'pug'
t_comparacion = r'\=\='

t_mas = r'\+'
t_menos = r'\-'
t_por = r'\*'
t_dividir = r'\/'
t_modulo = r'\%'

t_y = r'\#y'
t_o = r'\#o'

t_mayor = r'\>'
t_menor = r'\<'

t_pizquierdo = r'\('
t_pderecho = r'\)'

t_lizquierdo = r'\{'
t_lderecho = r'\}'

t_cizquierdo = r'\['
t_cderecho = r'\]'

t_coma = r'\,'
t_igual = r'\='
t_menor_igual = r'\<\='
t_mayor_igual = r'\>\='
t_diferente = r'\<\>'

def t_identificador(t):
  r'(?!flotante|si|sino|bool|entero|print|texto|break|while|devuelve|caract|charlie|false|true|pug)[a-zA-Z]+[\w]*'
  try:
    t.value = t.value
  except ValueError:
    t.value = 0
  return t



# A regular expression rule with some action code
def t_false(t):
  r'false'
  t.value = False 
  return t

def t_true(t):
  r'true'
  t.value = True 
  return t

def t_numero(t):
  r'\d+(?!\.)'
  try:
    t.value = int(t.value) 
  except ValueError:
    t.value = 0
  return t

def t_decimal(t):
  r'(0|[1-9][0-9]*)\.[0-9]*'
  try:
    t.value = float(t.value)
  except ValueError:
    t.value = 0
  return t

def t_lcaract(t):
  r'\'(\W|\w)\''
  t.value = t.value 
  return t

def t_ltexto(t):
  r'\"(\W|\w)+\"'
  t.value = t.value 
  return t

def t_comments(t):
    r'\~(\w|\W)*\~'


def t_newline(t):
  r'\n+'
  t.lexer.lineno += len(t.value)

t_ignore = ' \t'

def t_error(t):
  print("Error léxico, caracter no conocido: '%s'" % t.value[0])
  t.lexer.skip(1)
  raise SystemExit

lexer = lex.lex()


file=open('archivo2.txt','r')
texto=file.readlines()
file.close()
data = texto
tokens=[]
tokens_info=[]
for renglon in texto:

  lexer.input(renglon)
  # Tokenize
  while True:
    tok = lexer.token()
    if not tok:
      break 
    tokens.append(tok.type)
    tokens_info.append(tok)
    #print(tok)
    print(tok.type, tok.value, tok.lineno, tok.lexpos)
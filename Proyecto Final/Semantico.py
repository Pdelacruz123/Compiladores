import Parser
class simbolo:# Clase símbolo que representa un identificador en el código
  def __init__(self,t,lex,tp,pos,lin,scope,td=None):
    self.token=t# El token que representa el símbolo
    self.lexema=lex# El lexema (nombre) del símbolo
    self.tipo=tp# El tipo de símbolo (variable, función, etc.)
    self.posicion=pos # La posición del token en el código fuente
    self.linea=lin # La línea del código donde aparece el símbolo
    self.scope=scope  # El ámbito en el que se encuentra el símbolo
    self.tipo_dato=td # El tipo de dato del símbolo
# Función para buscar el tipo de dato de un símbolo en la tabla de símbolos
def buscar_simbolo(tabla,elemento):
  for i in tabla:
    if i.lexema==elemento and (i.tipo == "variable" or i.tipo == "charlie"):
      return i.tipo_dato
# Función para buscar el tipo de un símbolo en la tabla de símbolos
def buscar_tipo_de_simbolo(tabla,elemento):
  for i in tabla:
    if i.lexema==elemento and (i.tipo == "variable" or i.tipo == "charlie"):
      return i.tipo
# Función para imprimir la tabla de símbolos completa
def imprimir_tds(tabla):
  for i in tabla:
    print(i.token,i.lexema,i.tipo,i.posicion,i.linea,i.scope)
# Función recursiva para buscar una función (charlie) en el árbol sintáctico
def buscar_charlie(arbol,i):
  if arbol.elemento == "DeclaracionFuncion" and arbol.hijos[1].token.value == i:
    return arbol
  for subarbol in arbol.hijos:
    arbolBuscado = buscar_charlie(subarbol, i)
    if (arbolBuscado != None):
        return arbolBuscado
  return None
# Función para obtener el tipo de dato de una función (charlie) del árbol sintáctico
def obtener_tipo_charlie(arbol):
  if arbol.hijos[6].hijos[1].hijos[0].elemento == "''":
    return None
  else:
    tipo = verificar_tipo_Ex(arbol.hijos[6].hijos[1].hijos[1].hijos[0])
    return tipo

# Inicializa variables globales
n=0
es_while=False
tabla_de_simbolos=[]# Tabla de símbolos vacía
#Parser.arbol.imprimirArbol(Parser.arbolito)
funcion_actual=None
funcion_actual_aux=None
errores = False # Indicador de errores
# Función para verificar el tipo de dato de un identificador
def verificar_tipo_de_dato_id(node_tx):
  tipo_de_dato = buscar_simbolo(tabla_de_simbolos,node_tx.hijos[0].token.value)
  return tipo_de_dato
# Función para verificar el tipo de un término (número, booleano, texto, etc.)
def verificar_tipo_de_termino(node_t):
  tipo_de_dato = None
  if node_t.elemento == "lbool":
    tipo_de_dato = "bool"
  elif node_t.elemento == "numero":
    tipo_de_dato = "entero"
  elif node_t.elemento == "ltexto":
    tipo_de_dato = "texto"
  elif node_t.elemento == "decimal":
    tipo_de_dato = "flotante"
  elif node_t.elemento == "lcaract":
    tipo_de_dato = "caract"
  return tipo_de_dato
# Función recursiva para verificar el tipo de una expresión prima (Ex')
def verificar_tipo_Ex_prima(node_Ex_prima):
  global errores
  tipo_de_dato_Ex_prima = "None"
  if node_Ex_prima.hijos[0].elemento=="''":
    tipo_de_dato_Ex_prima = "None"
  elif node_Ex_prima.hijos[0].elemento=="Simbolo":
    tipo_de_dato_T = verificar_tipo_Tx(node_Ex_prima.hijos[1])
    tipo_de_dato_Ex_prima = verificar_tipo_Ex_prima(node_Ex_prima.hijos[2])

    if tipo_de_dato_Ex_prima == "None":
      tipo_de_dato_Ex_prima = tipo_de_dato_T
    else:
      if tipo_de_dato_T == tipo_de_dato_Ex_prima:
        tipo_de_dato_Ex_prima = tipo_de_dato_T
      else:
        print("Error de asiganción 3 en la línea " + str(node_Ex_prima.hijos[1].hijos[0].hijos[0].token.lineno) + ": los tipos no coinciden")
        errores = True
  return tipo_de_dato_Ex_prima
# Función para verificar el tipo de una expresión (Tx)
def verificar_tipo_Tx(node_Tx):
  tipo_de_dato=None
  if node_Tx.hijos[0].elemento == "Literal":
    tipo_de_dato = verificar_tipo_de_termino(node_Tx.hijos[0].hijos[0])
  elif node_Tx.hijos[0].elemento == "identificador":
    tipo_de_dato = verificar_tipo_de_dato_id(node_Tx)
  return tipo_de_dato


# Función para verificar el tipo entre una expresión (Tx) y una expresión prima (Ex')
def verificar_tipo_Tx_Ex_prima(node_Tx, node_Ex_prima):
  global errores
  type_Tx = verificar_tipo_Tx(node_Tx)
  type_Ex_prima= verificar_tipo_Ex_prima(node_Ex_prima)
  if str(type_Ex_prima) == "None":
    return type_Tx
  else:
    if type_Tx ==  type_Ex_prima:
      return type_Tx
    else:
      print("Error de asiganción 2 en la línea " + str(node_Tx.hijos[0].hijos[0].token.lineno) + ": los tipos no coinciden")
      errores = True
# Función para verificar el tipo de una expresión (Ex)
def verificar_tipo_Ex(arbol):
  tipo_de_dato = verificar_tipo_Tx_Ex_prima(arbol.hijos[0],arbol.hijos[1])
  return tipo_de_dato
# Función para comprobar si un identificador está duplicado
def comprobar_duplicado(valor,linea):
  global errores
  for x in reversed(tabla_de_simbolos):
    if x.lexema==valor and (x.tipo=="charlie" or x.tipo == "variable"):
      print("Error errore semántico en línea "+ str(linea) + ": " + x.lexema + " ya fue declarado")
      errores = True
      break
# Función para comprobar si un identificador existe
def comprobar_existencia(valor,tipo,linea):
  global errores
  encontrado=False
  for x in reversed(tabla_de_simbolos):
    if x.lexema==valor and x.tipo==tipo:
      encontrado=True
      break
  if encontrado==False:
    print("Error semántico en línea "+ str(linea) + ": Llamaste a la " + tipo + " " + valor + ", pero no fue declarada")
    errores = True

# Función para verificar la declaración de una variable
def verificar_declaracion_variable(arbol):
  global errores
  comprobar_duplicado(arbol.hijos[1].token.value,arbol.hijos[1].token.lineno)


 # Agrega la variable a la tabla de símbolos
  tabla_de_simbolos.append(simbolo(arbol.hijos[1].token,arbol.hijos[1].token.value,"variable",arbol.hijos[1].token.lexpos,arbol.hijos[1].token.lineno,funcion_actual,arbol.hijos[0].hijos[0].elemento))

# Verifica la asignación de la variable
  if arbol.hijos[3].hijos[0].elemento == "igual":
    td_asignacion = verificar_tipo_Ex(arbol.hijos[3].hijos[1].hijos[0])
    td_variable = buscar_simbolo(tabla_de_simbolos,arbol.hijos[1].token.value)
    if td_variable != td_asignacion:
      print ("Error de asignación en la línea " + str(arbol.hijos[1].token.lineno) + ": no coincienden los tipos")
      errores = True
    else:
      arbol.hijos[3].hijos[1].tipo=td_asignacion
# Función para obtener los parámetros de una función (charlie) del árbol sintáctico
def obtener_parametros_lcharlie(arbol,par):
  if arbol.elemento=="PL":
    tipo = verificar_tipo_Ex(arbol.hijos[0].hijos[0])
    par.append(tipo)
    arbol.hijos[0].tipo=tipo
  for x in arbol.hijos:
    obtener_parametros_lcharlie(x,par)
# Función para obtener parámetros de una función (charlie) desde el árbol sintáctico
def obtener_parametros(arbol,par):
  if arbol.elemento=="Y":# Si el nodo actual es del tipo 'Y', es un parámetro
    par.append(arbol.hijos[0].hijos[0].elemento)# Agrega el parámetro a la lista de parámetros
  for x in arbol.hijos:# Recorre sobre los hijos del nodo actual
    obtener_parametros(x,par)
# Función para insertar parámetros en la tabla de símbolos
def insertar_parametros(arbol):
  if arbol.elemento=="Y":# Si el nodo actual es del tipo 'Y', es un parámetro,Agrega el parámetro a la tabla de símbolos como una variable
    tabla_de_simbolos.append(simbolo(arbol.hijos[1].token,arbol.hijos[1].token.value,"variable",arbol.hijos[1].token.lexpos,arbol.hijos[1].token.lineno,funcion_actual,arbol.hijos[0].hijos[0].elemento))
  for x in arbol.hijos:# Recurre sobre los hijos del nodo actual
    insertar_parametros(x)
# Función para verificar la declaración y los parámetros de una función (charlie)
def verificar_charlie(arbol):
  global funcion_actual
  global funcion_actual_aux
  comprobar_duplicado(arbol.hijos[1].token.value,arbol.hijos[1].token.lineno)# Comprueba si el nombre de la función ya ha sido declarado
  funcion_actual=arbol.hijos[1].token.value# Actualiza la función actual
  funcion_actual_aux=funcion_actual
  if arbol.hijos[3].hijos[0]!="''":# Si la función tiene parámetros, los inserta en la tabla de símbolos
    insertar_parametros(arbol.hijos[3])
  tipo_de_charlie=obtener_tipo_charlie(arbol)# Obtiene el tipo de la función
  arbol.hijos[1].tipo = tipo_de_charlie# Agrega la función a la tabla de símbolos
  tabla_de_simbolos.append(simbolo(arbol.hijos[1].token,arbol.hijos[1].token.value,"charlie",arbol.hijos[1].token.lexpos,arbol.hijos[1].token.lineno,"global",tipo_de_charlie))

def verificar_asignacion_de_variable(arbol):
  global errores
  comprobar_existencia(arbol.hijos[0].token.value,"variable",arbol.hijos[0].token.lineno)# Verifica que la variable haya sido declarada
 # Verifica el tipo de la expresión asignada
  td_asignacion = verificar_tipo_Ex(arbol.hijos[1].hijos[1].hijos[0])
  td_variable = buscar_simbolo(tabla_de_simbolos,arbol.hijos[0].token.value)

  if td_variable != td_asignacion:# Comprueba si los tipos coinciden
    print ("Error de asignación en la línea " + str(arbol.hijos[0].token.lineno) + ": no coincienden los tipos")
    errores = True
  else:
      arbol.hijos[1].hijos[1].tipo=td_asignacion
# Agrega la asignación a la tabla de símbolos
  tabla_de_simbolos.append(simbolo(arbol.hijos[0].token,arbol.hijos[0].token.value,"asignacion",arbol.hijos[0].token.lexpos,arbol.hijos[0].token.lineno,funcion_actual))

def verificar_llamar_variable(arbol):# Función para verificar si se llama a una variable que existe
  comprobar_existencia(arbol.hijos[0].token.value,"variable",arbol.hijos[0].token.lineno)
# Función para verificar la llamada a una función (charlie)
def verificar_llamar_charlie(arbol):
  global errores
  parametros=[]
  parametros_lcharlie=[]
  comprobar_existencia(arbol.hijos[0].token.value,"charlie",arbol.hijos[0].token.lineno)# Verifica que la función (charlie) haya sido declarada
  nodo_charlie=buscar_charlie(Parser.arbolito,arbol.hijos[0].token.value)# Busca el nodo de la función en el árbol sintáctico
  obtener_parametros(nodo_charlie.hijos[3],parametros)# Obtiene los parámetros de la función y de la llamada a la función
  obtener_parametros_lcharlie(arbol.hijos[1].hijos[1],parametros_lcharlie)
  if len(parametros) != len(parametros_lcharlie): # Verifica que la cantidad de parámetros coincida
    print("Error semántico en la línea "+ str(arbol.hijos[0].token.lineno) +": los parámentros no coinciden")
    errores = True
  else:
    for ra in range(len(parametros)):# Verifica que los tipos de parámetros coincidan
      if parametros[ra] != parametros_lcharlie[ra]:
        print("Error semántico en la línea "+ str(arbol.hijos[0].token.lineno) +": los parametros no coinciden")
        errores = True

def verificar_print(arbol):# Función para verificar la instrucción 'print' y su tipo de dato
  td_asignacion = verificar_tipo_Ex(arbol.hijos[2].hijos[0])# Verifica el tipo de la expresión dentro de 'print'
  arbol.hijos[2].tipo=td_asignacion


def eliminar_scope(scope):# Función para eliminar el ámbito actual de la tabla de símbolos
  #imprimir_tds(tabla_de_simbolos)
  #print("")
  for item in reversed(tabla_de_simbolos):# Elimina los símbolos asociados al ámbito actual de la tabla de símbolos
    if item.scope == scope:
      tabla_de_simbolos.pop(tabla_de_simbolos.index(item))
  #imprimir_tds(tabla_de_simbolos)
  #print("")
# Función para verificar el ámbito principal de la función 'pug'
def verificar_scope_pug(arbol):
  for subarbol in arbol.hijos:
    if subarbol.elemento=="FuncionPrincipal":
      verificar_scope(subarbol)
# Función principal para verificar el ámbito del código
def verificar_scope(arbol):
  global funcion_actual
  global n
  global funcion_actual_aux
  global es_while

  if arbol.elemento == "FuncionPrincipal":# Si es la función principal, actualiza la función actual
    funcion_actual="pug"
    funcion_actual_aux="pug"

  if arbol.elemento == "while":# Si es un bucle 'while', marca que está dentro de un 'while'
    es_while=True

  if len(arbol.hijos)>0 and arbol.hijos[0].elemento=="charlie":# Verifica la declaración de una función (charlie)
    n=0
    verificar_charlie(arbol)

  if arbol.elemento == "DeclaracionVariable":# Verifica la declaración de una variable
    verificar_declaracion_variable(arbol)
# Verifica la asignación de una variable
  if (arbol.elemento=="SentenciasWhile" or arbol.elemento == "Sentencias") and arbol.hijos[0].elemento=="identificador"and arbol.hijos[1].hijos[0].elemento=="igual":
    verificar_asignacion_de_variable(arbol)
# Verifica la llamada a una función (charlie)
  if (arbol.elemento=="SentenciasWhile" or arbol.elemento == "Sentencias" or arbol.elemento =="Tx") and arbol.hijos[0].elemento=="identificador"and arbol.hijos[1].hijos[0].elemento=="pizquierdo":
    verificar_llamar_charlie(arbol)
# Verifica la llamada a una variable
  if arbol.elemento == "Tx" and arbol.hijos[0].elemento == "identificador" and arbol.hijos[1].hijos[0].elemento == "''":
    verificar_llamar_variable(arbol)
# Verifica la instrucción 'print'
  if (arbol.elemento=="SentenciasWhile" or arbol.elemento == "Sentencias") and arbol.hijos[0].elemento == "print":
    verificar_print(arbol)
# Maneja los bloques de código con 'lizquierdo' y 'lderecho'
  if (arbol.elemento=="SentenciasWhile" or arbol.elemento == "Sentencias") and arbol.hijos[0].elemento=="lizquierdo":
    n=n+1
    funcion_actual= funcion_actual_aux + str(n)

  if arbol.elemento == "lderecho" and n==0:
    if es_while==True:
      es_while=False
    else:
      eliminar_scope(funcion_actual)

  if arbol.elemento == "lderecho" and n>0:
    if es_while==True:
      es_while=False
    else:
      n=n-1
      eliminar_scope(funcion_actual)
      if n!=0:
        funcion_actual= funcion_actual_aux + str(n)
      else:
        funcion_actual= funcion_actual_aux

  for subarbol in arbol.hijos:# Recurre sobre los hijos del nodo actual
    if subarbol.elemento!="FuncionPrincipal":
      verificar_scope(subarbol)
# Verifica el ámbito principal del código
verificar_scope(Parser.arbolito)
#print("Scope pug")
verificar_scope_pug(Parser.arbolito)# Verifica el ámbito de la función 'pug'
#print("Final")
#imprimir_tds(tabla_de_simbolos)
if errores == True:# Si hay errores, termina la ejecución
  raise SystemExit
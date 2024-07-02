import Semantico

print("⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡄⢠⡄⡠⠤⣖⣸⣦⡕⡀⠀⠀")
print("⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠐⠪⣁⣀⡈⠉⠙⠛⢾⣿⢿⢧⠀⠀")
print("⠀⠀⠀⠀⠀⠀⡠⠒⠀⢈⠒⢨⡱⠦⠍⢒⡻⠄⢀⣀⠉⢳⣿⣷⠀")
print("⠀⠀⠀⢀⠔⢬⣎⠉⡄⢸⠁⡠⠴⡀⢰⠁⢲⣶⣗⣿⣯⣦⠢⠙⠂")
print("⠀⠀⣰⡔⢀⣮⡿⡘⡜⠄⢀⠥⣀⠈⠮⠶⠶⠿⢿⣾⣿⣻⡆⢱⠀")
print("⠀⢸⣹⣦⣼⡿⠀⠡⢠⠔⣡⣴⣭⡇⢠⣴⡻⣿⠶⠤⣬⣝⠏⡈⡀         Todo")
print("⢀⣾⣿⣿⣿⣧⠀⢰⠑⣿⠿⣿⣿⠠⣯⣽⣻⢶⢙⣭⠈⠩⣵⠽⡇         Compiló")
print("⢿⣿⡿⠛⠛⣯⡀⠸⣸⡿⠿⢿⣹⢀⡿⣿⠅⢰⠛⠉⣻⣷⣠⣅⡇         Adecuadamente")
print("⠙⠻⣷⣴⣴⠣⡗⠀⠈⡝⠻⢋⣭⡾⡛⡙⢠⣧⣠⣶⣾⣿⣿⠛⠁")
print("⠀⠀⠀⠉⠉⢄⠡⡀⠀⠱⣀⠰⣸⠘⡐⡁⣾⣿⣿⡿⢟⠏⢸⠀⠀")
print("⠀⠀⠀⠀⠀⠀⠱⢘⠲⠄⣀⣈⡑⠷⢇⠾⠟⢫⠁⢀⠎⠠⠞⠀⠀")
# Sección de datos en ensamblador MIPS donde se define una cadena para nueva línea
data = ".data\n\nendl: .asciiz " + '"' + "\\n" + '"' + "\n"
total = 0
parametros = []

# Función que genera código para un nodo terminal
def generar_terminal(node_t):
  if node_t.elemento == "numero":
    return "li $a0 " + str(node_t.token.value) + "\n"
  elif node_t.elemento == "decimal":
    return "li $a0" + str(node_t.token.value) + "\n"

# Función que genera código para expresiones con operadores
def generar_Ex_prima(node_Ex_prima):
  resultado = ""
  if node_Ex_prima.hijos[0].elemento == "''":
    return ""
  elif node_Ex_prima.hijos[0].elemento == "Simbolo":
    resultado = "sw $a0 0($sp)\naddiu $sp $sp -4\n"# Guarda $a0 en la pila
    resultado += generar_Tx(node_Ex_prima.hijos[1])
    resultado += "lw $t1 4($sp)\n"# Carga el valor guardado en $t1, Manejo de operadores aritméticos
    if node_Ex_prima.hijos[0].hijos[0].elemento == "mas":
      resultado += "add $a0 $t1 $a0\naddiu $sp $sp 4\n"
    elif node_Ex_prima.hijos[0].hijos[0].elemento == "menos":
      resultado += "sub $a0 $t1 $a0\naddiu $sp $sp 4\n"
    elif node_Ex_prima.hijos[0].hijos[0].elemento == "por":
      resultado += "mul $a0 $t1 $a0\naddiu $sp $sp 4\n"
    elif node_Ex_prima.hijos[0].hijos[0].elemento == "dividir":
      resultado += "div $t1 $a0\n"
      resultado += "mflo $a0\n"
      resultado += "addiu $sp $sp 4\n"

    elif node_Ex_prima.hijos[0].hijos[0].elemento == "modulo":
      resultado += "div $t1 $a0\n"
      resultado += "mfhi $a0\n"
      resultado += "addiu $sp $sp 4\n"
    elif node_Ex_prima.hijos[0].hijos[0].elemento == "comparacion":
      resultado += "addiu $sp $sp 4\n"
    elif node_Ex_prima.hijos[0].hijos[0].elemento == "diferente":
      resultado += "addiu $sp $sp 4\n"
    resultado += generar_Ex_prima(node_Ex_prima.hijos[2])
  return resultado

# Función que obtiene la dirección de un parámetro en la pila
def obtener_id_parametro(valor):
  return (len(parametros) - parametros.index(valor)) * 4

# Función que genera código para expresiones simples o llamadas a función
def generar_Tx(node_Tx):
  resultado = ""
  if node_Tx.hijos[0].elemento == "Literal":
    resultado = generar_terminal(node_Tx.hijos[0].hijos[0])
  elif node_Tx.hijos[0].elemento == "identificador" and node_Tx.hijos[1].hijos[
      0].elemento == "''":
    if node_Tx.hijos[0].token.value in parametros:
      resultado = "lw $a0 " + str(
          obtener_id_parametro(node_Tx.hijos[0].token.value)) + "($fp)\n"
    else:
      resultado = "lw $a0 " + node_Tx.hijos[0].token.value + "\n"
  elif node_Tx.hijos[0].elemento == "identificador" and node_Tx.hijos[1].hijos[
      0].elemento != "''":
    resultado = generar_llamar_charlie(node_Tx)
  return resultado

# Función que combina la generación de una expresión simple y su parte recursiva
def generar_Tx_Ex_prima(node_Tx, node_Ex_prima):
  resultado = generar_Tx(node_Tx)
  resultado += generar_Ex_prima(node_Ex_prima)
  return resultado

# Función que genera el código completo para una expresión
def generar_ex(node_e):
  resultado = generar_Tx_Ex_prima(node_e.hijos[0], node_e.hijos[1])
  return resultado

# Función que genera el código para declarar una variable
def generar_variable(node):
  global data
  data += str(node.hijos[1].token.value) + ": .word	0:1\n"
  if node.hijos[3].hijos[0].elemento == "''":
    return ""
  else:
    return generar_ex(node.hijos[3].hijos[1].hijos[0]) + "sw $a0 " + str(
        node.hijos[1].token.value) + "\n"

# Función que genera el código para la asignación de una variable
def generar_asignacion_de_variable(arbol):
  codigo = generar_ex(arbol.hijos[1].hijos[1].hijos[0]) + "sw $a0 " + str(
      arbol.hijos[0].token.value) + "\n"
  return codigo

# Función que genera el código para un bucle 'while'
def generar_while(arbol):
  codigo = "label_loop:\n"
  codigo += generar_ex(arbol.hijos[2].hijos[0])
  codigo += "beq $a0 $t1 label_exit\n"
  codigo += generar_codigo(arbol.hijos[5])
  codigo += "j label_loop\n"
  codigo += "label_exit:\n"
  return codigo

# Función que genera el código para una estructura condicional 'if'
def generar_if(arbol):
  codigo = generar_ex(arbol.hijos[2].hijos[0])
  codigo += "beq $a0 $t1 label_true\n"
  codigo += "label_false:\n"
  codigo += generar_codigo(arbol.hijos[6])
  codigo += "b label_end\n"
  codigo += "label_true:\n"
  codigo += generar_codigo(arbol.hijos[4])
  codigo += "label_end:\n"
  return codigo

# Función que genera el código para una instrucción de retorno en una función
def generar_devuelve(arbol):
  codigo = ""
  if arbol.hijos[0].elemento != "''":
    codigo = generar_ex(arbol.hijos[1].hijos[0])
  return codigo


def generar_print(arbol):
  codigo = ""# Inicializamos una variable para almacenar el código generado
  if arbol.hijos[2].tipo == "entero":
    codigo = generar_ex(arbol.hijos[2].hijos[0])# Genera el valor de la expresión del entero y lo guarda en 'codigo'
    codigo += "li $v0 1\n"# Syscall para imprimir un entero (código de syscall 1 en $v0)
    codigo += "syscall\n"
    codigo += "li $v0 4\nla $a0 endl\nsyscall\n"# Syscall para imprimir una nueva línea
  if arbol.hijos[2].tipo == "flotante":
    codigo = generar_ex(arbol.hijos[2].hijos[0])
    #codigo += "lw $f12 $a0"
    codigo += "li $v0 2\n"
    codigo += "syscall\n"
    codigo += "li $v0 4\nla $a0 endl\nsyscall\n"
  return codigo


def generar_PL_prima(PL_prima):
  codigo = ""# Inicializa una cadena vacía para almacenar el código generado
  if PL_prima.hijos[0].elemento != "''":# Verifica si el primer hijo no es una cadena vacía
    codigo = generar_PL_PL_prima(PL_prima.hijos[1], PL_prima.hijos[2])# Genera el código para los parámetros adicionales
  return codigo


def generar_PL(PL):
  codigo = generar_ex(PL.hijos[0].hijos[0])# Genera el código para evaluar la expresión del primer parámetro
  codigo += "sw $a0 0($sp)\naddiu $sp $sp-4\n"# Almacena el valor de $a0 en el tope de la pila y actualiza el puntero de la pila
  return codigo


def generar_PL_PL_prima(PL, PL_prima):
  codigo = generar_PL(PL)# Genera el código para el primer parámetro
  codigo += generar_PL_prima(PL_prima)# Genera el código para los parámetros adicionales
  return codigo


def generar_parametros(arbol):
  codigo = generar_PL_PL_prima(arbol.hijos[0], arbol.hijos[1])# Genera el código para todos los parámetros usando la función auxiliar
  return codigo


def generar_llamar_charlie(arbol):
  codigo = "sw $fp 0($sp)\naddiu $sp $sp-4\n"# Guarda el frame pointer ($fp) en la pila y actualiza el puntero de la pila
  if arbol.hijos[1].hijos[1].hijos[0].elemento != "''":# Verifica si hay parámetros para la llamada a la función
    codigo += generar_parametros(arbol.hijos[1].hijos[1])# Genera el código para pasar los parámetros
  codigo += "jal " + arbol.hijos[0].token.value + "\n"# Genera el salto a la función especificada
  return codigo


def contar_Y(Y):
  global total
  total = total + 1# Incrementa el conteo total de parámetros
  parametros.append(Y.hijos[1].token.value)# Agrega el valor del parámetro a la lista de parámetros


def contar_Y_prima(Y_prima):
  if Y_prima.hijos[0].elemento != "''":# Verifica si el primer hijo no es una cadena vacía
    contar_Y(Y_prima.hijos[1])# Cuenta el parámetro y llama recursivamente para contar los parámetros adicionales
    contar_Y_prima(Y_prima.hijos[2])


def contar_parametros(arbol):
  global total
  total = 0 # Inicializa el conteo de parámetros en cero
  contar_Y(arbol.hijos[0])# Cuenta el primer parámetro y los adicionales
  contar_Y_prima(arbol.hijos[1])
  return total# Retorna el total de parámetros contados


def generar_charlie(arbol):
  num_param = 0
  if arbol.hijos[3].hijos[0].elemento != "''":# Verifica si la función tiene parámetros y cuenta el número de parámetros
    num_param = contar_parametros(arbol.hijos[3])
  codigo = arbol.hijos[1].token.value + ":\n"# Genera la etiqueta de la función
  codigo += "move $fp $sp\nsw $ra 0($sp)\naddiu $sp $sp -4\n"# al stack pointer ($sp), guarda la dirección de retorno ($ra) y actualiza el puntero de la pila
  codigo += generar_codigo(arbol.hijos[6])# Genera el código del cuerpo de la función
  codigo += "lw $ra 4($sp)\naddiu $sp $sp " + str(# Restaura ($ra) y el ($fp), y actualiza el puntero de la pila
      (4 * num_param) + 8) + "\nlw $fp 0($sp)\njr $ra"
  return codigo


def generar_pug(arbol):
  codigo = ""# Inicializa una cadena vacía para almacenar el código generado
  for subarbol in arbol.hijos:# Recorre los hijos del árbol y busca la función principal
    if subarbol.elemento == "FuncionPrincipal":
      codigo = generar_codigo(subarbol)# Genera el código para la función principal
  codigo += "li $v0 10\nsyscall\n"# Añade el código para finalizar el programa (syscall de salida)
  return codigo


def generar_codigo(arbol):
  codigo = ""
  if arbol.elemento == "FuncionPrincipal":
    codigo += "main:\n"
  if arbol.elemento == "DeclaracionVariable":
    codigo += generar_variable(arbol)
  if (arbol.elemento == "SentenciasWhile" or arbol.elemento
      == "Sentencias") and arbol.hijos[0].elemento == "print":
    codigo += generar_print(arbol)
  if arbol.elemento == "J":
    codigo += generar_devuelve(arbol)
  if (arbol.elemento == "SentenciasWhile" or arbol.elemento == "Sentencias"
      ) and arbol.hijos[0].elemento == "identificador" and arbol.hijos[
          1].hijos[0].elemento == "igual":
    codigo += generar_asignacion_de_variable(arbol)
  if ((arbol.elemento == "SentenciasWhile" or arbol.elemento == "Sentencias")
      and (arbol.hijos[0].elemento == "si" or arbol.hijos[0].elemento
           == "while")) or arbol.elemento == "DeclaracionFuncion":
    if arbol.hijos[0].elemento == "si":
      codigo += generar_if(arbol)
    elif arbol.elemento == "DeclaracionFuncion":
      codigo += generar_charlie(arbol)
    else:
      codigo += generar_while(arbol)
  else:
    for subarbol in arbol.hijos:
      if subarbol.elemento != "FuncionPrincipal":
        codigo += generar_codigo(subarbol)

  return codigo


codigo_text = generar_pug(Semantico.Parser.arbolito)
codigo_text += generar_codigo(Semantico.Parser.arbolito)
codigo = data + "\n.text\n\n" + codigo_text

file = open('codigo.s', 'w')# Escribe el código generado en un archivo de salida
file.write(codigo)
file.close()

import Lexer
import xlrd #leer excel
import pandas as pd
import numpy as np
from graphviz import Digraph
import arbol
import math
dot = Digraph()# Inicializa el objeto Digraph
filas = {"Inicio"	:1	,# Mapeo de no terminales
"E"	:2	,
"E'"	:3	,
"DeclaracionFuncion"	:4	,
"FuncionPrincipal"	:5	,
"K"	:6	,
"Parametros"	:7	,
"Y'"	:8	,
"Y"	:9	,
"TipoDato"	:10	,
"C"	:11	,
"CuerpoF"	:12	,
"J"	:13	,
"Cuerpo"	:14	,
"D'"	:15	,
"DeclaracionVariables"	:16	,
"Dc'"	:17	,
"Sentencias"	:18	,
"OPS"	:19	,
"MuchasSentenciasWhile"	:20	,
"M'"	:21	,
"SentenciasWhile"	:22	,
"MuchasSentencias"	:23	,
"S'"	:24	,
"DeclaracionVariable"	:25	,
"Corchetes"	:26	,
"OPI"	:27	,
"Expresion"	:28	,
"Ex"	:29	,
"Ex'"	:30	,
"Tx"	:31	,
"Literal"	:32	,
"Op"	:33	,
"ParaLLamados"	:34	,
"PL'"	:35	,
"PL"	:36	,
"Simbolo"	:37
}
columnas={"charlie"	:1	,# Mapeo de tokens
"identificador"	:2	,
"pizquierdo"	:3	,
"pderecho"	:4	,
"lizquierdo"	:5	,
"lderecho"	:6	,
"pug"	:7	,
"coma"	:8	,
"bool"	:9	,
"entero"	:10	,
"flotante"	:11	,
"texto"	:12	,
"caract"	:13	,
"cizquierdo"	:14	,
"cderecho"	:15	,
"devuelve"	:16	,
"si"	:17	,
"sino"	:18	,
"while"	:19	,
"print"	:20	,
"igual"	:21	,
"break"	:22	,
"lbool"	:23	,
"numero"	:24	,
"ltexto"	:25	,
"decimal"	:26	,
"lcaract"	:27	,
"true"	:28	,
"false"	:29	,
"mas"	:30	,
"menos"	:31	,
"por"	:32	,
"o"	:33	,
"y"	:34	,
"mayor_igual"	:35	,
"diferente"	:36	,
"menor_igual"	:37	,
"comparacion"	:38	,
"menor"	:39	,
"mayor"	:40	,
"modulo"	:41	,
"dividir"	:42	,
"$"	:43
}
df = pd.read_excel("mitabla.xlsx", 'Hoja1',  header=None)# Carga de la tabla parseo Excel.
mitabla_parse = df.values

pila = ["Inicio","$"]# Iniciar la pila
entrada = Lexer.tokens# Lista de entrada
entrada.append("$")#++ símbolo de fin de entrada.
pila_tokens = Lexer.tokens_info # Copia de los tokens para usar en la pila de tokens y manejo de errores.
linea_tokens = Lexer.tokens_info.copy()


# Inicialización de variables auxiliares para el procesamiento del árbol de análisis sintáctico.
continuar=True
i=0
j=0
p=0
aux=[]
pendientes=[]
arbolito = arbol.Arbol(pila[0],0)# Creación del nodo raíz del árbol y del objeto Digraph para visualización.
dot.node(str(j), pila[0])
padres=[0,-1]# Lista que mantiene los nodos padres en el árbol.
print("Inicio:")
#print(pila)
#print(entrada)

while continuar:#bucle principal parser
  #print("Vuelta",i)
  if pila[0]=="$" and entrada[0]=="$":# Verificar la condición de aceptación.
    continuar=False
    #print(pila)
    #print(entrada)
    print("La cadena ha sido aceptada :D")
  elif pila[0] == entrada[0]:# Si el tope de la pila y la entrada son iguales, los consumimos.
    #print(pila)
    #print(entrada)
    pila = pila[1:]
    entrada.pop(0)
    linea_tokens.pop(0)
  #si el tope de la pila y la entrada no coinciden y ambos son terminales, generamos un error.
  elif pila[0][0]==(pila[0][0]).lower() and entrada[0][0]==(entrada[0][0]).lower():
    continuar=False
    #print(pila)
    #print(entrada)
    print("Error sintáctico en la línea " + str(linea_tokens[0].lineno) + ": Cadena rechazada")
    raise SystemExit
  else:# Si no coinciden y no son terminales, expandimos el no terminal en la pila.
    if entrada[0] in columnas:
      reemplazo = mitabla_parse[filas[pila[0]]][columnas[entrada[0]]]
      p=int(padres[0])
    else:
      continuar=False
      #print(pila)
      #print(entrada)
      print("Error sintáctico en la línea " + str(linea_tokens[0].lineno) + ": Cadena rechazada")
      raise SystemExit
      break
    if reemplazo == "vacio":# Si la producción es "vacio", agregamos un nodo vacío y actualizamos la pila y los padres.
      j=j+1
      h=j
      dot.node(str(h), "''")
      dot.edge(str(p),str(h))
      arbolito.agregarhijo(arbolito,"''",p,h)
      pila=pila[1:]
      padres=padres[1:]
      #print(pila)
      #print(entrada)
    else:# Si no es "vacio", expandimos el no terminal y añadimos los nuevos nodos al árbol.
      if str(reemplazo) == 'nan':
        print("Error sintáctico en la línea " + str(linea_tokens[0].lineno) + ": Cadena rechazada")
        raise SystemExit
      array_aux=reemplazo.split()
      pila = np.concatenate((array_aux,pila[1:]),axis=0)
      hijos = len(array_aux)
      aux.clear()
      for e in range(hijos):
        j=j+1
        if array_aux[e][0]==array_aux[e][0].upper():
          aux.append(j)
          arbolito.agregarhijo(arbolito,array_aux[e],p,j)
        else:
          arbolito.agregarhijo(arbolito,array_aux[e],p,j)
        h=j
        dot.node(str(h), array_aux[e])
        dot.edge(str(p),str(h))
      padres = np.concatenate((aux,padres[1:]),axis=0)
      #print(pila)
      #print(entrada)
  i=i+1
print(dot.source)

arbol.recorrerArbol(arbolito,pila_tokens)
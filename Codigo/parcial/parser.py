import csv
import re

# Sintactic

# Clasificación de símbolos en terminales y no terminales
def clasificar_simbolos(reglas):
      no_terminales = set()
      simbolos_totales = set()
#itera cd regla
      for regla in reglas:
          izquierda, derecha = re.split(r'\s*->\s*', regla.strip()) #dividir regla I,D
          no_terminales.add(izquierda)
          simbolos_totales.update(derecha.split())

      return no_terminales, simbolos_totales - no_terminales


def load_rules(archivo):
  with open(archivo, 'r') as file:# Carga de reglas gramaticales desde un archivo
    reglas = [linea.strip() for linea in file if linea.strip()]
  return reglas


def cargar_primeros(archivo):
 primeros = {}
 with open(archivo, 'r') as file:#cargafirst desde archivo y devuelve diccionario clv ntrmles y vlres cjnts simb
    for linea in file:
        linea = linea.strip()
        if linea:
            no_terminal, elementos = linea.split(':')
            elementos = [elemento.strip() for elemento in elementos.split(',')]
            primeros[no_terminal.strip()] = set(elemento if elemento != "''" else 'ε' for elemento in elementos if elemento)
 return primeros

# Cálculo de conjuntos FIRST
def obtener_primeros(reglas):
 primeros = {}
 cambio = True

 no_terminales, terminales = clasificar_simbolos(reglas)
 for simbolo in no_terminales.union(terminales):
    primeros[simbolo] = set()
    if simbolo in terminales:
        primeros[simbolo].add(simbolo)

 while cambio:
    cambio = False
    for regla in reglas:
        izq, der = regla.split('->')
        izq = izq.strip()
        der = der.strip().split()

        first_original = primeros[izq].copy()
        puede_ser_vacio = True

        for simbolo in der:
            if not puede_ser_vacio:
                break

            primeros[izq].update(primeros[simbolo] - {EPSILON})

            if EPSILON not in primeros[simbolo]:
                puede_ser_vacio = False

        if puede_ser_vacio:
            primeros[izq].add(EPSILON)

        if primeros[izq] != first_original:
            cambio = True

 return primeros

# Cálculo de conjuntos FOLLOW

def obtener_siguientes(reglas, primeros, simbolo_inicio):
    siguientes = {no_terminal: set() for no_terminal in primeros}
    siguientes[simbolo_inicio].add('$')

    cambio = True
    while cambio:
        cambio = False
        for regla in reglas:
            partes = regla.split('->')
            if len(partes) < 2:
                continue
            izquierda = partes[0].strip()
            derecha = partes[1].strip().split()

            trailer = set(siguientes[izquierda])
            for i in reversed(range(len(derecha))):
                simbolo = derecha[i]
                if simbolo in siguientes:
                    antes_de_actualizar = len(siguientes[simbolo])
                    siguientes[simbolo].update(trailer)
                    if len(siguientes[simbolo]) > antes_de_actualizar:
                        cambio = True
                    if 'ε' in primeros.get(simbolo, set()):
                        trailer.update(x for x in primeros[simbolo] if x != 'ε')
                    else:
                        trailer = set(primeros.get(simbolo, set()))
                else:
                    if simbolo != 'ε':
                        trailer = {simbolo}
    return {k: v for k, v in siguientes.items() if v}


# Exprtr t LL1, cjnt FIRST  FOLLOW a archivos
def exportar_tablas_y_conjuntos(primeros, siguientes, archivo):
 with open(archivo, 'w') as file:
    for simbolo in sorted(primeros):
        conjunto_formateado = ', '.join(sorted(primeros[simbolo]))
        file.write(f"PRIMEROS({simbolo}): {conjunto_formateado}\n")
    for simbolo in sorted(siguientes):
        conjunto_formateado = ', '.join(sorted(siguientes[simbolo]))
        file.write(f"SIGUIENTES({simbolo}): {conjunto_formateado}\n")

 print(f"Conjuntos PRIMEROS y SIGUIENTES escritos en {archivo}")

EPSILON = "''"
terminales = set()

# Cargar conjuntos desde un archivo
def cargar_conjuntos(archivo):
    conjuntos = {}
    with open(archivo, 'r') as file:
        for linea in file:
            linea = linea.strip()
            if linea:
                no_terminal, elementos = linea.split(':')
                elementos = elementos.split(',')
                conjuntos[no_terminal.strip()] = set(e.strip() if e.strip() != "''" else '' for e in elementos if e.strip())
    return conjuntos

# read gram table from arch
def cargar_tabla_gramatica(archivo):
    reglas = {}
    nt_actual = None
    with open(archivo, 'r') as file:
        for linea in file:
            linea = linea.strip()
            if linea:
                if '->' in linea:
                    lhs, rhs = linea.split('->')
                    lhs, rhs = lhs.strip(), rhs.strip()
                    if lhs not in reglas:
                        reglas[lhs] = []
                    nt_actual = lhs
                    reglas[lhs].append(rhs.split())
                elif nt_actual:
                    # Continuación de las producciones del no-terminal anterior
                    reglas[nt_actual].append(linea.split())
    return reglas

# Construir tabla LL1
def construir_tabla_ll1(reglas, primeros, siguientes):
    terminales = set(termino for terminos in primeros.values() for termino in terminos if termino != '') | {'$'}
    no_terminales = set(reglas.keys())
    tabla = {nt: {t: [] for t in terminales} for nt in no_terminales}

    for nt, producciones in reglas.items():
        for produccion in producciones:
            primer = calcular_primero_de_secuencia(produccion, primeros)
            for simbolo in primer - {''}:
                tabla[nt][simbolo].append(produccion)
            if '' in primer:
                for simbolo in siguientes[nt]:
                    tabla[nt][simbolo].append(produccion)

    return tabla

# Calcular FIRST de una secuencia
def calcular_primero_de_secuencia(secuencia, primeros):
    resultado = set()
    for simbolo in secuencia:
        resultado.update(primeros.get(simbolo, {simbolo}))
        if '' not in primeros.get(simbolo, {}):
            resultado.discard('')
            break
    else:
        resultado.add('')
    return resultado

# Imprimir tabla LL1 a archivo
def imprimir_tabla_ll1(tabla, archivo):
    with open(archivo, 'w') as file:
        for nt, fila in tabla.items():
            file.write(f"FOLLOW({nt}):\n")
            for terminal, producciones in fila.items():
                if producciones:
                    cadena_producciones = ' | '.join(' '.join(prod) for prod in producciones)
                    file.write(f"  {terminal}: {cadena_producciones}\n")
                else:
                    file.write(f"  {terminal}: error\n")

# Escribir conjuntos FIRST y FOLLOW a archivo
def escribir_conjuntos_archivo(conjuntos, archivo, tipo_conjunto):
    with open(archivo, 'w') as file:
        for simbolo in sorted(conjuntos):
            conjunto_formateado = ', '.join(sorted(conjuntos[simbolo]))
            file.write(f"{simbolo}: {conjunto_formateado}\n")

    print(f"Conjuntos de {tipo_conjunto} escritos en {archivo}")

EPSILON = "''"  # def const epsilon
terminales = set()

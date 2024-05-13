import csv
import re


# Clasificación de símbolos en terminales y no terminales
def clasificar_simbolos(reglas):
      no_terminales = set()
      simbolos_totales = set()

      for regla in reglas:
          izquierda, derecha = re.split(r'\s*->\s*', regla.strip())
          no_terminales.add(izquierda)
          simbolos_totales.update(derecha.split())

      return no_terminales, simbolos_totales - no_terminales

# Carga de reglas gramaticales desde un archivo
def cargar_reglas(archivo):
  with open(archivo, 'r') as file:
    reglas = [linea.strip() for linea in file if linea.strip()]
  return reglas

# Carga de conjuntos FIRST desde archivo
def cargar_primeros(archivo):
 primeros = {}
 with open(archivo, 'r') as file:
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
siguientes = {no_terminal: set() for no_terminal in primeros}  #siguientes de cada no terminal
siguientes[simbolo_inicio].add('$')  #símbolo de fin de cadena al FOLLOW del símbolo de inicio

cambio = True
while cambio:
    cambio = False
    for regla in reglas:
        izquierda, derecha = regla.split('->')
        izquierda = izquierda.strip()
        derecha = derecha.strip().split()

        trailer = set(siguientes[izquierda])
        for i in reversed(range(len(derecha))):
            simbolo = derecha[i]
            if simbolo in siguientes:
                # Antes de actualizar los FOLLOW del símbolo, guarda su tamaño anterior para verificar cambios
                antes_de_actualizar = len(siguientes[simbolo])
                siguientes[simbolo].update(trailer)
                #FOLLOW ha cambiado, marca que hubo un cambio y se necesita otra iteración
                if len(siguientes[simbolo]) > antes_de_actualizar:
                    cambio = True

                # Actualiza el trailer para el próximo símbolo en la producción
                if 'ε' in primeros[simbolo]:
                    trailer.update(x for x in primeros[simbolo] if x != 'ε')
                else:
                    trailer = set(primeros[simbolo])
            else:
                if simbolo != 'ε':
                    trailer = {simbolo}

return {k: v for k, v in siguientes.items() if v}


# Exportar tablas LL1, conjuntos FIRST y FOLLOW a archivos
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

# Leer tabla de gramática desde archivo
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

EPSILON = "''"  # Asegurando consistencia en la representación de EPSILON
terminales = set()

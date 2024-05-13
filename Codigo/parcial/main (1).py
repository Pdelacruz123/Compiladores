import ply.lex as lex
import lexer  
import parser

def main():
    
    with open('PRUEBA.txt', 'r') as file:
        data = file.read()

    
    my_lexer = lex.lex(module=lexer)

    
    my_lexer.input(data)

    
    tokens_list = []

    
    while True:
        tok = my_lexer.token()
        if not tok:
            break
        
        tokens_list.append({
            'type': tok.type,
            'value': tok.value,
            'line': tok.lineno,
            'position': tok.lexpos
        })

    
    with open("ingresarLL1.txt", "w") as f:
        for token in tokens_list:
            f.write(f"{token['type']} ")
        f.write("$\n")  

    print("Análisis léxico completado. Revisa el archivo 'ingresarLL1.txt' para ver los resultados.")


archivo_gramatica = 'gramaticaLL1.txt'
reglas = parser.cargar_reglas(archivo_gramatica)
simbolo_inicio = reglas[0].split('->')[0].strip()  


primeros = parser.obtener_primeros(reglas)


if '' in primeros:
    del primeros['']


parser.escribir_conjuntos_archivo(primeros, 'first.txt', 'FIRST')


primeros_desde_archivo = parser.cargar_primeros('first.txt')
siguientes = parser.obtener_siguientes(reglas, primeros_desde_archivo, simbolo_inicio)
parser.escribir_conjuntos_archivo(siguientes, 'follow.txt', 'FOLLOW')

archivo_primeros = 'first.txt'
archivo_siguientes = 'follow.txt'

reglas_T = parser.cargar_tabla_gramatica(archivo_gramatica)
primeros_T = parser.cargar_conjuntos(archivo_primeros)
siguientes_T = parser.cargar_conjuntos(archivo_siguientes)

tabla_ll1 = parser.construir_tabla_ll1(reglas_T, primeros_T, siguientes_T)
archivo_salida = 'll1_table.txt'
parser.imprimir_tabla_ll1(tabla_ll1, archivo_salida)
print(f"Tabla de análisis LL(1) escrita en {archivo_salida}")


if __name__ == '__main__':
    main()

import ply.lex as lex
import lexer  
import parser

def main():

    with open('PRUEBA.txt', 'r') as file:
        data = file.read()
    my_lexer = lex.lex(module=lexer) #crealexer
    my_lexer.input(data)
    tokens_list = []
    
    for tok in my_lexer:  # itera tokens por my_lexer inforelevante de cada token a tokens_list.
        tokens_list.append({
        'type': tok.type,
        'value': tok.value,
        'line': tok.lineno,
        'position': tok.lexpos
    })



    with open("INGRESELL1.txt", "w") as f: #escribe tipos de token
        for token in tokens_list:
            f.write(f"{token['type']} ")
        f.write("$\n")  

    #lista de tokens validos
    print("El analisis ha terminado. Compruebe el archivo 'INGRESELL1.txt'.")


archivo_gramatica = 'GRAMMARLL1.txt' #carga reglas
reglas = parser.load_rules(archivo_gramatica)
simbolo_inicio = reglas[0].split('->')[0].strip()  
#simb reglas 

primeros = parser.obtener_primeros(reglas)

#calc cjnts de primeros
if '' in primeros:
    del primeros['']


parser.escribir_conjuntos_archivo(primeros, 'first.txt', 'FIRST')
#info de los cjnts

primeros_desde_archivo = parser.cargar_primeros('first.txt') #carga
siguientes = parser.obtener_siguientes(reglas, primeros_desde_archivo, simbolo_inicio) #calc follow $ntrmnal
parser.escribir_conjuntos_archivo(siguientes, 'follow.txt', 'FOLLOW') #info

archivo_primeros = 'first.txt' #namefiles
archivo_siguientes = 'follow.txt'

reglas_T = parser.cargar_tabla_gramatica(archivo_gramatica)
primeros_T = parser.cargar_conjuntos(archivo_primeros) #carga gram ->tabla
siguientes_T = parser.cargar_conjuntos(archivo_siguientes)
tabla_ll1 = parser.construir_tabla_ll1(reglas_T, primeros_T, siguientes_T)

archivo_salida = 'll1_table.txt'
parser.imprimir_tabla_ll1(tabla_ll1, archivo_salida) #ll1 escribe
print(f"Tabla de análisis LL(1) escrita en {archivo_salida}")


if __name__ == '__main__':
    main()

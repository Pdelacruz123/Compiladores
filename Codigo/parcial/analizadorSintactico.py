import csv

class NodoArbol:
    def __init__(self, valor, hijos=None):
        self.valor = valor
        self.hijos = hijos if hijos is not None else []

def cargarGramaticacsv(archivo):
    gramatica = {}
    terminales = set()  # Usar un conjunto para evitar duplicados
    with open(archivo, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Saltar la cabecera
        for row in csv_reader:
            no_terminal = row[0]
            producciones = [p.strip().split() for p in row[1:] if p.strip()]  # Asegurarse de que las celdas no estén vacías
            gramatica[no_terminal] = producciones
            for produccion in producciones:
                for symbol in produccion:
                    if symbol.isupper():  # Asumiendo que los terminales están en mayúsculas
                        terminales.add(symbol)
    terminales.add('$')  # Añadir el símbolo de fin de archivo
    return gramatica, list(terminales)

def main():
    archivo_csv = 'll1_table.csv'
    gramatica, terminales = cargarGramaticacsv(archivo_csv)
    print("Gramática cargada:", gramatica)
    print("Terminales detectados:", terminales)

if __name__ == '__main__':
    main()

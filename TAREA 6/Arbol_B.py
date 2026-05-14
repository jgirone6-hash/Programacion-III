import csv
from graphviz import Digraph


class NodoB:
    def __init__(self, hoja=True):
        # Lista de claves dentro del nodo
        self.claves = []

        # Lista de hijos del nodo
        self.hijos = []

        # Indica si el nodo es hoja o no
        self.hoja = hoja


class ArbolB:
    def __init__(self, grado):
        # El grado mínimo debe ser 2
        if grado < 2:
            raise ValueError("El grado del Árbol B debe ser mayor o igual a 2")

        # Grado mínimo del árbol
        self.grado = grado

        # Se crea la raíz vacía
        self.raiz = NodoB(True)

    def buscar(self, clave, nodo=None):
        # Si no se envía nodo, se empieza desde la raíz
        if nodo is None:
            nodo = self.raiz

        i = 0

        # Avanza mientras la clave buscada sea mayor que las claves del nodo
        while i < len(nodo.claves) and clave > nodo.claves[i]:
            i += 1

        # Si encuentra la clave, retorna True
        if i < len(nodo.claves) and clave == nodo.claves[i]:
            return True

        # Si es hoja y no encontró la clave, retorna False
        if nodo.hoja:
            return False

        # Busca en el hijo correspondiente
        return self.buscar(clave, nodo.hijos[i])

    def insertar(self, clave):
        # Si la clave ya existe, no se vuelve a insertar
        if self.buscar(clave):
            print(f"La clave {clave} ya existe. No se insertó nuevamente.")
            return

        raiz = self.raiz

        # Si la raíz está llena, se debe dividir
        if len(raiz.claves) == (2 * self.grado) - 1:
            nueva_raiz = NodoB(False)

            # La raíz anterior pasa a ser hijo de la nueva raíz
            nueva_raiz.hijos.append(raiz)

            # Se divide la raíz anterior
            self.dividir_hijo(nueva_raiz, 0)

            # Se inserta la clave en la nueva raíz
            self.insertar_no_lleno(nueva_raiz, clave)

            # Se actualiza la raíz del árbol
            self.raiz = nueva_raiz
        else:
            # Si la raíz no está llena, se inserta normalmente
            self.insertar_no_lleno(raiz, clave)

    def insertar_no_lleno(self, nodo, clave):
        i = len(nodo.claves) - 1

        # Si el nodo es hoja, se inserta la clave en orden
        if nodo.hoja:
            nodo.claves.append(None)

            while i >= 0 and clave < nodo.claves[i]:
                nodo.claves[i + 1] = nodo.claves[i]
                i -= 1

            nodo.claves[i + 1] = clave
        else:
            # Busca el hijo donde se debe insertar la clave
            while i >= 0 and clave < nodo.claves[i]:
                i -= 1

            i += 1

            # Si el hijo está lleno, se divide antes de insertar
            if len(nodo.hijos[i].claves) == (2 * self.grado) - 1:
                self.dividir_hijo(nodo, i)

                if clave > nodo.claves[i]:
                    i += 1

            self.insertar_no_lleno(nodo.hijos[i], clave)

    def dividir_hijo(self, padre, indice):
        grado = self.grado

        hijo_lleno = padre.hijos[indice]
        nuevo_hijo = NodoB(hijo_lleno.hoja)

        # La clave del medio sube al padre
        clave_media = hijo_lleno.claves[grado - 1]

        # El nuevo hijo recibe las claves de la derecha
        nuevo_hijo.claves = hijo_lleno.claves[grado:]

        # El hijo original conserva las claves de la izquierda
        hijo_lleno.claves = hijo_lleno.claves[:grado - 1]

        # Si no es hoja, también se dividen los hijos
        if not hijo_lleno.hoja:
            nuevo_hijo.hijos = hijo_lleno.hijos[grado:]
            hijo_lleno.hijos = hijo_lleno.hijos[:grado]

        # Se inserta la clave media en el padre
        padre.claves.insert(indice, clave_media)

        # Se agrega el nuevo hijo al padre
        padre.hijos.insert(indice + 1, nuevo_hijo)

    def eliminar(self, clave):
        self.eliminar_de_nodo(self.raiz, clave)

        # Si la raíz queda sin claves y tiene hijos, se baja un nivel
        if len(self.raiz.claves) == 0 and not self.raiz.hoja:
            self.raiz = self.raiz.hijos[0]

    def eliminar_de_nodo(self, nodo, clave):
        grado = self.grado
        indice = 0

        # Busca la posición donde puede estar la clave
        while indice < len(nodo.claves) and clave > nodo.claves[indice]:
            indice += 1

        # Caso 1: la clave está en este nodo
        if indice < len(nodo.claves) and nodo.claves[indice] == clave:

            # Si es hoja, simplemente se elimina
            if nodo.hoja:
                nodo.claves.pop(indice)
            else:
                self.eliminar_de_nodo_interno(nodo, clave, indice)

        # Caso 2: la clave no está en este nodo
        else:
            # Si es hoja, la clave no existe
            if nodo.hoja:
                print(f"La clave {clave} no existe en el árbol.")
                return

            # Verifica si la clave debería estar en el último hijo
            ultimo = indice == len(nodo.claves)

            # Si el hijo tiene pocas claves, se rellena antes de bajar
            if len(nodo.hijos[indice].claves) < grado:
                self.rellenar(nodo, indice)

            # Después de rellenar, puede cambiar la posición del hijo
            if ultimo and indice > len(nodo.claves):
                self.eliminar_de_nodo(nodo.hijos[indice - 1], clave)
            else:
                self.eliminar_de_nodo(nodo.hijos[indice], clave)

    def eliminar_de_nodo_interno(self, nodo, clave, indice):
        grado = self.grado

        # Si el hijo izquierdo tiene suficientes claves
        if len(nodo.hijos[indice].claves) >= grado:
            predecesor = self.obtener_predecesor(nodo, indice)
            nodo.claves[indice] = predecesor
            self.eliminar_de_nodo(nodo.hijos[indice], predecesor)

        # Si el hijo derecho tiene suficientes claves
        elif len(nodo.hijos[indice + 1].claves) >= grado:
            sucesor = self.obtener_sucesor(nodo, indice)
            nodo.claves[indice] = sucesor
            self.eliminar_de_nodo(nodo.hijos[indice + 1], sucesor)

        # Si ambos hijos tienen pocas claves, se fusionan
        else:
            self.fusionar(nodo, indice)
            self.eliminar_de_nodo(nodo.hijos[indice], clave)

    def obtener_predecesor(self, nodo, indice):
        actual = nodo.hijos[indice]

        # El predecesor es la clave más grande del subárbol izquierdo
        while not actual.hoja:
            actual = actual.hijos[-1]

        return actual.claves[-1]

    def obtener_sucesor(self, nodo, indice):
        actual = nodo.hijos[indice + 1]

        # El sucesor es la clave más pequeña del subárbol derecho
        while not actual.hoja:
            actual = actual.hijos[0]

        return actual.claves[0]

    def rellenar(self, nodo, indice):
        # Si el hermano izquierdo puede prestar una clave
        if indice != 0 and len(nodo.hijos[indice - 1].claves) >= self.grado:
            self.prestar_del_anterior(nodo, indice)

        # Si el hermano derecho puede prestar una clave
        elif indice != len(nodo.claves) and len(nodo.hijos[indice + 1].claves) >= self.grado:
            self.prestar_del_siguiente(nodo, indice)

        # Si no pueden prestar, se fusiona
        else:
            if indice != len(nodo.claves):
                self.fusionar(nodo, indice)
            else:
                self.fusionar(nodo, indice - 1)

    def prestar_del_anterior(self, nodo, indice):
        hijo = nodo.hijos[indice]
        hermano = nodo.hijos[indice - 1]

        # Baja una clave del padre al hijo
        hijo.claves.insert(0, nodo.claves[indice - 1])

        # Si no es hoja, también se mueve el último hijo del hermano
        if not hijo.hoja:
            hijo.hijos.insert(0, hermano.hijos.pop())

        # Sube una clave del hermano al padre
        nodo.claves[indice - 1] = hermano.claves.pop()

    def prestar_del_siguiente(self, nodo, indice):
        hijo = nodo.hijos[indice]
        hermano = nodo.hijos[indice + 1]

        # Baja una clave del padre al hijo
        hijo.claves.append(nodo.claves[indice])

        # Si no es hoja, también se mueve el primer hijo del hermano
        if not hijo.hoja:
            hijo.hijos.append(hermano.hijos.pop(0))

        # Sube una clave del hermano al padre
        nodo.claves[indice] = hermano.claves.pop(0)

    def fusionar(self, nodo, indice):
        hijo = nodo.hijos[indice]
        hermano = nodo.hijos[indice + 1]

        # La clave del padre baja al hijo
        hijo.claves.append(nodo.claves.pop(indice))

        # Se agregan las claves del hermano
        hijo.claves.extend(hermano.claves)

        # Si no es hoja, también se agregan sus hijos
        if not hijo.hoja:
            hijo.hijos.extend(hermano.hijos)

        # Se elimina el hermano del padre
        nodo.hijos.pop(indice + 1)

    def cargar_csv(self, ruta_archivo):
        try:
            with open(ruta_archivo, "r", encoding="utf-8") as archivo:
                lector = csv.reader(archivo)

                # Se salta el encabezado
                next(lector, None)

                contador = 0

                for fila in lector:
                    if len(fila) > 0:
                        try:
                            clave = int(fila[0])
                            self.insertar(clave)
                            contador += 1
                        except ValueError:
                            print(f"Valor inválido ignorado: {fila[0]}")

                print(f"Se cargaron {contador} registros desde {ruta_archivo}")

        except FileNotFoundError:
            print("No se encontró el archivo. Verifica la ruta.")

    def mostrar(self, nodo=None, nivel=0):
        if nodo is None:
            nodo = self.raiz

        print("Nivel", nivel, ":", nodo.claves)

        if not nodo.hoja:
            for hijo in nodo.hijos:
                self.mostrar(hijo, nivel + 1)

    def graficar(self, nombre_archivo="arbol_b"):
        dot = Digraph(comment="Árbol B")
        dot.attr(rankdir="TB")

        contador = [0]

        def agregar_nodo(nodo):
            id_nodo = str(contador[0])
            contador[0] += 1

            etiqueta = "|".join(str(clave) for clave in nodo.claves)
            dot.node(id_nodo, etiqueta, shape="record")

            for hijo in nodo.hijos:
                id_hijo = agregar_nodo(hijo)
                dot.edge(id_nodo, id_hijo)

            return id_nodo

        agregar_nodo(self.raiz)

        dot.render(nombre_archivo, format="png", cleanup=True)
        print(f"Imagen generada correctamente: {nombre_archivo}.png")


def menu():
    print("======================================")
    print("        PROGRAMA DE ÁRBOL B")
    print("======================================")

    grado = int(input("Ingrese el grado mínimo del Árbol B: "))
    arbol = ArbolB(grado)

    while True:
        print("\n========== MENÚ ==========")
        print("1. Insertar clave")
        print("2. Buscar clave")
        print("3. Eliminar clave")
        print("4. Cargar datos desde CSV")
        print("5. Mostrar árbol en consola")
        print("6. Generar imagen con Graphviz")
        print("7. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            clave = int(input("Ingrese la clave a insertar: "))
            arbol.insertar(clave)
            print("Clave insertada correctamente.")

        elif opcion == "2":
            clave = int(input("Ingrese la clave a buscar: "))

            if arbol.buscar(clave):
                print("La clave sí existe en el árbol.")
            else:
                print("La clave no existe en el árbol.")

        elif opcion == "3":
            clave = int(input("Ingrese la clave a eliminar: "))
            arbol.eliminar(clave)
            print("Proceso de eliminación finalizado.")

        elif opcion == "4":
            print("Ejemplo de ruta: datos1.csv")
            ruta = input("Ingrese la ruta del archivo CSV: ")
            arbol.cargar_csv(ruta)

        elif opcion == "5":
            arbol.mostrar()

        elif opcion == "6":
            nombre = input("Ingrese el nombre de la imagen sin extensión: ")
            arbol.graficar(nombre)

        elif opcion == "7":
            print("Programa finalizado.")
            break

        else:
            print("Opción inválida. Intente nuevamente.")


if __name__ == "__main__":
    menu()

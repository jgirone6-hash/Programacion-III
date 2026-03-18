from graphviz import Digraph
import os


class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierda = None
        self.derecha = None


class ArbolBinarioBusqueda:
    def __init__(self):
        self.raiz = None

    def insertar(self, valor):
        if self.raiz is None:
            self.raiz = Nodo(valor)
        else:
            self._insertar_rec(self.raiz, valor)

    def _insertar_rec(self, nodo, valor):
        if valor < nodo.valor:
            if nodo.izquierda is None:
                nodo.izquierda = Nodo(valor)
            else:
                self._insertar_rec(nodo.izquierda, valor)
        elif valor > nodo.valor:
            if nodo.derecha is None:
                nodo.derecha = Nodo(valor)
            else:
                self._insertar_rec(nodo.derecha, valor)
        else:
            print(f"El valor {valor} ya existe en el árbol.")

    def buscar(self, valor):
        return self._buscar_rec(self.raiz, valor)

    def _buscar_rec(self, nodo, valor):
        if nodo is None:
            return False
        if valor == nodo.valor:
            return True
        elif valor < nodo.valor:
            return self._buscar_rec(nodo.izquierda, valor)
        else:
            return self._buscar_rec(nodo.derecha, valor)

    def eliminar(self, valor):
        self.raiz = self._eliminar_rec(self.raiz, valor)

    def _eliminar_rec(self, nodo, valor):
        if nodo is None:
            return nodo

        if valor < nodo.valor:
            nodo.izquierda = self._eliminar_rec(nodo.izquierda, valor)
        elif valor > nodo.valor:
            nodo.derecha = self._eliminar_rec(nodo.derecha, valor)
        else:
            if nodo.izquierda is None and nodo.derecha is None:
                return None

            if nodo.izquierda is None:
                return nodo.derecha

            if nodo.derecha is None:
                return nodo.izquierda

            sucesor = self._minimo(nodo.derecha)
            nodo.valor = sucesor.valor
            nodo.derecha = self._eliminar_rec(nodo.derecha, sucesor.valor)

        return nodo

    def _minimo(self, nodo):
        actual = nodo
        while actual.izquierda is not None:
            actual = actual.izquierda
        return actual

    def inorden(self):
        elementos = []
        self._inorden_rec(self.raiz, elementos)
        return elementos

    def _inorden_rec(self, nodo, elementos):
        if nodo is not None:
            self._inorden_rec(nodo.izquierda, elementos)
            elementos.append(nodo.valor)
            self._inorden_rec(nodo.derecha, elementos)

    def cargar_desde_archivo(self, ruta):
        carpeta_script = os.path.dirname(os.path.abspath(__file__))
        ruta_completa = os.path.join(carpeta_script, ruta)

        if not os.path.exists(ruta_completa):
            print("El archivo no existe.")
            print("Ruta buscada:", ruta_completa)
            return False

        try:
            with open(ruta_completa, "r", encoding="utf-8") as archivo:
                contenido = archivo.read().strip()

                if not contenido:
                    print("El archivo está vacío.")
                    return False

                contenido = contenido.replace("\n", ",").replace(" ", ",")
                partes = [x.strip() for x in contenido.split(",") if x.strip() != ""]

                for parte in partes:
                    self.insertar(int(parte))

            print("Datos cargados correctamente al árbol.")
            return True

        except ValueError:
            print("Error: el archivo contiene datos que no son números enteros.")
            return False
        except Exception as e:
            print(f"Ocurrió un error al leer el archivo: {e}")
            return False

    def graficar(self, nombre_archivo="arbol_binario"):
        if self.raiz is None:
            print("El árbol está vacío. No hay nada que graficar.")
            return

        dot = Digraph(comment="Árbol Binario de Búsqueda")
        dot.attr("node", shape="circle")

        self._graficar_rec(dot, self.raiz)

        carpeta_script = os.path.dirname(os.path.abspath(__file__))
        salida = os.path.join(carpeta_script, nombre_archivo)

        dot.render(salida, format="png", cleanup=True)
        print(f"Árbol generado correctamente en: {salida}.png")

    def _graficar_rec(self, dot, nodo):
        if nodo is not None:
            dot.node(str(nodo.valor), str(nodo.valor))

            if nodo.izquierda is not None:
                dot.edge(str(nodo.valor), str(nodo.izquierda.valor))
                self._graficar_rec(dot, nodo.izquierda)

            if nodo.derecha is not None:
                dot.edge(str(nodo.valor), str(nodo.derecha.valor))
                self._graficar_rec(dot, nodo.derecha)


def menu():
    arbol = ArbolBinarioBusqueda()

    while True:
        print("\n====== MENÚ ÁRBOL BINARIO DE BÚSQUEDA ======")
        print("1. Insertar número")
        print("2. Buscar número")
        print("3. Eliminar número")
        print("4. Cargar desde archivo")
        print("5. Mostrar recorrido inorden")
        print("6. Generar imagen Graphviz")
        print("7. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            try:
                valor = int(input("Ingrese el número a insertar: "))
                arbol.insertar(valor)
                print(f"Se insertó {valor} correctamente.")
                arbol.graficar()
            except ValueError:
                print("Debe ingresar un número entero.")

        elif opcion == "2":
            try:
                valor = int(input("Ingrese el número a buscar: "))
                if arbol.buscar(valor):
                    print(f"El número {valor} sí existe en el árbol.")
                else:
                    print(f"El número {valor} no existe en el árbol.")
            except ValueError:
                print("Debe ingresar un número entero.")

        elif opcion == "3":
            try:
                valor = int(input("Ingrese el número a eliminar: "))
                if arbol.buscar(valor):
                    arbol.eliminar(valor)
                    print(f"El número {valor} fue eliminado.")
                    arbol.graficar()
                else:
                    print(f"El número {valor} no existe en el árbol.")
            except ValueError:
                print("Debe ingresar un número entero.")

        elif opcion == "4":
            ruta = input("Ingrese la ruta del archivo (.csv o .txt): ")
            nuevo_arbol = ArbolBinarioBusqueda()

            if nuevo_arbol.cargar_desde_archivo(ruta):
                arbol = nuevo_arbol
                arbol.graficar()

        elif opcion == "5":
            print("Recorrido inorden:", arbol.inorden())

        elif opcion == "6":
            arbol.graficar()

        elif opcion == "7":
            print("Saliendo del programa...")
            break

        else:
            print("Opción inválida. Intente de nuevo.")


if __name__ == "__main__":
    menu()
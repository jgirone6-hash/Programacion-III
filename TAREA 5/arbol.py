import csv  # Se importa csv para leer archivos CSV.
import time  # Se importa time para medir tiempos de ejecución.
from graphviz import Digraph  # Se importa Digraph para generar la visualización del árbol.


class Nodo:  # Clase que representa cada nodo del árbol.
    def __init__(self, valor):  # Constructor que recibe el valor del nodo.
        self.valor = valor  # Guarda el valor del nodo.
        self.izquierda = None  # Apunta al hijo izquierdo.
        self.derecha = None  # Apunta al hijo derecho.


class ArbolBinarioBusqueda:  # Clase principal del árbol binario de búsqueda.
    def __init__(self):  # Constructor del árbol.
        self.raiz = None  # La raíz inicia vacía.
        self.tamano = 0  # Guarda la cantidad de elementos únicos en el árbol.

    def insertar(self, valor):  # Método público para insertar un valor.
        if not self.buscar(valor):  # Solo inserta si el valor no existe.
            if self.raiz is None:  # Si el árbol está vacío.
                self.raiz = Nodo(valor)  # El nuevo nodo será la raíz.
            else:  # Si ya existe raíz.
                self._insertar_rec(self.raiz, valor)  # Inserta recursivamente.
            self.tamano += 1  # Aumenta el contador de elementos.

    def _insertar_rec(self, nodo, valor):  # Método recursivo de inserción.
        if valor < nodo.valor:  # Si el valor es menor que el nodo actual.
            if nodo.izquierda is None:  # Si no existe hijo izquierdo.
                nodo.izquierda = Nodo(valor)  # Crea el hijo izquierdo.
            else:  # Si sí existe hijo izquierdo.
                self._insertar_rec(nodo.izquierda, valor)  # Continúa por la izquierda.
        elif valor > nodo.valor:  # Si el valor es mayor que el nodo actual.
            if nodo.derecha is None:  # Si no existe hijo derecho.
                nodo.derecha = Nodo(valor)  # Crea el hijo derecho.
            else:  # Si sí existe hijo derecho.
                self._insertar_rec(nodo.derecha, valor)  # Continúa por la derecha.

    def buscar(self, valor):  # Método público para buscar un valor.
        return self._buscar_rec(self.raiz, valor)  # Llama al método recursivo desde la raíz.

    def _buscar_rec(self, nodo, valor):  # Método recursivo de búsqueda.
        if nodo is None:  # Si no hay nodo.
            return False  # El valor no existe.

        if valor == nodo.valor:  # Si el valor coincide con el nodo actual.
            return True  # Sí existe.

        elif valor < nodo.valor:  # Si el valor es menor.
            return self._buscar_rec(nodo.izquierda, valor)  # Busca por la izquierda.

        else:  # Si el valor es mayor.
            return self._buscar_rec(nodo.derecha, valor)  # Busca por la derecha.

    def eliminar(self, valor):  # Método público para eliminar un valor.
        if self.buscar(valor):  # Solo elimina si el valor sí existe.
            self.raiz = self._eliminar_rec(self.raiz, valor)  # Elimina desde la raíz.
            self.tamano -= 1  # Disminuye el contador.

    def _eliminar_rec(self, nodo, valor):  # Método recursivo de eliminación.
        if nodo is None:  # Si el nodo no existe.
            return nodo  # No hay nada que eliminar.

        if valor < nodo.valor:  # Si el valor es menor que el nodo actual.
            nodo.izquierda = self._eliminar_rec(nodo.izquierda, valor)  # Busca y elimina por la izquierda.

        elif valor > nodo.valor:  # Si el valor es mayor que el nodo actual.
            nodo.derecha = self._eliminar_rec(nodo.derecha, valor)  # Busca y elimina por la derecha.

        else:  # Si encontró el nodo a eliminar.
            if nodo.izquierda is None and nodo.derecha is None:  # Caso 1: no tiene hijos.
                return None  # El nodo desaparece.

            if nodo.izquierda is None:  # Caso 2: solo tiene hijo derecho.
                return nodo.derecha  # Se reemplaza por el hijo derecho.

            if nodo.derecha is None:  # Caso 3: solo tiene hijo izquierdo.
                return nodo.izquierda  # Se reemplaza por el hijo izquierdo.

            sucesor = self._minimo(nodo.derecha)  # Busca el sucesor inorden.
            nodo.valor = sucesor.valor  # Copia el valor del sucesor.
            nodo.derecha = self._eliminar_rec(nodo.derecha, sucesor.valor)  # Elimina el sucesor duplicado.

        return nodo  # Devuelve el nodo actualizado.

    def _minimo(self, nodo):  # Método para encontrar el nodo menor de un subárbol.
        actual = nodo  # Empieza desde el nodo recibido.
        while actual.izquierda is not None:  # Mientras exista hijo izquierdo.
            actual = actual.izquierda  # Sigue avanzando a la izquierda.
        return actual  # Devuelve el menor encontrado.

    def inorden(self):  # Método que devuelve una lista con recorrido inorden.
        elementos = []  # Lista donde se guardarán los valores.
        self._inorden_rec(self.raiz, elementos)  # Llama al método recursivo.
        return elementos  # Devuelve la lista final.

    def _inorden_rec(self, nodo, elementos):  # Método recursivo para recorrido inorden.
        if nodo is not None:  # Si el nodo existe.
            self._inorden_rec(nodo.izquierda, elementos)  # Recorre izquierda.
            elementos.append(nodo.valor)  # Guarda el valor actual.
            self._inorden_rec(nodo.derecha, elementos)  # Recorre derecha.

    def vaciar(self):  # Método para vaciar completamente el árbol.
        self.raiz = None  # Borra la raíz.
        self.tamano = 0  # Reinicia el tamaño.

    def obtener_elementos_en_orden(self):  # Método extra para mantener mismo estilo que AVL.
        return self.inorden()  # Devuelve el recorrido inorden.

    def cargar_desde_csv(self, ruta_archivo, columna=0, tiene_encabezado=True):  # Carga una columna del CSV.
        try:  # Se usa try para controlar errores.
            with open(ruta_archivo, mode="r", newline="", encoding="utf-8") as archivo:  # Abre el archivo.
                lector = csv.reader(archivo)  # Crea el lector del CSV.

                if tiene_encabezado:  # Si el archivo tiene encabezado.
                    next(lector, None)  # Salta la primera fila.

                for fila in lector:  # Recorre las filas.
                    if len(fila) > columna:  # Verifica que exista la columna indicada.
                        dato = fila[columna].strip()  # Obtiene el dato y limpia espacios.
                        if dato != "":  # Solo trabaja si no está vacío.
                            self.insertar(dato)  # Inserta el dato en el árbol.

            print("\nDatos cargados correctamente al árbol.")
            print("Cantidad de elementos almacenados en el árbol:", self.tamano)

        except FileNotFoundError:  # Si el archivo no existe.
            print("\nError: el archivo no fue encontrado.")
        except Exception as e:  # Para cualquier otro error.
            print(f"\nOcurrió un error al leer el archivo: {e}")

    def graficar(self, nombre_archivo="arbol_binario"):  # Método para generar la imagen del árbol.
        if self.raiz is None:  # Si el árbol está vacío.
            print("El árbol está vacío. No hay nada que graficar.")
            return

        dot = Digraph(comment="Árbol Binario de Búsqueda")  # Crea el objeto Graphviz.
        dot.attr("node", shape="circle")  # Define forma circular para los nodos.

        self._graficar_rec(dot, self.raiz)  # Llama al método recursivo para dibujar nodos.

        dot.render(nombre_archivo, format="png", cleanup=True)  # Genera la imagen en PNG.
        print(f"Árbol generado correctamente en: {nombre_archivo}.png")

    def _graficar_rec(self, dot, nodo):  # Método recursivo para dibujar el árbol.
        if nodo is not None:  # Si el nodo existe.
            dot.node(str(nodo.valor), str(nodo.valor))  # Dibuja el nodo actual.

            if nodo.izquierda is not None:  # Si existe hijo izquierdo.
                dot.edge(str(nodo.valor), str(nodo.izquierda.valor))  # Dibuja la conexión izquierda.
                self._graficar_rec(dot, nodo.izquierda)  # Continúa por el subárbol izquierdo.

            if nodo.derecha is not None:  # Si existe hijo derecho.
                dot.edge(str(nodo.valor), str(nodo.derecha.valor))  # Dibuja la conexión derecha.
                self._graficar_rec(dot, nodo.derecha)  # Continúa por el subárbol derecho.


def leer_columna_csv(ruta_archivo, columna=0, tiene_encabezado=True):  # Función para leer una columna del CSV.
    datos = []  # Lista donde se guardarán los datos leídos.

    try:  # Manejo de errores.
        with open(ruta_archivo, mode="r", newline="", encoding="utf-8") as archivo:  # Abre el archivo.
            lector = csv.reader(archivo)  # Crea el lector del CSV.

            if tiene_encabezado:  # Si hay encabezado.
                next(lector, None)  # Salta la primera fila.

            for fila in lector:  # Recorre las filas.
                if len(fila) > columna:  # Verifica que exista la columna.
                    dato = fila[columna].strip()  # Obtiene el valor y limpia espacios.
                    if dato != "":  # Si el dato no está vacío.
                        datos.append(dato)  # Lo agrega a la lista.

    except FileNotFoundError:  # Si el archivo no existe.
        print("\nError: el archivo no fue encontrado.")
    except Exception as e:  # Otros errores.
        print(f"\nOcurrió un error al leer el archivo: {e}")

    return datos  # Devuelve los datos extraídos.


def medir_insercion(datos):  # Función que mide el tiempo de inserción en un ABB nuevo.
    arbol = ArbolBinarioBusqueda()  # Crea un árbol vacío.

    inicio = time.perf_counter()  # Marca el tiempo inicial.
    for dato in datos:  # Recorre todos los datos.
        arbol.insertar(dato)  # Inserta cada dato en el árbol.
    fin = time.perf_counter()  # Marca el tiempo final.

    return fin - inicio, arbol  # Devuelve el tiempo total y el árbol cargado.


def medir_busqueda(arbol, datos_buscar):  # Función que mide el tiempo total de búsqueda.
    inicio = time.perf_counter()  # Tiempo inicial.
    for dato in datos_buscar:  # Recorre los datos a buscar.
        arbol.buscar(dato)  # Busca cada dato.
    fin = time.perf_counter()  # Tiempo final.

    return fin - inicio  # Devuelve el tiempo total.


def medir_eliminacion(arbol, datos_eliminar):  # Función que mide el tiempo total de eliminación.
    inicio = time.perf_counter()  # Tiempo inicial.
    for dato in datos_eliminar:  # Recorre los datos a eliminar.
        arbol.eliminar(dato)  # Elimina cada dato del árbol.
    fin = time.perf_counter()  # Tiempo final.

    return fin - inicio  # Devuelve el tiempo total.


def ejecutar_experimento_csv(ruta_archivo, columna=0, tiene_encabezado=True, cantidad_pruebas=100):  # Ejecuta prueba automática.
    datos = leer_columna_csv(ruta_archivo, columna, tiene_encabezado)  # Lee los datos del CSV.

    if len(datos) == 0:  # Si no hay datos.
        print("\nNo hay datos para realizar el experimento.")
        return

    tiempo_insercion, arbol = medir_insercion(datos)  # Mide inserción y obtiene el árbol cargado.

    muestra_busqueda = datos[:cantidad_pruebas]  # Toma una muestra para búsqueda.
    muestra_eliminacion = datos[:cantidad_pruebas]  # Toma una muestra para eliminación.

    tiempo_busqueda = medir_busqueda(arbol, muestra_busqueda)  # Mide búsqueda.
    tiempo_eliminacion = medir_eliminacion(arbol, muestra_eliminacion)  # Mide eliminación.

    print("\n========= RESULTADOS DEL EXPERIMENTO ABB =========")
    print("Archivo analizado:", ruta_archivo)
    print("Cantidad de datos cargados:", len(datos))
    print("Tiempo total de inserción:", tiempo_insercion, "segundos")
    print("Tiempo total de búsqueda:", tiempo_busqueda, "segundos")
    print("Tiempo total de eliminación:", tiempo_eliminacion, "segundos")


def leer_entero(mensaje):  # Función para leer un número entero válido.
    while True:  # Repite hasta que el usuario escriba bien.
        try:  # Intenta convertir a entero.
            return int(input(mensaje))  # Devuelve el valor leído.
        except ValueError:  # Si no logra convertir.
            print("Debe ingresar un número entero.")  # Muestra mensaje de error.


def leer_booleano_encabezado():  # Pregunta si el archivo CSV tiene encabezado.
    respuesta = input("¿El archivo tiene encabezado? (s/n): ").strip().lower()  # Lee la respuesta.
    return respuesta == "s"  # Devuelve True si el usuario escribió s.


def menu():  # Función principal del menú.
    arbol = ArbolBinarioBusqueda()  # Crea un árbol vacío.

    while True:  # Mantiene el programa activo hasta salir.
        print("\n====== MENÚ ÁRBOL BINARIO DE BÚSQUEDA ======")
        print("1. Insertar dato")
        print("2. Buscar dato")
        print("3. Eliminar dato")
        print("4. Cargar desde archivo CSV")
        print("5. Mostrar recorrido inorden")
        print("6. Generar imagen Graphviz")
        print("7. Ejecutar experimento con CSV")
        print("8. Vaciar árbol")
        print("9. Salir")

        opcion = input("Seleccione una opción: ")  # Lee la opción elegida.

        if opcion == "1":  # Insertar dato.
            valor = input("Ingrese el dato a insertar: ").strip()  # Lee el dato como texto.
            if valor != "":  # Verifica que no esté vacío.
                arbol.insertar(valor)  # Inserta el dato.
                print(f"Se insertó {valor} correctamente.")
                arbol.graficar()
            else:
                print("No se puede insertar un dato vacío.")

        elif opcion == "2":  # Buscar dato.
            valor = input("Ingrese el dato a buscar: ").strip()  # Lee el dato.
            if arbol.buscar(valor):  # Busca el dato.
                print(f"El dato {valor} sí existe en el árbol.")
            else:
                print(f"El dato {valor} no existe en el árbol.")

        elif opcion == "3":  # Eliminar dato.
            valor = input("Ingrese el dato a eliminar: ").strip()  # Lee el dato.
            if arbol.buscar(valor):  # Verifica si existe.
                arbol.eliminar(valor)  # Elimina el dato.
                print(f"El dato {valor} fue eliminado.")
                arbol.graficar()
            else:
                print(f"El dato {valor} no existe en el árbol.")

        elif opcion == "4":  # Cargar CSV.
            ruta = input("Ingrese la ruta del archivo CSV: ").strip()  # Pide la ruta.
            columna = leer_entero("Ingrese el índice de la columna a usar (ejemplo 0, 1, 2): ")  # Pide la columna.
            encabezado = leer_booleano_encabezado()  # Pregunta si tiene encabezado.

            nuevo_arbol = ArbolBinarioBusqueda()  # Crea un árbol nuevo.
            nuevo_arbol.cargar_desde_csv(ruta, columna, encabezado)  # Carga los datos.
            arbol = nuevo_arbol  # Reemplaza el árbol actual por el cargado.
            arbol.graficar()

        elif opcion == "5":  # Mostrar recorrido inorden.
            print("Recorrido inorden:", arbol.inorden())

        elif opcion == "6":  # Generar imagen.
            nombre = input("Ingrese el nombre para la imagen (sin extensión): ").strip()
            if nombre == "":
                nombre = "arbol_binario"
            arbol.graficar(nombre)

        elif opcion == "7":  # Ejecutar experimento automático.
            ruta = input("Ingrese la ruta del archivo CSV: ").strip()  # Pide la ruta.
            columna = leer_entero("Ingrese el índice de la columna a usar (ejemplo 0, 1, 2): ")  # Pide la columna.
            encabezado = leer_booleano_encabezado()  # Pregunta si hay encabezado.
            cantidad_pruebas = leer_entero("Ingrese cuántos datos usar para búsqueda y eliminación: ")  # Pide la muestra.
            ejecutar_experimento_csv(ruta, columna, encabezado, cantidad_pruebas)  # Ejecuta el experimento.

        elif opcion == "8":  # Vaciar árbol.
            arbol.vaciar()  # Borra todo el contenido.
            print("El árbol fue vaciado correctamente.")

        elif opcion == "9":  # Salir.
            print("Saliendo del programa...")
            break

        else:  # Opción inválida.
            print("Opción inválida. Intente de nuevo.")


if __name__ == "__main__":  # Verifica si se está ejecutando directamente.
    menu()  # Llama al menú principal.
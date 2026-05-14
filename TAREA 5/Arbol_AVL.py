import csv  # Se importa csv para poder leer archivos CSV.
import time  # Se importa time para medir tiempos de ejecución.
from graphviz import Digraph  # Se importa Digraph para generar la visualización del árbol.


class Nodo:  # Clase que representa cada nodo del árbol.
    def __init__(self, valor):  # Constructor que recibe el valor a guardar en el nodo.
        self.valor = valor  # Guarda el valor del nodo.
        self.izquierdo = None  # Apuntador al hijo izquierdo, inicia vacío.
        self.derecho = None  # Apuntador al hijo derecho, inicia vacío.
        self.altura = 1  # Altura del nodo, inicia en 1 porque al crearse está solo.


class ABB:  # Clase base para el Árbol Binario de Búsqueda.
    def __init__(self):  # Constructor de la clase ABB.
        self.raiz = None  # La raíz inicia vacía porque el árbol aún no tiene nodos.

    def buscar(self, valor):  # Método público para buscar un valor en el árbol.
        return self._buscar_recursivo(self.raiz, valor)  # Llama al método recursivo desde la raíz.

    def _buscar_recursivo(self, nodo, valor):  # Método recursivo que busca un valor.
        if nodo is None:  # Si el nodo es None significa que no se encontró.
            return False  # Devuelve False porque el valor no existe en el árbol.

        if valor == nodo.valor:  # Si el valor buscado es igual al del nodo actual.
            return True  # Devuelve True porque sí se encontró.

        if valor < nodo.valor:  # Si el valor es menor que el nodo actual.
            return self._buscar_recursivo(nodo.izquierdo, valor)  # Busca por el subárbol izquierdo.
        else:  # En caso contrario, si el valor es mayor.
            return self._buscar_recursivo(nodo.derecho, valor)  # Busca por el subárbol derecho.


class AVL(ABB):  # Clase AVL que hereda de ABB.
    def __init__(self):  # Constructor de la clase AVL.
        super().__init__()  # Llama al constructor de la clase padre ABB.
        self.tamano = 0  # Guarda la cantidad de elementos únicos almacenados en el árbol.

    def obtener_altura(self, nodo):  # Método para obtener la altura de un nodo.
        if nodo is None:  # Si el nodo no existe.
            return 0  # Su altura se considera 0.
        return nodo.altura  # Devuelve la altura almacenada en el nodo.

    def actualizar_altura(self, nodo):  # Método para recalcular la altura de un nodo.
        if nodo is not None:  # Solo trabaja si el nodo existe.
            altura_izquierda = self.obtener_altura(nodo.izquierdo)  # Obtiene la altura del hijo izquierdo.
            altura_derecha = self.obtener_altura(nodo.derecho)  # Obtiene la altura del hijo derecho.
            nodo.altura = 1 + max(altura_izquierda, altura_derecha)  # Guarda la nueva altura del nodo.

    def obtener_balance(self, nodo):  # Método para calcular el factor de balance.
        if nodo is None:  # Si el nodo no existe.
            return 0  # Su balance se considera 0.
        return self.obtener_altura(nodo.izquierdo) - self.obtener_altura(nodo.derecho)  # Devuelve diferencia de alturas.

    def rotacion_derecha(self, y):  # Método que realiza una rotación simple a la derecha.
        x = y.izquierdo  # x será el hijo izquierdo del nodo desbalanceado.
        t2 = x.derecho  # t2 guarda el subárbol derecho de x.

        x.derecho = y  # El nodo y pasa a ser hijo derecho de x.
        y.izquierdo = t2  # El subárbol t2 pasa a ser hijo izquierdo de y.

        self.actualizar_altura(y)  # Se actualiza la altura del nodo y.
        self.actualizar_altura(x)  # Se actualiza la altura del nodo x.

        return x  # Se devuelve x porque ahora es la nueva raíz de ese subárbol.

    def rotacion_izquierda(self, x):  # Método que realiza una rotación simple a la izquierda.
        y = x.derecho  # y será el hijo derecho del nodo desbalanceado.
        t2 = y.izquierdo  # t2 guarda el subárbol izquierdo de y.

        y.izquierdo = x  # El nodo x pasa a ser hijo izquierdo de y.
        x.derecho = t2  # El subárbol t2 pasa a ser hijo derecho de x.

        self.actualizar_altura(x)  # Se actualiza la altura del nodo x.
        self.actualizar_altura(y)  # Se actualiza la altura del nodo y.

        return y  # Se devuelve y porque ahora es la nueva raíz de ese subárbol.

    def insertar(self, valor):  # Método público para insertar un valor en el árbol AVL.
        if not self.buscar(valor):  # Solo inserta si el valor no existe ya en el árbol.
            self.raiz = self._insertar_recursivo(self.raiz, valor)  # Inserta desde la raíz y guarda el nuevo estado.
            self.tamano += 1  # Aumenta el contador de elementos únicos.

    def _insertar_recursivo(self, nodo, valor):  # Método recursivo para insertar y balancear.
        if nodo is None:  # Si se llegó a una posición vacía.
            return Nodo(valor)  # Crea un nuevo nodo y lo devuelve.

        if valor < nodo.valor:  # Si el valor es menor que el nodo actual.
            nodo.izquierdo = self._insertar_recursivo(nodo.izquierdo, valor)  # Inserta en el subárbol izquierdo.
        elif valor > nodo.valor:  # Si el valor es mayor que el nodo actual.
            nodo.derecho = self._insertar_recursivo(nodo.derecho, valor)  # Inserta en el subárbol derecho.
        else:  # Si el valor ya existe.
            return nodo  # No se inserta repetido y se devuelve el mismo nodo.

        self.actualizar_altura(nodo)  # Se actualiza la altura del nodo actual.
        balance = self.obtener_balance(nodo)  # Se calcula el balance del nodo actual.

        if balance > 1 and valor < nodo.izquierdo.valor:  # Caso Izquierda-Izquierda.
            return self.rotacion_derecha(nodo)  # Se corrige con rotación derecha.

        if balance < -1 and valor > nodo.derecho.valor:  # Caso Derecha-Derecha.
            return self.rotacion_izquierda(nodo)  # Se corrige con rotación izquierda.

        if balance > 1 and valor > nodo.izquierdo.valor:  # Caso Izquierda-Derecha.
            nodo.izquierdo = self.rotacion_izquierda(nodo.izquierdo)  # Primero rota a la izquierda el hijo.
            return self.rotacion_derecha(nodo)  # Después rota a la derecha el nodo actual.

        if balance < -1 and valor < nodo.derecho.valor:  # Caso Derecha-Izquierda.
            nodo.derecho = self.rotacion_derecha(nodo.derecho)  # Primero rota a la derecha el hijo.
            return self.rotacion_izquierda(nodo)  # Después rota a la izquierda el nodo actual.

        return nodo  # Si no hubo desbalance, devuelve el nodo sin cambios extra.

    def eliminar(self, valor):  # Método público para eliminar un valor del árbol AVL.
        if self.buscar(valor):  # Solo elimina si el valor existe en el árbol.
            self.raiz = self._eliminar_recursivo(self.raiz, valor)  # Elimina desde la raíz y actualiza el árbol.
            self.tamano -= 1  # Disminuye el contador de elementos.

    def _eliminar_recursivo(self, nodo, valor):  # Método recursivo para eliminar y balancear.
        if nodo is None:  # Si el nodo no existe.
            return nodo  # Devuelve None porque no hay nada que eliminar.

        if valor < nodo.valor:  # Si el valor buscado es menor.
            nodo.izquierdo = self._eliminar_recursivo(nodo.izquierdo, valor)  # Busca y elimina en la izquierda.
        elif valor > nodo.valor:  # Si el valor buscado es mayor.
            nodo.derecho = self._eliminar_recursivo(nodo.derecho, valor)  # Busca y elimina en la derecha.
        else:  # Si se encontró el nodo a eliminar.
            if nodo.izquierdo is None:  # Si no tiene hijo izquierdo.
                return nodo.derecho  # Se reemplaza por el hijo derecho.
            elif nodo.derecho is None:  # Si no tiene hijo derecho.
                return nodo.izquierdo  # Se reemplaza por el hijo izquierdo.

            temporal = self.obtener_minimo(nodo.derecho)  # Busca el sucesor inorden en el subárbol derecho.
            nodo.valor = temporal.valor  # Copia el valor del sucesor al nodo actual.
            nodo.derecho = self._eliminar_recursivo(nodo.derecho, temporal.valor)  # Elimina el sucesor duplicado.

        self.actualizar_altura(nodo)  # Actualiza la altura del nodo después de eliminar.
        balance = self.obtener_balance(nodo)  # Calcula el balance del nodo.

        if balance > 1 and self.obtener_balance(nodo.izquierdo) >= 0:  # Caso Izquierda-Izquierda.
            return self.rotacion_derecha(nodo)  # Corrige con rotación derecha.

        if balance > 1 and self.obtener_balance(nodo.izquierdo) < 0:  # Caso Izquierda-Derecha.
            nodo.izquierdo = self.rotacion_izquierda(nodo.izquierdo)  # Primero rota el hijo izquierdo.
            return self.rotacion_derecha(nodo)  # Después rota el nodo actual.

        if balance < -1 and self.obtener_balance(nodo.derecho) <= 0:  # Caso Derecha-Derecha.
            return self.rotacion_izquierda(nodo)  # Corrige con rotación izquierda.

        if balance < -1 and self.obtener_balance(nodo.derecho) > 0:  # Caso Derecha-Izquierda.
            nodo.derecho = self.rotacion_derecha(nodo.derecho)  # Primero rota el hijo derecho.
            return self.rotacion_izquierda(nodo)  # Después rota el nodo actual.

        return nodo  # Devuelve el nodo ya equilibrado.

    def obtener_minimo(self, nodo):  # Método para encontrar el nodo con menor valor en un subárbol.
        actual = nodo  # Se inicia desde el nodo recibido.
        while actual.izquierdo is not None:  # Mientras exista hijo izquierdo.
            actual = actual.izquierdo  # Avanza a la izquierda porque ahí están los menores.
        return actual  # Devuelve el nodo mínimo encontrado.

    def vaciar(self):  # Método para dejar el árbol completamente vacío.
        self.raiz = None  # Borra la referencia a la raíz.
        self.tamano = 0  # Reinicia el contador de elementos.

    def obtener_elementos_en_orden(self):  # Método que devuelve una lista con los valores en recorrido inorden.
        elementos = []  # Lista donde se guardarán los valores.
        self._inorden(self.raiz, elementos)  # Llama al método recursivo.
        return elementos  # Devuelve la lista final.

    def _inorden(self, nodo, elementos):  # Método recursivo para recorrido inorden.
        if nodo is not None:  # Solo trabaja si el nodo existe.
            self._inorden(nodo.izquierdo, elementos)  # Recorre primero el subárbol izquierdo.
            elementos.append(nodo.valor)  # Guarda el valor del nodo actual.
            self._inorden(nodo.derecho, elementos)  # Recorre finalmente el subárbol derecho.

    def cargar_desde_csv(self, ruta_archivo, columna=0, tiene_encabezado=True):  # Carga una sola columna del CSV.
        try:  # Se usa try para controlar errores al abrir o leer el archivo.
            with open(ruta_archivo, mode="r", newline="", encoding="utf-8") as archivo:  # Abre el archivo en modo lectura.
                lector = csv.reader(archivo)  # Crea un lector de filas del CSV.

                if tiene_encabezado:  # Si el archivo trae encabezados.
                    next(lector, None)  # Salta la primera fila.

                for fila in lector:  # Recorre cada fila del archivo.
                    if len(fila) > columna:  # Verifica que la columna solicitada exista.
                        dato = fila[columna].strip()  # Toma el dato de la columna indicada y limpia espacios.
                        if dato != "":  # Solo trabaja si el dato no está vacío.
                            self.insertar(dato)  # Inserta el dato tal como está, normalmente como texto.

            print("\nDatos cargados correctamente desde el archivo CSV.")  # Mensaje de éxito.
            print("Cantidad de elementos almacenados en el árbol:", self.tamano)  # Muestra cuántos elementos quedaron.

        except FileNotFoundError:  # Error si el archivo no existe.
            print("\nError: el archivo no fue encontrado.")  # Muestra mensaje claro al usuario.
        except Exception as e:  # Captura cualquier otro error inesperado.
            print(f"\nOcurrió un error al cargar el archivo: {e}")  # Muestra el detalle del error.

    def graficar(self, nombre_archivo="arbol_avl"):  # Método para generar la imagen del árbol con Graphviz.
        if self.raiz is None:  # Si el árbol está vacío.
            print("\nEl árbol está vacío. No hay nada para graficar.")  # Muestra mensaje al usuario.
            return  # Sale del método porque no se puede graficar un árbol vacío.

        dot = Digraph(comment="Árbol AVL")  # Crea el objeto principal de Graphviz.
        dot.attr("node", shape="circle")  # Define que los nodos se dibujen en forma de círculo.

        self._agregar_nodos_graphviz(dot, self.raiz)  # Llama al método recursivo para agregar nodos y conexiones.

        dot.render(nombre_archivo, format="png", cleanup=True)  # Genera el archivo PNG y limpia el archivo temporal.
        print(f"\nÁrbol graficado correctamente. Se generó el archivo: {nombre_archivo}.png")  # Mensaje de éxito.

    def _agregar_nodos_graphviz(self, dot, nodo):  # Método recursivo para agregar nodos al gráfico.
        if nodo is None:  # Si el nodo no existe.
            return  # Termina la llamada recursiva.

        etiqueta = f"{nodo.valor}\nH:{nodo.altura}"  # Crea la etiqueta con valor y altura del nodo.
        dot.node(str(nodo.valor), etiqueta)  # Agrega el nodo al gráfico usando su valor como identificador.

        if nodo.izquierdo is not None:  # Si existe hijo izquierdo.
            dot.edge(str(nodo.valor), str(nodo.izquierdo.valor))  # Dibuja la conexión hacia el hijo izquierdo.
            self._agregar_nodos_graphviz(dot, nodo.izquierdo)  # Continúa recursivamente con el hijo izquierdo.

        if nodo.derecho is not None:  # Si existe hijo derecho.
            dot.edge(str(nodo.valor), str(nodo.derecho.valor))  # Dibuja la conexión hacia el hijo derecho.
            self._agregar_nodos_graphviz(dot, nodo.derecho)  # Continúa recursivamente con el hijo derecho.


def leer_columna_csv(ruta_archivo, columna=0, tiene_encabezado=True):  # Función para leer una columna específica del CSV.
    datos = []  # Lista donde se guardarán los datos extraídos.

    try:  # Manejo de errores de lectura.
        with open(ruta_archivo, mode="r", newline="", encoding="utf-8") as archivo:  # Abre el archivo.
            lector = csv.reader(archivo)  # Crea el lector del CSV.

            if tiene_encabezado:  # Si el archivo tiene encabezado.
                next(lector, None)  # Salta la primera fila.

            for fila in lector:  # Recorre cada fila.
                if len(fila) > columna:  # Verifica que exista la columna.
                    dato = fila[columna].strip()  # Extrae y limpia el dato.
                    if dato != "":  # Solo guarda datos no vacíos.
                        datos.append(dato)  # Agrega el dato a la lista.

    except FileNotFoundError:  # Error si el archivo no existe.
        print("\nError: el archivo no fue encontrado.")
    except Exception as e:  # Otros errores.
        print(f"\nOcurrió un error al leer el archivo: {e}")

    return datos  # Devuelve la lista de datos leídos.


def medir_insercion(datos):  # Función que mide el tiempo total de inserción de una lista de datos en un AVL nuevo.
    arbol = AVL()  # Crea un árbol AVL vacío.

    inicio = time.perf_counter()  # Guarda el tiempo justo antes de insertar.
    for dato in datos:  # Recorre todos los datos.
        arbol.insertar(dato)  # Inserta cada dato en el árbol.
    fin = time.perf_counter()  # Guarda el tiempo al terminar.

    return fin - inicio, arbol  # Devuelve el tiempo total y el árbol cargado.


def medir_busqueda(arbol, datos_buscar):  # Función que mide el tiempo total de búsqueda.
    inicio = time.perf_counter()  # Tiempo inicial.
    for dato in datos_buscar:  # Recorre cada dato a buscar.
        arbol.buscar(dato)  # Realiza la búsqueda.
    fin = time.perf_counter()  # Tiempo final.

    return fin - inicio  # Devuelve el tiempo total de búsqueda.


def medir_eliminacion(arbol, datos_eliminar):  # Función que mide el tiempo total de eliminación.
    inicio = time.perf_counter()  # Tiempo inicial.
    for dato in datos_eliminar:  # Recorre los datos a eliminar.
        arbol.eliminar(dato)  # Elimina cada dato del árbol.
    fin = time.perf_counter()  # Tiempo final.

    return fin - inicio  # Devuelve el tiempo total de eliminación.


def ejecutar_experimento_csv(ruta_archivo, columna=0, tiene_encabezado=True, cantidad_pruebas=100):  # Función automática para probar inserción, búsqueda y eliminación.
    datos = leer_columna_csv(ruta_archivo, columna, tiene_encabezado)  # Lee los datos desde el CSV.

    if len(datos) == 0:  # Si no se cargaron datos.
        print("\nNo hay datos para realizar el experimento.")  # Informa al usuario.
        return  # Sale de la función.

    tiempo_insercion, arbol = medir_insercion(datos)  # Mide la inserción y devuelve el árbol ya cargado.

    muestra_busqueda = datos[:cantidad_pruebas]  # Toma una muestra inicial para búsqueda.
    muestra_eliminacion = datos[:cantidad_pruebas]  # Toma una muestra inicial para eliminación.

    tiempo_busqueda = medir_busqueda(arbol, muestra_busqueda)  # Mide búsqueda.
    tiempo_eliminacion = medir_eliminacion(arbol, muestra_eliminacion)  # Mide eliminación.

    print("\n========= RESULTADOS DEL EXPERIMENTO AVL =========")
    print("Archivo analizado:", ruta_archivo)
    print("Cantidad de datos cargados:", len(datos))
    print("Tiempo total de inserción:", tiempo_insercion, "segundos")
    print("Tiempo total de búsqueda:", tiempo_busqueda, "segundos")
    print("Tiempo total de eliminación:", tiempo_eliminacion, "segundos")


def mostrar_menu():  # Función que imprime el menú principal del programa.
    print("\n========= MENÚ ÁRBOL AVL =========")
    print("1. Insertar un dato")
    print("2. Buscar un dato")
    print("3. Eliminar un dato")
    print("4. Cargar árbol desde archivo CSV")
    print("5. Visualizar árbol con Graphviz")
    print("6. Mostrar recorrido inorden")
    print("7. Ejecutar experimento con CSV")
    print("8. Vaciar árbol")
    print("9. Salir")


def leer_entero(mensaje):  # Función que obliga al usuario a ingresar un número entero válido.
    while True:  # Ciclo infinito hasta que el usuario escriba un entero correcto.
        try:  # Intenta convertir la entrada a entero.
            return int(input(mensaje))  # Lee el dato, lo convierte y lo devuelve.
        except ValueError:  # Si el dato no es entero.
            print("Error: debe ingresar un número entero.")  # Informa el error y vuelve a pedir el dato.


def leer_booleano_encabezado():  # Función para preguntar si el archivo CSV tiene encabezado.
    respuesta = input("¿El archivo tiene encabezado? (s/n): ").strip().lower()  # Lee la respuesta del usuario.
    return respuesta == "s"  # Devuelve True si escribió s.


def main():  # Función principal del programa.
    arbol = AVL()  # Crea un objeto de tipo AVL.

    while True:  # Ciclo principal para mantener activo el menú hasta que el usuario salga.
        mostrar_menu()  # Muestra el menú en pantalla.
        opcion = input("Seleccione una opción: ")  # Lee la opción elegida por el usuario.

        if opcion == "1":  # Si el usuario eligió insertar.
            dato = input("Ingrese el dato a insertar: ").strip()  # Pide el dato a insertar.
            if dato != "":  # Verifica que no venga vacío.
                arbol.insertar(dato)  # Inserta el dato en el árbol.
                print("Dato insertado correctamente.")  # Confirma la acción.
            else:  # Si viene vacío.
                print("No se puede insertar un dato vacío.")  # Informa error.

        elif opcion == "2":  # Si el usuario eligió buscar.
            dato = input("Ingrese el dato a buscar: ").strip()  # Pide el dato a buscar.
            if arbol.buscar(dato):  # Verifica si el dato existe.
                print("El dato sí existe en el árbol.")  # Mensaje si se encontró.
            else:  # Si no se encontró.
                print("El dato no existe en el árbol.")  # Mensaje si no está.

        elif opcion == "3":  # Si el usuario eligió eliminar.
            dato = input("Ingrese el dato a eliminar: ").strip()  # Pide el dato a eliminar.
            if arbol.buscar(dato):  # Primero verifica que el dato exista.
                arbol.eliminar(dato)  # Elimina el dato del árbol.
                print("Dato eliminado correctamente.")  # Confirma la acción.
            else:  # Si no existe el dato.
                print("No se puede eliminar porque el dato no existe en el árbol.")  # Informa al usuario.

        elif opcion == "4":  # Si el usuario eligió cargar desde CSV.
            ruta = input("Ingrese la ruta del archivo CSV: ")  # Pide la ruta del archivo.
            columna = leer_entero("Ingrese el índice de la columna a usar (ejemplo 0, 1, 2): ")  # Pide la columna.
            encabezado = leer_booleano_encabezado()  # Pregunta si el archivo tiene encabezado.
            arbol.cargar_desde_csv(ruta, columna, encabezado)  # Carga los datos desde la columna indicada.

        elif opcion == "5":  # Si el usuario eligió visualizar con Graphviz.
            nombre = input("Ingrese el nombre para la imagen (sin extensión): ")  # Pide nombre base del archivo.
            if nombre.strip() == "":  # Si el usuario no escribió nada.
                nombre = "arbol_avl"  # Usa un nombre por defecto.
            arbol.graficar(nombre)  # Genera la imagen del árbol.

        elif opcion == "6":  # Si el usuario eligió mostrar el recorrido inorden.
            elementos = arbol.obtener_elementos_en_orden()  # Obtiene los elementos ordenados.
            print("\nRecorrido inorden del árbol:")
            print(elementos)  # Muestra la lista en pantalla.

        elif opcion == "7":  # Si el usuario eligió ejecutar experimento.
            ruta = input("Ingrese la ruta del archivo CSV: ")  # Pide la ruta del archivo.
            columna = leer_entero("Ingrese el índice de la columna a usar (ejemplo 0, 1, 2): ")  # Pide la columna.
            encabezado = leer_booleano_encabezado()  # Pregunta si el archivo tiene encabezado.
            cantidad_pruebas = leer_entero("Ingrese cuántos datos usar para búsqueda y eliminación: ")  # Pide tamaño de muestra.
            ejecutar_experimento_csv(ruta, columna, encabezado, cantidad_pruebas)  # Ejecuta el experimento.

        elif opcion == "8":  # Si el usuario eligió vaciar el árbol.
            arbol.vaciar()  # Limpia completamente el árbol.
            print("El árbol fue vaciado correctamente.")  # Confirma la acción.

        elif opcion == "9":  # Si el usuario eligió salir.
            print("Programa finalizado.")  # Mensaje de despedida.
            break  # Termina el ciclo principal.

        else:  # Si el usuario escribió una opción no válida.
            print("Opción inválida. Intente nuevamente.")  # Mensaje de error.


if __name__ == "__main__":  # Verifica si este archivo se está ejecutando directamente.
    main()  # Llama a la función principal para iniciar el programa.
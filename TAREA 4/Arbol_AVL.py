import csv  # Se importa csv para poder leer archivos CSV.
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
        self.raiz = self._insertar_recursivo(self.raiz, valor)  # Inserta desde la raíz y guarda el nuevo estado.

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
        self.raiz = self._eliminar_recursivo(self.raiz, valor)  # Elimina desde la raíz y actualiza el árbol.

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

    def cargar_desde_csv(self, ruta_archivo):  # Método para cargar números desde un archivo CSV.
        try:  # Se usa try para controlar errores al abrir o leer el archivo.
            with open(ruta_archivo, mode="r", newline="", encoding="utf-8") as archivo:  # Abre el archivo en modo lectura.
                lector = csv.reader(archivo)  # Crea un lector de filas del CSV.

                for fila in lector:  # Recorre cada fila del archivo.
                    for dato in fila:  # Recorre cada dato dentro de la fila.
                        dato = dato.strip()  # Elimina espacios al inicio y al final del texto.
                        if dato != "":  # Solo trabaja si el dato no está vacío.
                            self.insertar(int(dato))  # Convierte el dato a entero y lo inserta en el árbol.

            print("\nDatos cargados correctamente desde el archivo CSV.")  # Mensaje de éxito.

        except FileNotFoundError:  # Error si el archivo no existe.
            print("\nError: el archivo no fue encontrado.")  # Muestra mensaje claro al usuario.
        except ValueError:  # Error si algún dato no se puede convertir a entero.
            print("\nError: el archivo contiene valores no válidos. Solo use números enteros.")  # Mensaje de error.
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


def mostrar_menu():  # Función que imprime el menú principal del programa.
    print("\n========= MENÚ ÁRBOL AVL =========")  
    print("1. Insertar un número")  
    print("2. Buscar un número")  
    print("3. Eliminar un número")  
    print("4. Cargar árbol desde archivo CSV")  
    print("5. Visualizar árbol con Graphviz")  
    print("6. Salir")  


def leer_entero(mensaje):  # Función que obliga al usuario a ingresar un número entero válido.
    while True:  # Ciclo infinito hasta que el usuario escriba un entero correcto.
        try:  # Intenta convertir la entrada a entero.
            return int(input(mensaje))  # Lee el dato, lo convierte y lo devuelve.
        except ValueError:  # Si el dato no es entero.
            print("Error: debe ingresar un número entero.")  # Informa el error y vuelve a pedir el dato.


def main():  # Función principal del programa.
    arbol = AVL()  # Crea un objeto de tipo AVL.

    while True:  # Ciclo principal para mantener activo el menú hasta que el usuario salga.
        mostrar_menu()  # Muestra el menú en pantalla.
        opcion = input("Seleccione una opción: ")  # Lee la opción elegida por el usuario.

        if opcion == "1":  # Si el usuario eligió insertar.
            numero = leer_entero("Ingrese el número a insertar: ")  # Pide el número a insertar.
            arbol.insertar(numero)  # Inserta el número en el árbol.
            print("Número insertado correctamente.")  # Confirma la acción.

        elif opcion == "2":  # Si el usuario eligió buscar.
            numero = leer_entero("Ingrese el número a buscar: ")  # Pide el número a buscar.
            if arbol.buscar(numero):  # Verifica si el número existe.
                print("El número sí existe en el árbol.")  # Mensaje si se encontró.
            else:  # Si no se encontró.
                print("El número no existe en el árbol.")  # Mensaje si no está.

        elif opcion == "3":  # Si el usuario eligió eliminar.
            numero = leer_entero("Ingrese el número a eliminar: ")  # Pide el número a eliminar.
            if arbol.buscar(numero):  # Primero verifica que el número exista.
                arbol.eliminar(numero)  # Elimina el número del árbol.
                print("Número eliminado correctamente.")  # Confirma la acción.
            else:  # Si no existe el número.
                print("No se puede eliminar porque el número no existe en el árbol.")  # Informa al usuario.

        elif opcion == "4":  # Si el usuario eligió cargar desde CSV.
            ruta = input("Ingrese la ruta del archivo CSV: ")  # Pide la ruta del archivo.
            arbol.cargar_desde_csv(ruta)  # Llama al método para cargar datos desde el CSV.

        elif opcion == "5":  # Si el usuario eligió visualizar con Graphviz.
            nombre = input("Ingrese el nombre para la imagen (sin extensión): ")  # Pide nombre base del archivo.
            if nombre.strip() == "":  # Si el usuario no escribió nada.
                nombre = "arbol_avl"  # Usa un nombre por defecto.
            arbol.graficar(nombre)  # Genera la imagen del árbol.

        elif opcion == "6":  # Si el usuario eligió salir.
            print("Programa finalizado.")  # Mensaje de despedida.
            break  # Termina el ciclo principal.

        else:  # Si el usuario escribió una opción no válida.
            print("Opción inválida. Intente nuevamente.")  # Mensaje de error.


if __name__ == "__main__":  # Verifica si este archivo se está ejecutando directamente.
    main()  # Llama a la función principal para iniciar el programa.

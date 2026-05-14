import csv  # Se importa csv para leer archivos CSV.
import time  # Se importa time para medir tiempos de ejecución.
from graphviz import Digraph  # Se importa Digraph para graficar la lista.


class Nodo:  # Clase que representa cada nodo de la lista simple.
    def __init__(self, carnet, nombre="", apellido=""):  # Constructor del nodo.
        self.carnet = carnet  # Guarda el valor principal del nodo.
        self.nombre = nombre  # Guarda el nombre del nodo.
        self.apellido = apellido  # Guarda el apellido del nodo.
        self.siguiente = None  # Apunta al siguiente nodo.


class Lista_Simple:  # Clase principal de la lista simplemente enlazada.
    def __init__(self):  # Constructor de la lista.
        self.inicio = None  # El inicio comienza vacío.
        self.final = None  # El final comienza vacío.
        self.contador_img = 1  # Sirve para no sobrescribir imágenes.
        self.tamano = 0  # Guarda cuántos elementos hay en la lista.

    def esta_vacia(self):  # Método para saber si la lista está vacía.
        return self.inicio is None  # Devuelve True si no hay nodos.

    def insertar_al_principio(self, carnet, nombre="", apellido=""):  # Inserta al inicio.
        nuevo = Nodo(carnet, nombre, apellido)  # Crea el nuevo nodo.

        if self.inicio is None:  # Si la lista está vacía.
            self.inicio = nuevo  # El nuevo nodo será el inicio.
            self.final = nuevo  # También será el final.
        else:  # Si ya hay nodos.
            nuevo.siguiente = self.inicio  # El nuevo nodo apunta al inicio actual.
            self.inicio = nuevo  # El nuevo nodo pasa a ser el inicio.

        self.tamano += 1  # Aumenta el contador de elementos.

    def insertar_al_final(self, carnet, nombre="", apellido=""):  # Inserta al final.
        nuevo = Nodo(carnet, nombre, apellido)  # Crea el nuevo nodo.

        if self.final is None:  # Si la lista está vacía.
            self.inicio = nuevo  # El nuevo nodo será el inicio.
            self.final = nuevo  # También será el final.
        else:  # Si ya hay elementos.
            self.final.siguiente = nuevo  # El último nodo apunta al nuevo nodo.
            self.final = nuevo  # El nuevo nodo pasa a ser el final.

        self.tamano += 1  # Aumenta el contador de elementos.

    def buscar(self, dato):  # Método para buscar un dato en la lista.
        temp = self.inicio  # Empieza desde el inicio.

        while temp is not None:  # Recorre toda la lista.
            if temp.carnet == dato:  # Si encuentra el dato.
                return True  # Devuelve True.
            temp = temp.siguiente  # Avanza al siguiente nodo.

        return False  # Si termina el recorrido y no lo encuentra, devuelve False.

    def eliminar_por_valor(self, dato):  # Elimina el primer nodo que coincida con el valor dado.
        temp = self.inicio  # Empieza desde el inicio.
        anterior = None  # Guarda el nodo anterior al actual.

        while temp is not None:  # Recorre toda la lista.
            if temp.carnet == dato:  # Si encuentra el nodo a eliminar.

                if temp == self.inicio and temp == self.final:  # Caso 1: único nodo.
                    self.inicio = None  # La lista queda vacía.
                    self.final = None  # La lista queda vacía.

                elif temp == self.inicio:  # Caso 2: está al inicio.
                    self.inicio = temp.siguiente  # El inicio avanza al siguiente nodo.

                elif temp == self.final:  # Caso 3: está al final.
                    anterior.siguiente = None  # El nodo anterior pasa a ser el último.
                    self.final = anterior  # Se actualiza el final.

                else:  # Caso 4: está en medio.
                    anterior.siguiente = temp.siguiente  # Se salta el nodo a eliminar.

                self.tamano -= 1  # Disminuye el contador.
                return True  # Indica que sí eliminó el dato.

            anterior = temp  # Guarda el nodo actual como anterior.
            temp = temp.siguiente  # Avanza al siguiente nodo.

        return False  # Si no encontró el valor, devuelve False.

    def vaciar(self):  # Método para dejar la lista vacía.
        self.inicio = None  # Borra el inicio.
        self.final = None  # Borra el final.
        self.tamano = 0  # Reinicia el tamaño.

    def obtener_elementos(self):  # Devuelve una lista con todos los carnets almacenados.
        elementos = []  # Lista vacía donde se guardarán los datos.
        temp = self.inicio  # Empieza desde el inicio.

        while temp is not None:  # Recorre toda la lista.
            elementos.append(temp.carnet)  # Guarda el valor del nodo.
            temp = temp.siguiente  # Avanza al siguiente nodo.

        return elementos  # Devuelve la lista completa.

    def mostrar_lista(self):  # Método para mostrar la lista en pantalla.
        salida = "None -> "  # Texto inicial.
        temp = self.inicio  # Empieza desde el inicio.

        while temp is not None:  # Recorre todos los nodos.
            salida += f"{temp.carnet}--{temp.nombre}--{temp.apellido}"  # Agrega el contenido del nodo.
            if temp.siguiente is not None:  # Si hay más nodos después.
                salida += " -> "  # Agrega la flecha simple.
            temp = temp.siguiente  # Avanza al siguiente.

        salida += " -> None"  # Finaliza la representación.
        print(salida)  # Muestra la lista.

    def graficar(self, nombre_archivo="lista_simple"):  # Método para generar una imagen de la lista.
        dot = Digraph(format="png")  # Crea el objeto Graphviz.
        dot.attr(rankdir="LR")  # Dibuja de izquierda a derecha.

        dot.node("NONE_IZQ", "None", shape="box")  # Nodo None inicial.
        dot.node("NONE_DER", "None", shape="box")  # Nodo None final.

        if self.inicio is None:  # Si la lista está vacía.
            dot.edge("NONE_IZQ", "NONE_DER", label="vacía")  # Une ambos None.
            dot.render(nombre_archivo, cleanup=True)  # Genera la imagen.
            return  # Sale del método.

        temp = self.inicio  # Empieza desde el inicio.
        i = 1  # Contador para nombrar nodos en la imagen.
        ids = []  # Lista para guardar los identificadores de los nodos.

        while temp is not None:  # Recorre toda la lista.
            node_id = f"N{i}"  # Crea un id único para el nodo.
            ids.append(node_id)  # Guarda el id en la lista.

            etiqueta = f"{temp.carnet}\\n{temp.nombre} {temp.apellido}"  # Texto del nodo.
            dot.node(node_id, etiqueta, shape="record")  # Agrega el nodo a la imagen.

            temp = temp.siguiente  # Avanza al siguiente nodo.
            i += 1  # Aumenta el contador.

        dot.edge("NONE_IZQ", ids[0])  # Conecta None inicial con el primer nodo.

        for j in range(len(ids) - 1):  # Recorre los ids para unir nodos.
            dot.edge(ids[j], ids[j + 1], label="sig")  # Une cada nodo con el siguiente.

        dot.edge(ids[-1], "NONE_DER")  # El último nodo apunta a None final.

        dot.render(nombre_archivo, cleanup=True)  # Genera la imagen.

    def cargar_desde_csv(self, ruta_archivo, columna=0, tiene_encabezado=True):  # Carga datos desde una columna del CSV.
        try:  # Se usa try para controlar errores.
            with open(ruta_archivo, mode="r", newline="", encoding="utf-8") as archivo:  # Abre el archivo.
                lector = csv.reader(archivo)  # Crea el lector del CSV.

                if tiene_encabezado:  # Si el archivo tiene encabezado.
                    next(lector, None)  # Salta la primera fila.

                for fila in lector:  # Recorre todas las filas.
                    if len(fila) > columna:  # Verifica que exista la columna indicada.
                        dato = fila[columna].strip()  # Obtiene y limpia el dato.
                        if dato != "":  # Solo inserta si no está vacío.
                            self.insertar_al_final(dato)  # Inserta al final de la lista.

            print("\nDatos cargados correctamente desde el archivo CSV.")  # Mensaje de éxito.
            print("Cantidad de elementos almacenados en la lista:", self.tamano)  # Muestra cantidad.

        except FileNotFoundError:  # Si el archivo no existe.
            print("\nError: el archivo no fue encontrado.")
        except Exception as e:  # Para cualquier otro error.
            print(f"\nOcurrió un error al cargar el archivo: {e}")


def leer_columna_csv(ruta_archivo, columna=0, tiene_encabezado=True):  # Función para leer una columna del CSV.
    datos = []  # Lista donde se guardarán los datos.

    try:  # Manejo de errores.
        with open(ruta_archivo, mode="r", newline="", encoding="utf-8") as archivo:  # Abre el archivo.
            lector = csv.reader(archivo)  # Crea el lector.

            if tiene_encabezado:  # Si tiene encabezado.
                next(lector, None)  # Salta la primera fila.

            for fila in lector:  # Recorre cada fila.
                if len(fila) > columna:  # Verifica que exista la columna.
                    dato = fila[columna].strip()  # Toma el valor y limpia espacios.
                    if dato != "":  # Si el dato no está vacío.
                        datos.append(dato)  # Lo agrega a la lista.

    except FileNotFoundError:  # Error si no existe el archivo.
        print("\nError: el archivo no fue encontrado.")
    except Exception as e:  # Otros errores.
        print(f"\nOcurrió un error al leer el archivo: {e}")

    return datos  # Devuelve la lista de datos.


def medir_insercion(datos):  # Función que mide el tiempo de inserción en una lista nueva.
    lista = Lista_Simple()  # Crea una lista vacía.

    inicio = time.perf_counter()  # Marca el tiempo inicial.
    for dato in datos:  # Recorre todos los datos.
        lista.insertar_al_final(dato)  # Inserta cada dato al final.
    fin = time.perf_counter()  # Marca el tiempo final.

    return fin - inicio, lista  # Devuelve el tiempo y la lista ya cargada.


def medir_busqueda(lista, datos_buscar):  # Función que mide el tiempo total de búsqueda.
    inicio = time.perf_counter()  # Tiempo inicial.
    for dato in datos_buscar:  # Recorre los datos a buscar.
        lista.buscar(dato)  # Busca cada dato.
    fin = time.perf_counter()  # Tiempo final.

    return fin - inicio  # Devuelve el tiempo total.


def medir_eliminacion(lista, datos_eliminar):  # Función que mide el tiempo total de eliminación.
    inicio = time.perf_counter()  # Tiempo inicial.
    for dato in datos_eliminar:  # Recorre los datos a eliminar.
        lista.eliminar_por_valor(dato)  # Elimina cada dato.
    fin = time.perf_counter()  # Tiempo final.

    return fin - inicio  # Devuelve el tiempo total.


def ejecutar_experimento_csv(ruta_archivo, columna=0, tiene_encabezado=True, cantidad_pruebas=100):  # Ejecuta prueba automática.
    datos = leer_columna_csv(ruta_archivo, columna, tiene_encabezado)  # Lee los datos del CSV.

    if len(datos) == 0:  # Si no hay datos.
        print("\nNo hay datos para realizar el experimento.")  # Informa al usuario.
        return  # Sale de la función.

    tiempo_insercion, lista = medir_insercion(datos)  # Mide inserción y obtiene la lista cargada.

    muestra_busqueda = datos[:cantidad_pruebas]  # Toma una muestra para buscar.
    muestra_eliminacion = datos[:cantidad_pruebas]  # Toma una muestra para eliminar.

    tiempo_busqueda = medir_busqueda(lista, muestra_busqueda)  # Mide búsqueda.
    tiempo_eliminacion = medir_eliminacion(lista, muestra_eliminacion)  # Mide eliminación.

    print("\n========= RESULTADOS DEL EXPERIMENTO LISTA SIMPLE =========")
    print("Archivo analizado:", ruta_archivo)
    print("Cantidad de datos cargados:", len(datos))
    print("Tiempo total de inserción:", tiempo_insercion, "segundos")
    print("Tiempo total de búsqueda:", tiempo_busqueda, "segundos")
    print("Tiempo total de eliminación:", tiempo_eliminacion, "segundos")


def leer_entero(mensaje):  # Función para leer un número entero válido.
    while True:  # Repite hasta que el usuario escriba bien.
        try:  # Intenta convertir a entero.
            return int(input(mensaje))  # Devuelve el número.
        except ValueError:  # Si falla la conversión.
            print("Error: debe ingresar un número entero.")  # Muestra mensaje de error.


def leer_booleano_encabezado():  # Pregunta si el archivo tiene encabezado.
    respuesta = input("¿El archivo tiene encabezado? (s/n): ").strip().lower()  # Lee la respuesta.
    return respuesta == "s"  # Devuelve True si escribió s.


def mostrar_menu():  # Muestra el menú principal.
    print("\n--- MENÚ LISTA SIMPLEMENTE ENLAZADA ---")
    print("1. Insertar al principio")
    print("2. Insertar al final")
    print("3. Buscar por carnet")
    print("4. Eliminar por carnet")
    print("5. Mostrar lista")
    print("6. Graficar lista")
    print("7. Cargar lista desde archivo CSV")
    print("8. Ejecutar experimento con CSV")
    print("9. Vaciar lista")
    print("10. Salir")


def main():  # Función principal del programa.
    lista = Lista_Simple()  # Crea una lista vacía.

    while True:  # Mantiene el programa corriendo hasta salir.
        mostrar_menu()  # Muestra el menú.
        opcion = input("Seleccione una opción: ")  # Lee la opción del usuario.

        if opcion == "1":  # Insertar al principio.
            carnet = input("Carnet: ").strip()  # Lee el carnet.
            nombre = input("Nombre: ").strip()  # Lee el nombre.
            apellido = input("Apellido: ").strip()  # Lee el apellido.
            lista.insertar_al_principio(carnet, nombre, apellido)  # Inserta el nodo.
            lista.graficar(f"lista_simple_{lista.contador_img}")  # Genera imagen.
            lista.contador_img += 1  # Aumenta contador de imagen.
            print("✔ Dato insertado al principio")  # Mensaje de éxito.

        elif opcion == "2":  # Insertar al final.
            carnet = input("Carnet: ").strip()  # Lee el carnet.
            nombre = input("Nombre: ").strip()  # Lee el nombre.
            apellido = input("Apellido: ").strip()  # Lee el apellido.
            lista.insertar_al_final(carnet, nombre, apellido)  # Inserta el nodo.
            lista.graficar(f"lista_simple_{lista.contador_img}")  # Genera imagen.
            lista.contador_img += 1  # Aumenta contador de imagen.
            print("✔ Dato insertado al final")  # Mensaje de éxito.

        elif opcion == "3":  # Buscar dato.
            carnet = input("Carnet a buscar: ").strip()  # Lee el carnet.
            if lista.buscar(carnet):  # Busca el dato.
                print("✔ El carnet sí existe en la lista")  # Si lo encontró.
            else:  # Si no lo encontró.
                print("✘ El carnet no existe en la lista")

        elif opcion == "4":  # Eliminar dato.
            carnet = input("Carnet a eliminar: ").strip()  # Lee el carnet.
            if lista.eliminar_por_valor(carnet):  # Intenta eliminar.
                lista.graficar(f"lista_simple_{lista.contador_img}")  # Genera imagen.
                lista.contador_img += 1  # Aumenta contador.
                print("✔ Dato eliminado")  # Mensaje de éxito.
            else:  # Si no lo encontró.
                print("✘ Carnet no encontrado")

        elif opcion == "5":  # Mostrar lista.
            lista.mostrar_lista()  # Muestra la lista en consola.

        elif opcion == "6":  # Graficar lista.
            nombre = input("Ingrese el nombre para la imagen (sin extensión): ").strip()  # Pide nombre.
            if nombre == "":  # Si no escribe nada.
                nombre = "lista_simple"  # Usa nombre por defecto.
            lista.graficar(nombre)  # Genera la imagen.
            print("✔ Lista graficada correctamente")

        elif opcion == "7":  # Cargar CSV.
            ruta = input("Ingrese la ruta del archivo CSV: ").strip()  # Pide la ruta.
            columna = leer_entero("Ingrese el índice de la columna a usar (ejemplo 0, 1, 2): ")  # Pide la columna.
            encabezado = leer_booleano_encabezado()  # Pregunta si tiene encabezado.
            lista.cargar_desde_csv(ruta, columna, encabezado)  # Carga el archivo.

        elif opcion == "8":  # Ejecutar experimento.
            ruta = input("Ingrese la ruta del archivo CSV: ").strip()  # Pide ruta.
            columna = leer_entero("Ingrese el índice de la columna a usar (ejemplo 0, 1, 2): ")  # Pide columna.
            encabezado = leer_booleano_encabezado()  # Pregunta por encabezado.
            cantidad_pruebas = leer_entero("Ingrese cuántos datos usar para búsqueda y eliminación: ")  # Pide cantidad.
            ejecutar_experimento_csv(ruta, columna, encabezado, cantidad_pruebas)  # Ejecuta la prueba.

        elif opcion == "9":  # Vaciar lista.
            lista.vaciar()  # Borra todos los nodos.
            print("✔ La lista fue vaciada correctamente")

        elif opcion == "10":  # Salir.
            print("Saliendo del programa...")  # Mensaje final.
            break  # Termina el ciclo.

        else:  # Opción inválida.
            print("Opción inválida, intente nuevamente")  # Mensaje de error.


if __name__ == "__main__":  # Verifica si el archivo se ejecuta directamente.
    main()  # Llama a la función principal.
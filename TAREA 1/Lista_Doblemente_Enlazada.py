from graphviz import Digraph


class Nodo:
    def __init__(self, carnet, nombre, apellido):
        self.carnet = carnet
        self.nombre = nombre
        self.apellido = apellido
        self.siguiente = None
        self.anterior = None

    def texto(self):
        return f"{self.carnet}--{self.nombre}--{self.apellido}"


class Lista_Doble:
    def __init__(self):
        self.inicio = None
        self.final = None
        self.contador_img = 1  # para no sobrescribir imágenes

    def graficar(self, nombre_archivo="lista"):
        dot = Digraph(format="png")
        dot.attr(rankdir="LR")

        # None izquierdo y derecho
        dot.node("NONE_IZQ", "None", shape="box")
        dot.node("NONE_DER", "None", shape="box")

        # Si la lista está vacía
        if self.inicio is None:
            dot.edge("NONE_IZQ", "NONE_DER", label="vacía")
            dot.render(nombre_archivo, cleanup=True)
            return

        # Si NO está vacía
        temp = self.inicio
        i = 1
        ids = []

        while temp is not None:
            node_id = f"N{i}"
            ids.append(node_id)

            etiqueta = f"{temp.carnet}\\n{temp.nombre} {temp.apellido}"
            dot.node(node_id, etiqueta, shape="record")

            temp = temp.siguiente
            i += 1

        dot.edge("NONE_IZQ", ids[0])

        for j in range(len(ids) - 1):
            dot.edge(ids[j], ids[j + 1], label="sig")
            dot.edge(ids[j + 1], ids[j], label="ant")

        dot.edge(ids[-1], "NONE_DER")

        dot.render(nombre_archivo, cleanup=True)

    def insertar_al_principio(self, carnet, nombre, apellido):
        nd = Nodo(carnet, nombre, apellido)

        if self.inicio is None:
            self.inicio = nd
            self.final = nd
        else:
            nd.siguiente = self.inicio
            self.inicio.anterior = nd
            self.inicio = nd

    def insertar_al_final(self, carnet, nombre, apellido):
        nd = Nodo(carnet, nombre, apellido)

        if self.final is None:
            self.inicio = nd
            self.final = nd
        else:
            self.final.siguiente = nd
            nd.anterior = self.final
            self.final = nd

    def eliminar_por_valor(self, dato):
        temp = self.inicio

        while temp is not None:
            if temp.carnet == dato:

                # Caso 1: único nodo
                if temp == self.inicio and temp == self.final:
                    self.inicio = None
                    self.final = None

                # Caso 2: está al inicio
                elif temp == self.inicio:
                    self.inicio = temp.siguiente
                    self.inicio.anterior = None

                # Caso 3: está al final
                elif temp == self.final:
                    self.final = temp.anterior
                    self.final.siguiente = None

                # Caso 4: está en medio
                else:
                    temp.anterior.siguiente = temp.siguiente
                    temp.siguiente.anterior = temp.anterior

                return True

            temp = temp.siguiente

        return False

    def mostrar_lista(self):
        salida = "None <- "
        temp = self.inicio

        while temp is not None:
            salida += temp.texto()
            if temp.siguiente is not None:
                salida += " <-> "
            temp = temp.siguiente

        salida += " -> None"
        print(salida)


# ---------------- MENÚ ----------------
lista = Lista_Doble()

while True:
    print("\n--- MENÚ LISTA DOBLEMENTE ENLAZADA ---")
    print("1. Insertar al principio")
    print("2. Insertar al final")
    print("3. Eliminar por carnet")
    print("4. Mostrar lista")
    print("5. Salir")

    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        carnet = int(input("Carnet: "))
        nombre = input("Nombre: ")
        apellido = input("Apellido: ")
        lista.insertar_al_principio(carnet, nombre, apellido)

        # ✅ crear imagen
        lista.graficar(f"lista_{lista.contador_img}")
        lista.contador_img += 1

        print("✔ Estudiante insertado al principio")

    elif opcion == "2":
        carnet = int(input("Carnet: "))
        nombre = input("Nombre: ")
        apellido = input("Apellido: ")
        lista.insertar_al_final(carnet, nombre, apellido)

        # ✅ crear imagen
        lista.graficar(f"lista_{lista.contador_img}")
        lista.contador_img += 1

        print("✔ Estudiante insertado al final")

    elif opcion == "3":
        carnet = int(input("Carnet a eliminar: "))
        if lista.eliminar_por_valor(carnet):

            # ✅ crear imagen
            lista.graficar(f"lista_{lista.contador_img}")
            lista.contador_img += 1

            print("✔ Estudiante eliminado")
        else:
            print("✘ Carnet no encontrado")

    elif opcion == "4":
        lista.mostrar_lista()

    elif opcion == "5":
        print("Saliendo del programa...")
        break

    else:
        print("Opción inválida, intente nuevamente")

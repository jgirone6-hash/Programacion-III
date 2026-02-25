def convertir_a_binario(n):
    
    if n < 0:
        return "-" + convertir_a_binario(-n)

    # Caso base
    if n < 2:
        return str(n)

    # Caso recursivo
    return convertir_a_binario(n // 2) + str(n % 2)

def contar_digitos(n):
    n = abs(n)

    # Caso base
    if n < 10:
        return 1

    # Caso recursivo
    return 1 + contar_digitos(n // 10)

def raiz_cuadrada_entera(n):
    # Caso recursivo
    if n < 0:
        raise ValueError("No existe raíz cuadrada real para números negativos.")
    return calcular_raiz_cuadrada(n, 0)

     # Caso base
def calcular_raiz_cuadrada(n, candidato):
    if candidato * candidato > n:
        return candidato - 1
    return calcular_raiz_cuadrada(n, candidato + 1)

def romano_a_decimal(romano):
    valores = {'I':1,'V':5,'X':10,'L':50,'C':100,'D':500,'M':1000}

    if len(romano) == 0:
        return 0

    if len(romano) == 1:
        return valores[romano]

    if valores[romano[0]] < valores[romano[1]]:
        return -valores[romano[0]] + romano_a_decimal(romano[1:])
    else:
        return valores[romano[0]] + romano_a_decimal(romano[1:])

def suma_numeros_enteros(n):
    
    if n < 0:
        raise ValueError("n debe ser un entero positivo (>= 0).")

    # Caso base
    if n == 0:
        return 0

    # Caso recursivo
    return n + suma_numeros_enteros(n - 1)
    

while True:
    
    print("\n--- MENÚ FUNCIONES RECURSIVAS ---")
    print("1. Convertir a Binario")
    print("2. Contar Dígitos")
    print("3. Raíz Cuadrada Entera")
    print("4. Convertir a Decimal desde Romano ")
    print("5. Suma de Números Enteros")
    print("6. Salir")
    
    
    
    opcion = input ("Elija la opción a realizar: ").strip()


    if opcion == "1":
        n = int(input("Ingrese un número entero: "))
        print("Binario:", convertir_a_binario(n))

    elif opcion =="2":
        n = int(input("Ingrese un número entero: "))
        print("Número de dígitos: ",contar_digitos(n))
        
    elif opcion =="3":
        n = int(input("Ingrese un numero entero: "))
        print("Raiz cuadrada entera: ",raiz_cuadrada_entera(n)) 
         
    elif opcion =="4":
        romano = input("Ingrese un numero romano: ").upper().strip()
        print("Su numero decimal es: ", romano_a_decimal(romano))     
          
    elif opcion == "5":
            n = int(input("Ingrese un número entero positivo: "))
            print("Suma 0..n: ", suma_numeros_enteros(n))
    
    elif opcion == "6":
        print("Ha salido del programa")
        break

    else: 
        print("Opcion no disponible")    
        
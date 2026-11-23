"""Menú de consola de Chivas del Rodadero."""

from datetime import date

from business_logic import Empresa, NIVELES, validar_dias_simulados


def crear_chiva(empresa):
    nombre = input("Nombre de la chiva: ")
    puestos = input("Número de puestos: ")
    anio = input("Año de inicio: ")
    mes = input("Mes de inicio: ")
    dia = input("Día de inicio: ")
    chiva = empresa.crear_chiva(nombre, puestos, anio, mes, dia)
    print(f"Se creó la chiva «{chiva.nombre}».")


def elegir_chiva(empresa):
    return empresa.obtener_chiva(input("Nombre de la chiva: "))


def registrar_dia(empresa):
    chiva = elegir_chiva(empresa)
    fecha = chiva.fecha_siguiente()
    while True:
        try:
            chiva.registrar_dia(input(f"Pasajeros del {fecha}: "))
            print(f"Se registraron los pasajeros del {fecha}.")
            return
        except ValueError as error:
            print(error)


def simular_dias(empresa):
    chiva = elegir_chiva(empresa)
    dias = validar_dias_simulados(input("Número de días para simular: "))
    minimo = chiva.validar_pasajeros(input("Pasajeros mínimos: "))
    maximo = chiva.validar_pasajeros(input("Pasajeros máximos: "))
    chiva.simular_dias(dias, minimo, maximo)
    print(f"Se simularon {dias} días.")


def mostrar_informe(empresa):
    chiva = elegir_chiva(empresa)
    print(f"Chiva: {chiva.nombre}")
    print(f"Puestos: {chiva.puestos}")
    dias = chiva.dias_registrados()
    if dias == 0:
        print("La chiva no tiene días registrados.")
        return

    print(f"Días registrados: {dias}")
    print(f"Pasajeros totales: {chiva.total_pasajeros()}")
    print(f"Promedio de pasajeros por día: {round(chiva.promedio_diario(), 2)}")
    print(f"Porcentaje de ocupación: {round(chiva.ocupacion(), 2)} %")
    print(f"Desviación estándar: {round(chiva.desviacion_estandar(), 2)}")

    dia_mayor, dia_menor = chiva.fechas_extremas()
    print(f"Día con más pasajeros: {dia_mayor}")
    print(f"Día con menos pasajeros: {dia_menor}")

    print("Días por nivel de ocupación:")
    conteos = chiva.contar_niveles()
    for indice in range(len(NIVELES)):
        print(f"  {NIVELES[indice]}: {conteos[indice]}")

    longitud, inicio = chiva.racha_baja_mas_larga()
    if longitud == 0:
        print("No hubo días en ocupación baja.")
    else:
        print(f"Racha más larga en ocupación baja: {longitud} días, desde {inicio}.")

    ultimo_dia, pendientes = chiva.estado_del_registro(date.today())
    print(f"Último día registrado: {ultimo_dia}")
    if pendientes == 0:
        print("El registro está al día.")
    else:
        print(f"Días pendientes por registrar: {pendientes}")


def mostrar_extremos_de_ocupacion(empresa):
    mayor, menor = empresa.extremos_de_ocupacion()
    if mayor is None:
        print("Ninguna chiva tiene días registrados.")
        return
    print(f"Mayor ocupación: {mayor.nombre}, {round(mayor.ocupacion(), 2)} %")
    print(f"Menor ocupación: {menor.nombre}, {round(menor.ocupacion(), 2)} %")


def mostrar_descartes(descartes):
    for numero, causa in descartes:
        print(f"Línea {numero} descartada: {causa}")


def cargar_archivos(empresa):
    empresa.validar_carga()
    ruta_chivas = input("Ruta del CSV de chivas: ").strip()
    cargadas, descartes = empresa.cargar_chivas(ruta_chivas)
    mostrar_descartes(descartes)
    print(f"Chivas cargadas: {cargadas}")

    ruta_pasajeros = input("Ruta del CSV de pasajeros: ").strip()
    cargados, descartes = empresa.cargar_pasajeros(ruta_pasajeros)
    mostrar_descartes(descartes)
    print(f"Días cargados: {cargados}")


def mostrar_menu():
    print()
    print("Chivas del Rodadero")
    print("1. Crear una chiva")
    print("2. Registrar los pasajeros del día siguiente")
    print("3. Simular días")
    print("4. Ver el informe de una chiva")
    print("5. Ver las chivas con mayor y menor ocupación")
    print("6. Cargar chivas y pasajeros desde archivos")
    print("7. Salir")


def main():
    empresa = Empresa()
    while True:
        mostrar_menu()
        opcion = input("Elija una opción: ").strip()
        try:
            if opcion == "1":
                crear_chiva(empresa)
            elif opcion == "2":
                registrar_dia(empresa)
            elif opcion == "3":
                simular_dias(empresa)
            elif opcion == "4":
                mostrar_informe(empresa)
            elif opcion == "5":
                mostrar_extremos_de_ocupacion(empresa)
            elif opcion == "6":
                cargar_archivos(empresa)
            elif opcion == "7":
                return
            else:
                print("La opción no es válida.")
        except ValueError as error:
            print(error)


if __name__ == "__main__":
    main()

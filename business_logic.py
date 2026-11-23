"""Registros e indicadores de ocupación de Chivas del Rodadero."""

from datetime import date, timedelta
from random import randint


NIVELES = ("Baja", "Regular", "Buena", "Alta")


def leer_entero(valor):
    return int(str(valor))


def validar_dias_simulados(valor):
    try:
        dias = leer_entero(valor)
    except ValueError:
        raise ValueError("El número de días debe ser un número entero.")

    if dias < 1:
        raise ValueError("Se debe simular al menos un día.")

    return dias

class Chiva:
    def __init__(self, nombre, puestos, fecha_inicio):
        self.nombre = nombre
        self.puestos = puestos
        self.fecha_inicio = fecha_inicio
        self.pasajeros_por_dia = []

    def dias_registrados(self):
        return len(self.pasajeros_por_dia)

    def fecha_del_dia(self, dias_registrados):
        maximo_de_dias = (date.max - self.fecha_inicio).days
        if dias_registrados > maximo_de_dias:
            raise ValueError("El registro excede la última fecha del calendario.")
        return self.fecha_inicio + timedelta(days=dias_registrados)

    def fecha_siguiente(self):
        return self.fecha_del_dia(self.dias_registrados())

    def validar_pasajeros(self, valor):
        try:
            pasajeros = leer_entero(valor)
        except ValueError:
            raise ValueError("Los pasajeros deben ser un número entero.")
        if pasajeros < 0 or pasajeros > self.puestos:
            raise ValueError(f"Los pasajeros van de 0 a {self.puestos}.")
        return pasajeros

    def registrar_dia(self, valor):
        pasajeros = self.validar_pasajeros(valor)
        self.fecha_siguiente()
        self.pasajeros_por_dia.append(pasajeros)

    def simular_dias(self, dias, minimo, maximo):
        dias = validar_dias_simulados(dias)
        minimo = self.validar_pasajeros(minimo)
        maximo = self.validar_pasajeros(maximo)
        if minimo > maximo:
            raise ValueError("El mínimo no puede ser mayor que el máximo.")
        self.fecha_del_dia(self.dias_registrados() + dias - 1)
        for dia in range(dias):
            self.pasajeros_por_dia.append(randint(minimo, maximo))

    def total_pasajeros(self):
        return sum(self.pasajeros_por_dia)

    def promedio_diario(self):
        return self.total_pasajeros() / self.dias_registrados()

    def ocupacion(self):
        return self.promedio_diario() / self.puestos * 100

    def desviacion_estandar(self):
        dias = self.dias_registrados()
        if dias == 0:
            return 0.0

        mayor = max(self.pasajeros_por_dia)
        if mayor == 0:
            return 0.0

        total = self.total_pasajeros()
        escala = dias * mayor
        suma_cuadrados = 0.0
        for pasajeros in self.pasajeros_por_dia:
            # Se resta con enteros antes de dividir para evitar pérdida de precisión.
            diferencia_escalada = (pasajeros * dias - total) / escala
            suma_cuadrados += diferencia_escalada ** 2

        varianza_escalada = suma_cuadrados / dias
        return (varianza_escalada ** 0.5) * mayor

    def fechas_extremas(self):
        indice_mayor = 0
        indice_menor = 0
        for indice in range(1, self.dias_registrados()):
            pasajeros = self.pasajeros_por_dia[indice]
            if pasajeros > self.pasajeros_por_dia[indice_mayor]:
                indice_mayor = indice
            if pasajeros < self.pasajeros_por_dia[indice_menor]:
                indice_menor = indice
        fecha_con_mas = self.fecha_del_dia(indice_mayor)
        fecha_con_menos = self.fecha_del_dia(indice_menor)
        return fecha_con_mas, fecha_con_menos

    def nivel_de_ocupacion(self, pasajeros):
        # Se comparan enteros para respetar exactamente los tres cortes.
        pasajeros_por_cien = pasajeros * 100
        if pasajeros_por_cien < 45 * self.puestos:
            return 0
        if pasajeros_por_cien < 70 * self.puestos:
            return 1
        if pasajeros_por_cien < 90 * self.puestos:
            return 2
        return 3

    def contar_niveles(self):
        conteos = [0, 0, 0, 0]
        for pasajeros in self.pasajeros_por_dia:
            conteos[self.nivel_de_ocupacion(pasajeros)] += 1
        return conteos

    def racha_baja_mas_larga(self):
        longitud = 0
        inicio = 0
        mejor_longitud = 0
        mejor_inicio = 0
        for indice in range(self.dias_registrados()):
            pasajeros = self.pasajeros_por_dia[indice]
            if self.nivel_de_ocupacion(pasajeros) == 0:
                if longitud == 0:
                    inicio = indice
                longitud += 1
                if longitud > mejor_longitud:
                    mejor_longitud = longitud
                    mejor_inicio = inicio
            else:
                longitud = 0
        if mejor_longitud == 0:
            return 0, None
        return mejor_longitud, self.fecha_del_dia(mejor_inicio)

    def estado_del_registro(self, fecha_actual):
        ultimo_dia = self.fecha_del_dia(self.dias_registrados() - 1)
        pendientes = (fecha_actual - ultimo_dia).days - 1
        return ultimo_dia, max(0, pendientes)

    def comparar_ocupacion(self, otra):
        # Cada ocupación es el total dividido entre los puestos de todos sus días.
        # El producto cruzado compara las dos fracciones sin redondeo.
        total_propio = self.total_pasajeros()
        total_ajeno = otra.total_pasajeros()
        puestos_propios = self.dias_registrados() * self.puestos
        puestos_ajenos = otra.dias_registrados() * otra.puestos
        return total_propio * puestos_ajenos - total_ajeno * puestos_propios


def leer_filas(ruta):
    try:
        with open(ruta, encoding="utf-8-sig") as archivo:
            lineas = archivo.readlines()
    except FileNotFoundError:
        raise ValueError("El archivo no existe.")
    except UnicodeError:
        raise ValueError("El archivo debe estar codificado en UTF-8.")
    except OSError:
        raise ValueError("No se pudo leer el archivo.")

    filas = []
    for numero, linea in enumerate(lineas[1:], start=2):
        if linea.strip() != "":
            campos = []
            for campo in linea.split(";"):
                campos.append(campo.strip())
            filas.append((numero, campos))
    return filas


class Empresa:
    def __init__(self):
        self.chivas = []

    def buscar_chiva(self, nombre):
        nombre = nombre.strip()
        for chiva in self.chivas:
            if chiva.nombre == nombre:
                return chiva
        return None

    def obtener_chiva(self, nombre):
        chiva = self.buscar_chiva(nombre)
        if chiva is None:
            raise ValueError(f"No hay una chiva con el nombre «{nombre.strip()}».")
        return chiva

    def crear_chiva(self, nombre, puestos, anio, mes, dia):
        nombre = nombre.strip()
        if nombre == "":
            raise ValueError("El nombre no puede estar vacío.")
        if self.buscar_chiva(nombre) is not None:
            raise ValueError(f"Ya existe una chiva con el nombre «{nombre}».")

        try:
            puestos = leer_entero(puestos)
        except ValueError:
            raise ValueError("Los puestos deben ser un número entero.")
        if puestos < 1:
            raise ValueError("La chiva debe tener al menos un puesto.")

        mensaje = "La fecha no es válida."
        try:
            anio = leer_entero(anio)
            mes = leer_entero(mes)
            dia = leer_entero(dia)
        except ValueError:
            raise ValueError(mensaje)
        if not (1 <= anio <= 9999 and 1 <= mes <= 12 and 1 <= dia <= 31):
            raise ValueError(mensaje)
        try:
            fecha_inicio = date(anio, mes, dia)
        except ValueError:
            raise ValueError(mensaje)

        chiva = Chiva(nombre, puestos, fecha_inicio)
        self.chivas.append(chiva)
        return chiva

    def extremos_de_ocupacion(self):
        mayor = None
        menor = None
        for chiva in self.chivas:
            if chiva.dias_registrados() == 0:
                continue
            if mayor is None or chiva.comparar_ocupacion(mayor) > 0:
                mayor = chiva
            if menor is None or chiva.comparar_ocupacion(menor) < 0:
                menor = chiva
        return mayor, menor

    def validar_carga(self):
        if self.chivas:
            raise ValueError("La carga solo se hace con el programa sin chivas.")

    def cargar_chivas(self, ruta):
        self.validar_carga()
        cargadas = 0
        descartes = []
        for numero, campos in leer_filas(ruta):
            try:
                if len(campos) != 5:
                    raise ValueError("La línea debe tener cinco campos.")
                nombre, puestos, anio, mes, dia = campos
                self.crear_chiva(nombre, puestos, anio, mes, dia)
                cargadas += 1
            except ValueError as error:
                descartes.append((numero, str(error)))
        return cargadas, descartes

    def cargar_pasajeros(self, ruta):
        cargados = 0
        descartes = []
        for numero, campos in leer_filas(ruta):
            try:
                if len(campos) != 2:
                    raise ValueError("La línea debe tener dos campos.")
                nombre, pasajeros = campos
                self.obtener_chiva(nombre).registrar_dia(pasajeros)
                cargados += 1
            except ValueError as error:
                descartes.append((numero, str(error)))
        return cargados, descartes

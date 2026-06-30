# PROGRAMACIÓN - (213023A_2202)
# grupo: 213023_46
# fase 4: "Asistente Virtual FJ"
# integrantes del grupo:
# 1-Yeison Daniel Parra Jara
# Principios aplicados: Abstracción, Encapsulamiento, Herencia, Polimorfismo
# Sin base de datos: toda la información se guarda en listas y diccionarios

# Importamos 'abc' para poder crear clases abstractas
from abc import ABC, abstractmethod

# Importamos 'datetime' para manejar fechas y horas
from datetime import datetime


# CLASE ABSTRACTA BASE: EntidadSistema
# Esta clase define la estructura general que todas las entidades deben tener.

class EntidadSistema(ABC):
    """ Clase abstracta que representa cualquier entidad dentro del codigo y obliga a las clases hijas a implementar ciertos métodos esenciales."""

    def __init__(self, id_entidad: str):
        # Guardamos el ID con doble guión bajo para encapsularlo (acceso privado)
        self.__id_entidad = id_entidad

        # Fecha en que se creó esta entidad, se asigna automáticamente
        self.__fecha_creacion = datetime.now().strftime("%Y-%m-%d %H:%M")

    
    @abstractmethod
    def obtener_resumen(self) -> str:
        """Retorna un resumen de la entidad y Cada clase lo implementa a su manera."""
        pass

    # GETTERS: contiene losmétodos para leer atributos privados
    def get_id(self) -> str:
        """Retorna el ID único de la entidad."""
        return self.__id_entidad

    def get_fecha_creacion(self) -> str:
        """Retorna la fecha en que se creó esta entidad."""
        return self.__fecha_creacion

    def __str__(self) -> str:
        """Permite imprimir el objeto directamente con print()."""
        return self.obtener_resumen()



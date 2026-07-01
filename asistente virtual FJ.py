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

# CLASE: Cliente
# clase hereda de "EntidadSistema" y que Gestiona datos personales con encapsulamiento.
class Cliente(EntidadSistema):
    """ Representa a un cliente de la empresa FJ y Encapsula: nombre, correo, teléfono y lista de reservas del cliente.  """

    def __init__(self, id_cliente: str, nombre: str, correo: str, telefono: str):
        # Llamamos al constructor de la clase padre (EntidadSistema)
        super().__init__(id_cliente)

        # Validamos y guardamos los datos con doble guión bajo (privados)
        self.__nombre = self.__validar_nombre(nombre)
        self.__correo = self.__validar_correo(correo)
        self.__telefono = self.__validar_telefono(telefono)

        # Lista donde guardaremos los IDs de reservas que tiene este cliente
        self.__reservas = []

    # VALIDACIONES INTERNAS PARA LA CLASE CLIENTE:
    # validaciones para nombre, correo y teléfono, que lanzan ValueError si algo no es válido
    def __validar_nombre(self, nombre: str) -> str:
        """Verifica que el nombre no esté vacío y solo contenga letras y espacios."""
        nombre = nombre.strip()  # elimina espacios al inicio y al final del nombre del cliente
        if not nombre:
            raise ValueError("El nombre del cliente no puede estar vacío.")
        if not all(c.isalpha() or c.isspace() for c in nombre):
            raise ValueError("El nombre solo puede contener letras y espacios.")
        return nombre

    def __validar_correo(self, correo: str) -> str:
        """Verifica que el correo tenga formato básico con '@' y '.'"""
        correo = correo.strip()
        if "@" not in correo or "." not in correo:
            raise ValueError(f"El correo '{correo}' no tiene un formato válido.")
        return correo

    def __validar_telefono(self, telefono: str) -> str:
        """Verifica que el teléfono tenga entre 7 y 15 dígitos numéricos."""
        telefono = telefono.strip().replace(" ", "")  # Eliminamos espacios
        if not telefono.isdigit():
            raise ValueError("El teléfono solo puede contener dígitos.")
        if not (7 <= len(telefono) <= 15):
            raise ValueError("El teléfono debe tener entre 7 y 15 dígitos.")
        return telefono

    # GETTERS: para leer los datos privados desde afuera de la clase
    def get_nombre(self) -> str:
        """Retorna el nombre del cliente."""
        return self.__nombre

    def get_correo(self) -> str:
        """Retorna el correo del cliente."""
        return self.__correo

    def get_telefono(self) -> str:
        """Retorna el teléfono del cliente."""
        return self.__telefono

    def get_reservas(self) -> list:
        """Retorna una copia de la lista de reservas."""
        return list(self.__reservas)

    # SETTERS: que permiten modificar datos con validación
    def set_correo(self, nuevo_correo: str):
        """Permite actualizar el correo con validación."""
        self.__correo = self.__validar_correo(nuevo_correo)

    def set_telefono(self, nuevo_telefono: str):
        """Permite actualizar el teléfono con validación."""
        self.__telefono = self.__validar_telefono(nuevo_telefono)

    # MÉTODO PARA AGREGAR RESERVAS:
    def agregar_reserva(self, id_reserva: str):
        """Vincula una reserva a este cliente guardando su ID."""
        if id_reserva not in self.__reservas:  # previene duplicados
            self.__reservas.append(id_reserva)

    # IMPLEMENTACIÓN DEL MÉTODO ABSTRACTO 
    def obtener_resumen(self) -> str:
        """Retorna un resumen legible de la información del cliente."""
        return (
            f"[CLIENTE] ID: {self.get_id()} | "
            f"Nombre: {self.__nombre} | "
            f"Correo: {self.__correo} | "
            f"Teléfono: {self.__telefono} | "
            f"Reservas: {len(self.__reservas)}"
        )

# CLASE: Servicio
# Define la estructura base para todos los tipos de servicios que brinda la empresa FJ.
class Servicio(EntidadSistema):
    """ Clase abstracta que representa un servicio genérico de Software FJ. """

    def __init__(self, id_servicio: str, nombre: str, precio_hora: float):
        # Llamamos al constructor de EntidadSistema
        super().__init__(id_servicio)

        # Validamos y guardamos los datos
        self.__nombre = self.__validar_nombre(nombre)
        self.__precio_hora = self.__validar_precio(precio_hora)

        # Indica si el servicio está disponible para reservar
        self.__disponible = True

    # VALIDACIONES INTERNAS PARA LA CLASE SERVICIO 
    def __validar_nombre(self, nombre: str) -> str:
        """El nombre del servicio no puede estar vacío."""
        nombre = nombre.strip()
        if not nombre:
            raise ValueError("El nombre del servicio no puede estar vacío.")
        return nombre

    def __validar_precio(self, precio: float) -> float:
        """El precio por hora debe ser un valor positivo."""
        if precio <= 0:
            raise ValueError("El precio por hora debe ser mayor a 0.")
        return precio

    @abstractmethod
    def obtener_tipo(self) -> str:
        """Retorna el tipo de servicio (sala, equipo, asesoría)."""
        pass

    def get_nombre(self) -> str:
        return self.__nombre

    def get_precio_hora(self) -> float:
        return self.__precio_hora

    def esta_disponible(self) -> bool:
        """Retorna True si el servicio está disponible."""
        return self.__disponible

    def set_disponible(self, estado: bool):
        """Cambia la disponibilidad del servicio."""
        self.__disponible = estado

    def set_precio_hora(self, nuevo_precio: float):
        """Actualiza el precio por hora con validación."""
        self.__precio_hora = self.__validar_precio(nuevo_precio)

    def obtener_resumen(self) -> str:
        """Resumen general de cualquier servicio."""
        estado = "Disponible" if self.__disponible else "No disponible"
        return (
            f"SERVICIO: {self.obtener_tipo()} ID: {self.get_id()}-"
            f"Nombre: {self.__nombre} -"
            f"Precio/hora: ${self.__precio_hora:.2f} -"
            f"Estado: {estado}"
        )

# CLASE: ReservaSala (hereda de Servicio)
# Representa el servicio de reserva de salas de reunión o trabajo.
class ReservaSala(Servicio):
    """Servicio de reserva de salas con información de capacidad y equipamiento."""
    def __init__(self, id_servicio: str, nombre: str, precio_hora: float, capacidad: int, tiene_proyector: bool = False):

        # Llamamos al constructor de Servicio
        super().__init__(id_servicio, nombre, precio_hora)
        self.__capacidad = capacidad        
        self.__tiene_proyector = tiene_proyector  

    def get_capacidad(self) -> int:
        return self.__capacidad

    def tiene_proyector(self) -> bool:
        return self.__tiene_proyector

    def obtener_tipo(self) -> str:
        """Retorna la categoría de este servicio."""
        return "Sala de Reuniones"

    def obtener_resumen(self) -> str:
        """Extiende el resumen base con datos propios de la sala."""
        proyector = "Sí" if self.__tiene_proyector else "No"
        return (
            super().obtener_resumen() + f" Capacidad: {self.__capacidad} personas -Proyector: {proyector}"
        )

# CLASE: AlquilerEquipo (hereda de Servicio)
# Representa el servicio de alquiler de equipos tecnológicos.
class AlquilerEquipo(Servicio):
    """Servicio de alquiler de equipos con información del tipo de equipo y marca."""

    def __init__(self, id_servicio: str, nombre: str, precio_hora: float,
                 tipo_equipo: str, marca: str):
        super().__init__(id_servicio, nombre, precio_hora)

        # Datos específicos del equipo 
        self.__tipo_equipo = tipo_equipo  # Ej: "Laptop", "Cámara", "Proyector"
        self.__marca = marca              # Marca del equipo que sera alquilado

    def get_tipo_equipo(self) -> str:
        return self.__tipo_equipo

    def get_marca(self) -> str:
        return self.__marca

    def obtener_tipo(self) -> str:
        return "Alquiler de Equipo"

    def obtener_resumen(self) -> str:
        return (
            super().obtener_resumen() + f" - Equipo: {self.__tipo_equipo} - Marca: {self.__marca}"
        )

# CLASE: AsesoriaEspecializada (hereda de Servicio)
# Representa el servicio de asesoría con un especialista.
class AsesoriaEspecializada(Servicio):
    """Servicio de asesoría con nombre del asesor y área de especialidad."""

    def __init__(self, id_servicio: str, nombre: str, precio_hora: float, especialidad: str, nombre_asesor: str):
        super().__init__(id_servicio, nombre, precio_hora)

        # Datos específicos de la asesoría 
        self.__especialidad = especialidad      # Ej: "Redes", "Programación"
        self.__nombre_asesor = nombre_asesor    # Nombre del profesional

    def get_especialidad(self) -> str:
        return self.__especialidad

    def get_nombre_asesor(self) -> str:
        return self.__nombre_asesor

    def obtener_tipo(self) -> str:
        return "Asesoría Especializada"

    def obtener_resumen(self) -> str:
        return (
            super().obtener_resumen() + f" - Especialidad: {self.__especialidad} - Asesor: {self.__nombre_asesor}"
        )

# CLASE: Reserva
# Une a un Cliente con un Servicio en un rango de fecha y hora y calcula el costo total según las horas reservadas.
# También hereda de EntidadSistema para tener ID y fecha de creación.
class Reserva(EntidadSistema):
    """
    Representa una reserva realizada por un cliente para un servicio específico.
    Calcula automáticamente el costo total según las horas reservadas.
    """

    # Estados posibles de una reserva
    ESTADO_PENDIENTE   = "Pendiente"
    ESTADO_CONFIRMADA  = "Confirmada"
    ESTADO_CANCELADA   = "Cancelada"

    def __init__(self, id_reserva: str, cliente: Cliente, servicio: Servicio, horas: float):
        super().__init__(id_reserva)

        # Validamos que el servicio esté disponible antes de reservar
        if not servicio.esta_disponible():
            raise ValueError( f"El servicio '{servicio.get_nombre()}' no está disponible.")     

        # Validamos que las horas sean un número positivo
        if horas <= 0:
            raise ValueError("Las horas de reserva deben ser mayores a 0.")

        # Guardamos referencias al cliente y al servicio (objetos)
        self.__cliente  = cliente
        self.__servicio = servicio
        self.__horas    = horas

        # Calculamos el costo total automáticamente
        self.__costo_total = horas * servicio.get_precio_hora()

        # El estado inicial siempre es "Pendiente"
        self.__estado = Reserva.ESTADO_PENDIENTE

        # Guardamos la fecha en que se hizo la reserva
        self.__fecha_reserva = datetime.now().strftime("%Y-%m-%d %H:%M")

    def get_cliente(self) -> Cliente:
        return self.__cliente

    def get_servicio(self) -> Servicio:
        return self.__servicio

    def get_horas(self) -> float:
        return self.__horas

    def get_costo_total(self) -> float:
        return self.__costo_total

    def get_estado(self) -> str:
        return self.__estado

    def get_fecha_reserva(self) -> str:
        return self.__fecha_reserva

    # MÉTODOS PARA EL CAMBIO DE ESTADO:
    def confirmar(self):
        """Cambia el estado de la reserva a Confirmada."""
        if self.__estado == Reserva.ESTADO_CANCELADA:
            raise ValueError("No se puede confirmar una reserva cancelada.")
        self.__estado = Reserva.ESTADO_CONFIRMADA

    def cancelar(self):
        """Cambia el estado de la reserva a Cancelada y libera el servicio."""
        self.__estado = Reserva.ESTADO_CANCELADA

    def obtener_resumen(self) -> str:
        """Resumen completo de la reserva."""
        return (
            f"RESERVA ID: {self.get_id()} - "
            f"Cliente: {self.__cliente.get_nombre()} - "
            f"Servicio: {self.__servicio.get_nombre()} ({self.__servicio.obtener_tipo()}) - "
            f"Horas: {self.__horas} - "
            f"Total: ${self.__costo_total:.2f} - "
            f"Estado: {self.__estado} - "
            f"Fecha: {self.__fecha_reserva}"
        )





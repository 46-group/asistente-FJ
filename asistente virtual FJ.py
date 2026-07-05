# PROGRAMACIÓN - (213023A_2202)
# grupo: 213023_46
# fase 4: "Asistente Virtual FJ"
# integrantes del grupo:
# 1-Yeison Daniel Parra Jara
# 2-Gerson Daniel Arias Gonzalez
# Principios aplicados: Abstracción, Encapsulamiento, Herencia, Polimorfismo
# Sin base de datos: toda la información se guarda en listas y diccionarios

# Importamos 'abc' para poder crear clases abstractas
from abc import ABC, abstractmethod

# Importamos 'datetime' para manejar fechas y horas
from datetime import datetime
import logging
import os

# SISTEMA DE LOGS (registro de eventos y errores)
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/eventos.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def registrar_evento(mensaje: str):
    logging.info(mensaje)

def registrar_error(mensaje: str, excepcion: Exception = None):
    if excepcion is not None:
        logging.error(f"{mensaje} | Tipo: {type(excepcion).__name__} | Detalle: {excepcion}")
    else:
        logging.error(mensaje)

# --- EXCEPCIONES PERSONALIZADAS ---
class ErrorSistemaFJ(Exception):
    """Excepción base del sistema."""
    pass

class ClienteInvalidoException(ErrorSistemaFJ):
    pass

class ServicioInvalidoException(ErrorSistemaFJ):
    pass

class ServicioNoDisponibleException(ErrorSistemaFJ):
    pass

class DuracionInvalidaException(ErrorSistemaFJ):
    pass

class DatosFaltantesException(ErrorSistemaFJ):
    pass

class ReservaException(ErrorSistemaFJ):
    pass

class OperacionNoPermitidaException(ErrorSistemaFJ):
    pass


class EntidadSistema(ABC):
    def __init__(self, id_entidad: str):
        self.__id_entidad = id_entidad
        self.__fecha_creacion = datetime.now().strftime("%Y-%m-%d %H:%M")

    @abstractmethod
    def obtener_resumen(self) -> str:
        pass

    def get_id(self) -> str:
        return self.__id_entidad

    def get_fecha_creacion(self) -> str:
        return self.__fecha_creacion

    def __str__(self) -> str:
        return self.obtener_resumen()

class Cliente(EntidadSistema):
    def __init__(self, id_cliente: str, nombre: str, correo: str, telefono: str):
        super().__init__(id_cliente)
        try:
            self.__nombre = self.__validar_nombre(nombre)
            self.__correo = self.__validar_correo(correo)
            self.__telefono = self.__validar_telefono(telefono)
        except ValueError as e:
            registrar_error(f"No se pudo crear el cliente '{id_cliente}'", e)
            raise ClienteInvalidoException(f"Datos de cliente inválidos: {e}") from e

        self.__reservas = []

    def __validar_nombre(self, nombre: str) -> str:
        nombre = nombre.strip()
        if not nombre:
            raise ValueError("El nombre del cliente no puede estar vacío.")
        if not all(c.isalpha() or c.isspace() for c in nombre):
            raise ValueError("El nombre solo puede contener letras y espacios.")
        return nombre

    def __validar_correo(self, correo: str) -> str:
        correo = correo.strip()
        if "@" not in correo or "." not in correo:
            raise ValueError(f"El correo '{correo}' no tiene un formato válido.")
        return correo

    def __validar_telefono(self, telefono: str) -> str:
        telefono = telefono.strip().replace(" ", "")
        if not telefono.isdigit():
            raise ValueError("El teléfono solo puede contener dígitos.")
        if not (7 <= len(telefono) <= 15):
            raise ValueError("El teléfono debe tener entre 7 y 15 dígitos.")
        return telefono

    def get_nombre(self) -> str:
        return self.__nombre

    def get_correo(self) -> str:
        return self.__correo

    def get_telefono(self) -> str:
        return self.__telefono

    def get_reservas(self) -> list:
        return list(self.__reservas)

    def set_correo(self, nuevo_correo: str):
        self.__correo = self.__validar_correo(nuevo_correo)

    def set_telefono(self, nuevo_telefono: str):
        self.__telefono = self.__validar_telefono(nuevo_telefono)

    def agregar_reserva(self, id_reserva: str):
        if id_reserva not in self.__reservas:
            self.__reservas.append(id_reserva)

    def obtener_resumen(self) -> str:
        return (
            f"[CLIENTE] ID: {self.get_id()} | "
            f"Nombre: {self.__nombre} | "
            f"Correo: {self.__correo} | "
            f"Teléfono: {self.__telefono} | "
            f"Reservas: {len(self.__reservas)}"
        )

class Servicio(EntidadSistema):
    def __init__(self, id_servicio: str, nombre: str, precio_hora: float):
        super().__init__(id_servicio)
        self.__nombre = self.__validar_nombre(nombre)
        self.__precio_hora = self.__validar_precio(precio_hora)
        self.__disponible = True

    def __validar_nombre(self, nombre: str) -> str:
        nombre = nombre.strip()
        if not nombre:
            raise ValueError("El nombre del servicio no puede estar vacío.")
        return nombre

    def __validar_precio(self, precio: float) -> float:
        if precio <= 0:
            raise ValueError("El precio por hora debe ser mayor a 0.")
        return precio

    @abstractmethod
    def obtener_tipo(self) -> str:
        pass

    @abstractmethod
    def describir(self) -> str:
        pass

    @abstractmethod
    def validar_parametros(self) -> bool:
        pass

    @abstractmethod
    def calcular_costo(self, horas: float, impuesto: float = 0.0, descuento: float = 0.0) -> float:
        pass

    def _aplicar_impuesto_y_descuento(self, costo_base, impuesto, descuento) -> float:
        if impuesto < 0 or descuento < 0:
            raise DatosFaltantesException("Impuesto y descuento no pueden ser negativos.")
        costo = costo_base - (costo_base * descuento)
        costo = costo + (costo * impuesto)
        return round(costo, 2)

    def get_nombre(self) -> str:
        return self.__nombre

    def get_precio_hora(self) -> float:
        return self.__precio_hora

    def esta_disponible(self) -> bool:
        return self.__disponible

    def set_disponible(self, estado: bool):
        self.__disponible = estado

    def set_precio_hora(self, nuevo_precio: float):
        self.__precio_hora = self.__validar_precio(nuevo_precio)

    def obtener_resumen(self) -> str:
        estado = "Disponible" if self.__disponible else "No disponible"
        return (
            f"SERVICIO: {self.obtener_tipo()} ID: {self.get_id()}-"
            f"Nombre: {self.__nombre} -"
            f"Precio/hora: ${self.__precio_hora:.2f} -"
            f"Estado: {estado}"
        )

class ReservaSala(Servicio):
    def __init__(self, id_servicio: str, nombre: str, precio_hora: float, capacidad: int, tiene_proyector: bool = False):
        super().__init__(id_servicio, nombre, precio_hora)
        self.__capacidad = capacidad
        self.__tiene_proyector = tiene_proyector
        self.validar_parametros()

    def validar_parametros(self) -> bool:
        if self.__capacidad is None or self.__capacidad <= 0:
            raise DatosFaltantesException("La capacidad debe ser mayor a 0.")
        return True

    def describir(self) -> str:
        proyector = "con proyector" if self.__tiene_proyector else "sin proyector"
        return f"Sala para {self.__capacidad} personas, {proyector}."

    def calcular_costo(self, horas: float, impuesto: float = 0.0, descuento: float = 0.0) -> float:
        if horas <= 0:
            raise DuracionInvalidaException("Las horas deben ser mayores a 0.")
        costo = horas * self.get_precio_hora()
        if self.__tiene_proyector:
            costo += costo * 0.05
        return self._aplicar_impuesto_y_descuento(costo, impuesto, descuento)

    def get_capacidad(self) -> int:
        return self.__capacidad

    def tiene_proyector(self) -> bool:
        return self.__tiene_proyector

    def obtener_tipo(self) -> str:
        return "Sala de Reuniones"

    def obtener_resumen(self) -> str:
        proyector = "Sí" if self.__tiene_proyector else "No"
        return (
            super().obtener_resumen() + f" Capacidad: {self.__capacidad} personas -Proyector: {proyector}"
        )

class AlquilerEquipo(Servicio):
    def __init__(self, id_servicio: str, nombre: str, precio_hora: float,
                 tipo_equipo: str, marca: str):
        super().__init__(id_servicio, nombre, precio_hora)
        self.__tipo_equipo = tipo_equipo
        self.__marca = marca
        self.validar_parametros()

    def validar_parametros(self) -> bool:
        if not self.__tipo_equipo.strip() or not self.__marca.strip():
            raise DatosFaltantesException("Tipo de equipo y marca son obligatorios.")
        return True

    def describir(self) -> str:
        return f"Equipo tipo {self.__tipo_equipo}, marca {self.__marca}."

    def calcular_costo(self, horas: float, impuesto: float = 0.0, descuento: float = 0.0) -> float:
        if horas <= 0:
            raise DuracionInvalidaException("Las horas deben ser mayores a 0.")
        costo = horas * self.get_precio_hora() + 5000
        return self._aplicar_impuesto_y_descuento(costo, impuesto, descuento)

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

class AsesoriaEspecializada(Servicio):
    def __init__(self, id_servicio: str, nombre: str, precio_hora: float, especialidad: str, nombre_asesor: str):
        super().__init__(id_servicio, nombre, precio_hora)
        self.__especialidad = especialidad
        self.__nombre_asesor = nombre_asesor
        self.validar_parametros()

    def validar_parametros(self) -> bool:
        if not self.__especialidad.strip() or not self.__nombre_asesor.strip():
            raise DatosFaltantesException("Especialidad y asesor son obligatorios.")
        return True

    def describir(self) -> str:
        return f"Asesoría en {self.__especialidad}, con {self.__nombre_asesor}."

    def calcular_costo(self, horas: float, impuesto: float = 0.0, descuento: float = 0.0) -> float:
        if horas <= 0:
            raise DuracionInvalidaException("Las horas deben ser mayores a 0.")
        horas_cobradas = max(horas, 1)
        costo = horas_cobradas * self.get_precio_hora()
        return self._aplicar_impuesto_y_descuento(costo, impuesto, descuento)

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

class Reserva(EntidadSistema):
    ESTADO_PENDIENTE   = "Pendiente"
    ESTADO_CONFIRMADA  = "Confirmada"
    ESTADO_CANCELADA   = "Cancelada"

    def __init__(self, id_reserva: str, cliente: Cliente, servicio: Servicio, horas: float):
        super().__init__(id_reserva)

        if not servicio.esta_disponible():
            registrar_error(f"Intento de reservar servicio no disponible: {servicio.get_id()}")
            raise ServicioNoDisponibleException(f"El servicio '{servicio.get_nombre()}' no está disponible.")

        if horas <= 0:
            raise DuracionInvalidaException("Las horas de reserva deben ser mayores a 0.")

        self.__cliente  = cliente
        self.__servicio = servicio
        self.__horas    = horas

        try:
            self.__costo_total = servicio.calcular_costo(horas)
        except ErrorSistemaFJ as e:
            registrar_error(f"No se pudo calcular el costo de la reserva '{id_reserva}'", e)
            raise

        self.__estado = Reserva.ESTADO_PENDIENTE
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

    def confirmar(self):
        try:
            if self.__estado == Reserva.ESTADO_CANCELADA:
                raise ReservaException(f"No se puede confirmar {self.get_id()}: está cancelada.")
            if self.__estado == Reserva.ESTADO_CONFIRMADA:
                raise OperacionNoPermitidaException(f"{self.get_id()} ya estaba confirmada.")
        except (ReservaException, OperacionNoPermitidaException) as e:
            registrar_error(f"No se pudo confirmar {self.get_id()}", e)
            raise
        else:
            self.__estado = Reserva.ESTADO_CONFIRMADA
            registrar_evento(f"Reserva {self.get_id()} confirmada.")
        finally:
            registrar_evento(f"Intento de confirmación procesado: {self.get_id()}.")

    def cancelar(self):
        try:
            if self.__estado == Reserva.ESTADO_CANCELADA:
                raise OperacionNoPermitidaException(f"{self.get_id()} ya estaba cancelada.")
        except OperacionNoPermitidaException as e:
            registrar_error(f"No se pudo cancelar {self.get_id()}", e)
            raise
        else:
            self.__estado = Reserva.ESTADO_CANCELADA
            registrar_evento(f"Reserva {self.get_id()} cancelada.")
        finally:
            registrar_evento(f"Intento de cancelación procesado: {self.get_id()}.")

    def obtener_resumen(self) -> str:
        return (
            f"RESERVA ID: {self.get_id()} - "
            f"Cliente: {self.__cliente.get_nombre()} - "
            f"Servicio: {self.__servicio.get_nombre()} ({self.__servicio.obtener_tipo()}) - "
            f"Horas: {self.__horas} - "
            f"Total: ${self.__costo_total:.2f} - "
            f"Estado: {self.__estado} - "
            f"Fecha: {self.__fecha_reserva}"
        )

class SistemaFJ:
    def __init__(self):
        self.__clientes  = {}
        self.__servicios = {}
        self.__reservas  = {}
        self.__contador_reservas = 1
        print("   SISTEMA DE GESTIÓN  FJ   ")

    def registrar_cliente(self, id_cliente: str, nombre: str, correo: str, telefono: str):
        cliente_creado = None
        try:
            if id_cliente in self.__clientes:
                raise ClienteInvalidoException(f"Ya existe un cliente con el ID '{id_cliente}'.")
            cliente_creado = Cliente(id_cliente, nombre, correo, telefono)
        except (ClienteInvalidoException, DatosFaltantesException) as e:
            registrar_error("Error al registrar cliente", e)
            print(f"  ❌ Error: {e}")
        else:
            self.__clientes[id_cliente] = cliente_creado
            print(f"✔ Cliente registrado exitosamente: {cliente_creado.get_nombre()}")
        finally:
            registrar_evento(f"Intento de registro de cliente procesado (ID: {id_cliente}).")
        return cliente_creado

    def buscar_cliente(self, id_cliente: str) -> Cliente:
        if id_cliente not in self.__clientes:
            raise ClienteInvalidoException(f"No se encontró el cliente con ID '{id_cliente}'.")
        return self.__clientes[id_cliente]

    def listar_clientes(self):
        print("\n CLIENTES REGISTRADOS:")
        if not self.__clientes:
            print("  (No hay clientes registrados)")
            return
        for cliente in self.__clientes.values():
            print(" ", cliente.obtener_resumen())

    def registrar_servicio(self, servicio: Servicio):
        try:
            id_srv = servicio.get_id()
            if id_srv in self.__servicios:
                raise ServicioInvalidoException(f"Ya existe un servicio con el ID '{id_srv}'.")
        except ServicioInvalidoException as e:
            registrar_error("Error al registrar servicio", e)
            print(f"  ❌ Error: {e}")
        else:
            self.__servicios[servicio.get_id()] = servicio
            print(f"✔ Servicio registrado exitosamente: {servicio.get_nombre()} [{servicio.obtener_tipo()}]")
        finally:
            registrar_evento(f"Intento de registro de servicio procesado (ID: {servicio.get_id()}).")

    def buscar_servicio(self, id_servicio: str) -> Servicio:
        if id_servicio not in self.__servicios:
            raise ServicioInvalidoException(f"No se encontró el servicio con ID '{id_servicio}'.")
        return self.__servicios[id_servicio]

    def listar_servicios(self, solo_disponibles: bool = False):
        print("\nSERVICIOS:")
        if not self.__servicios:
            print("  (No hay servicios registrados)")
            return
        for servicio in self.__servicios.values():
            if solo_disponibles and not servicio.esta_disponible():
                continue
            print(" ", servicio.obtener_resumen())

    def crear_reserva(self, id_cliente: str, id_servicio: str, horas: float):
        nueva_reserva = None
        try:
            cliente = self.buscar_cliente(id_cliente)
            servicio = self.buscar_servicio(id_servicio)
            id_reserva = f"RES{self.__contador_reservas:03d}"
            nueva_reserva = Reserva(id_reserva, cliente, servicio, horas)
        except (ClienteInvalidoException, ServicioInvalidoException,
                ServicioNoDisponibleException, DuracionInvalidaException,
                DatosFaltantesException) as e:
            registrar_error("Error al crear la reserva", e)
            print(f"  ❌ Error: {e}")
        else:
            self.__contador_reservas += 1
            self.__reservas[nueva_reserva.get_id()] = nueva_reserva
            cliente.agregar_reserva(nueva_reserva.get_id())
            print(
                f"✔ Reserva creada exitosamente: {nueva_reserva.get_id()} - "
                f"Cliente: {cliente.get_nombre()} - "
                f"Servicio: {servicio.get_nombre()} - "
                f"Total: ${nueva_reserva.get_costo_total():.2f}"
            )
        finally:
            registrar_evento(f"Intento de creación de reserva procesado (Cliente: {id_cliente}, Servicio: {id_servicio}).")
        return nueva_reserva

    def confirmar_reserva(self, id_reserva: str):
        try:
            reserva = self.__buscar_reserva(id_reserva)
            reserva.confirmar()
        except (ReservaException, OperacionNoPermitidaException, DatosFaltantesException) as e:
            print(f"  ❌ Error: {e}")
        else:
            print(f"✔ Reserva {id_reserva} confirmada.")
        finally:
            registrar_evento(f"Intento de confirmación de reserva procesado (ID: {id_reserva}).")

    def cancelar_reserva(self, id_reserva: str):
        try:
            reserva = self.__buscar_reserva(id_reserva)
            reserva.cancelar()
        except (ReservaException, OperacionNoPermitidaException, DatosFaltantesException) as e:
            print(f"  ❌ Error: {e}")
        else:
            print(f"✔ Reserva {id_reserva} cancelada.")
        finally:
            registrar_evento(f"Intento de cancelación de reserva procesado (ID: {id_reserva}).")

    def __buscar_reserva(self, id_reserva: str) -> Reserva:
        if id_reserva not in self.__reservas:
            raise DatosFaltantesException(f"No se encontró la reserva con ID '{id_reserva}'.")
        return self.__reservas[id_reserva]

    def listar_reservas(self):
        print("\n RESERVAS REGISTRADAS:")
        if not self.__reservas:
            print("No hay reservas registradas")
            return
        for reserva in self.__reservas.values():
            print(" ", reserva.obtener_resumen())

    def reporte_general(self):
        print(" REPORTE GENERAL de la empresa FJ")
        total_clientes = len(self.__clientes)
        total_servicios = len(self.__servicios)
        total_reservas = len(self.__reservas)
        ingresos = sum(
            r.get_costo_total()
            for r in self.__reservas.values()
            if r.get_estado() == Reserva.ESTADO_CONFIRMADA
        )
        print(f"  Clientes registrados : {total_clientes}")
        print(f"  Servicios disponibles: {total_servicios}")
        print(f"  Reservas totales     : {total_reservas}")
        print(f"  Ingresos confirmados : ${ingresos:.2f}")


# FUNCIONES DEL MENÚ INTERACTIVO
# Cada función le pide al usuario los datos por teclado y llama al sistema.

def menu_registrar_cliente(sistema: SistemaFJ):
    """Le pide al usuario los datos de un cliente y lo registra en el sistema."""
    print("\n REGISTRAR CLIENTE:")
    id_c     = input("  ID del cliente (ej: C001)  : ").strip()
    nombre   = input("  Nombre completo            : ").strip()
    correo   = input("  Correo electrónico         : ").strip()
    telefono = input("  Teléfono (solo dígitos)    : ").strip()
    sistema.registrar_cliente(id_c, nombre, correo, telefono)

def menu_registrar_servicio(sistema: SistemaFJ):
    """
    Le pregunta al usuario qué tipo de servicio quiere registrar y solicita los datos correspondientes.
    """
    print("\n REGISTRAR SERVICIO:")
    print("  servicios disponibles:")
    print("    1. Sala de Reuniones")
    print("    2. Alquiler de Equipo")
    print("    3. Asesoría Especializada")

    tipo = input("  Elige el tipo de servicio que desea adquirir (1/2/3): ").strip()

    # Datos comunes a todos los tipos de servicio
    id_s       = input("  ID del servicio (ej: S001) : ").strip()
    nombre     = input("  Nombre del servicio        : ").strip()

    try:
        # Convertimos el precio a número flotante; si falla lanzamos error
        precio = float(input("  Precio por hora ($)        : ").strip())
    except ValueError:
        print("  ❌ Error: El precio debe ser solo números (ej: 50000).")
        return

    try:
        # Según el tipo elegido pedimos datos adicionales y creamos el objeto
        if tipo == "1":
            #  Sala de Reuniones
            capacidad_str = input("  Capacidad (número de personas): ").strip()
            if not capacidad_str.isdigit():
                print("  ❌ Error: La capacidad debe ser un número entero.")
                return
            capacidad  = int(capacidad_str)
            proyector  = input("  ¿Tiene proyector? (s/n)       : ").strip().lower()
            tiene_proy = proyector == "s"   # True si escribió 's', False si no
            servicio   = ReservaSala(id_s, nombre, precio, capacidad, tiene_proy)

        elif tipo == "2":
            #  Alquiler de Equipo
            tipo_eq  = input("  Tipo de equipo (ej: Laptop)   : ").strip()
            marca    = input("  Marca del equipo              : ").strip()
            servicio = AlquilerEquipo(id_s, nombre, precio, tipo_eq, marca)

        elif tipo == "3":
            #  Asesoría Especializada
            especialidad = input("  Especialidad (ej: Redes)      : ").strip()
            asesor       = input("  Nombre del asesor             : ").strip()
            servicio     = AsesoriaEspecializada(id_s, nombre, precio, especialidad, asesor)

        else:
            print("  ❌ Opción inválida. Elige el tipo de servicio que desea adquirir (1/2/3)")
            return

        # Registramos el servicio ya construido en el sistema
        sistema.registrar_servicio(servicio)

    except ErrorSistemaFJ as e:
        registrar_error("Error al construir el servicio desde el menú", e)
        print(f"  ❌ Error: {e}")

def menu_crear_reserva(sistema: SistemaFJ):
    """Le pide al usuario IDs de cliente y servicio, y las horas a reservar."""
    print("\n CREAR RESERVA: ")

    # Mostramos los disponibles para que el usuario sepa qué IDs usar
    sistema.listar_clientes()
    sistema.listar_servicios(solo_disponibles=True)

    id_cliente  = input("\n  ID del cliente  : ").strip()
    id_servicio = input("  ID del servicio : ").strip()

    try:
        horas = float(input("  Número de horas : ").strip())
    except ValueError:
        print("  ❌ Error: Las horas deben ser un número (ej: 2 o 1.5).")
        return

    sistema.crear_reserva(id_cliente, id_servicio, horas)

def menu_confirmar_reserva(sistema: SistemaFJ):
    """Le pide el ID de una reserva y la confirma."""
    print("\n CONFIRMAR RESERVA: ")
    sistema.listar_reservas()
    id_res = input("\n  ID de la reserva a confirmar: ").strip()
    sistema.confirmar_reserva(id_res)

def menu_cancelar_reserva(sistema: SistemaFJ):
    """Le pide el ID de una reserva y la cancela."""
    print("\nCANCELAR RESERVA:")
    sistema.listar_reservas()
    id_res = input("\n  ID de la reserva a cancelar: ").strip()
    sistema.cancelar_reserva(id_res)

def menu_actualizar_cliente(sistema: SistemaFJ):
    """Permite actualizar el correo o el teléfono de un cliente existente."""
    print("\n ACTUALIZACION DE DATOS DE CLIENTE:")
    sistema.listar_clientes()
    id_c = input("\n  ID del cliente a actualizar: ").strip()
    try:
        cliente = sistema.buscar_cliente(id_c)
    except ClienteInvalidoException as e:
        print(f"  ❌ Error: {e}")
        return

    print(f"  Cliente encontrado: {cliente.obtener_resumen()}")
    print("  ¿Qué deseas actualizar?")
    print("    1. Correo electrónico")
    print("    2. Teléfono")
    opcion = input("  Elige (1/2): ").strip()

    try:
        if opcion == "1":
            nuevo = input("  Nuevo correo: ").strip()
            cliente.set_correo(nuevo)
            print("  ✔ Correo actualizado correctamente.")
        elif opcion == "2":
            nuevo = input("  Nuevo teléfono: ").strip()
            cliente.set_telefono(nuevo)
            print("  ✔ Teléfono actualizado correctamente.")
        else:
            print("  ❌ Opción inválida.")
    except ValueError as e:
        registrar_error(f"No se pudo actualizar datos del cliente {id_c}", e)
        print(f"  ❌ Error: {e}")


# BLOQUE PRINCIPAL: Menú interactivo en consola
# El programa queda en un ciclo hasta que el usuario elija "Salir".
if __name__ == "__main__":
    # Creamos la instancia del sistema
    sistema = SistemaFJ()

    # Opciones del menú principal
    opciones = {
        "1": "Registrar cliente",
        "2": "Registrar servicio",
        "3": "Crear reserva",
        "4": "Confirmar reserva",
        "5": "Cancelar reserva",
        "6": "Actualizar datos de cliente",
        "7": "Ver todos los clientes",
        "8": "Ver todos los servicios",
        "9": "Ver todas las reservas",
        "10": "Reporte general",
        "0": "Salir",
    }

    # Ciclo principal: el menú se repite hasta que el usuario elija 0
    while True:
        try:
            print("\n" + "=" * 50)
            print("       MENÚ PRINCIPAL DEL SISTEMA DE GESTIÓN FJ      ")
            print("=" * 50)
            for clave, descripcion in opciones.items():
                print(f"  [{clave}] {descripcion}")

            eleccion = input("  Elige una opción: ").strip()

            if eleccion == "1":
                menu_registrar_cliente(sistema)
            elif eleccion == "2":
                menu_registrar_servicio(sistema)
            elif eleccion == "3":
                menu_crear_reserva(sistema)
            elif eleccion == "4":
                menu_confirmar_reserva(sistema)
            elif eleccion == "5":
                menu_cancelar_reserva(sistema)
            elif eleccion == "6":
                menu_actualizar_cliente(sistema)
            elif eleccion == "7":
                sistema.listar_clientes()
            elif eleccion == "8":
                sistema.listar_servicios()
            elif eleccion == "9":
                sistema.listar_reservas()
            elif eleccion == "10":
                sistema.reporte_general()
            elif eleccion == "0":
                print("\n  ✔ Hasta luego. Sistema de Gestion FJ cerrado.\n")
                registrar_evento("Sistema cerrado por el usuario.")
                break
            else:
                print("  ❌ Opción no válida. Por favor elige un número del menú.")

        except ErrorSistemaFJ as e:
            registrar_error("Error del sistema no manejado en un punto específico", e)
            print(f"  ❌ Ocurrió un error: {e}")
        except Exception as e:
            registrar_error("Error inesperado en el ciclo principal", e)
            print("  ❌ Ocurrió un error inesperado. Fue registrado en logs/eventos.log.")
        finally:
            registrar_evento("Iteración del menú principal finalizada.")
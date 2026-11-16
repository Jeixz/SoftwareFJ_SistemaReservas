"""
Módulo de Servicios de Software FJ.
Implementa herencia, polimorfismo y sobrecarga de métodos en el cálculo de tarifas.
"""

from abc import abstractmethod
from functools import singledispatchmethod
from modelos.entidad_base import EntidadSistema
from utilidades.excepciones import (
    DatoInvalidoError,
    ParametroFaltanteError,
    ServicioNoDisponibleError,
    CalculoInconsistenteError,
)


class Servicio(EntidadSistema):
    """Clase abstracta que modela cualquier servicio ofertado por Software FJ."""

    def __init__(self, id_servicio: str, nombre: str, tarifa_base: float, disponible: bool = True):
        super().__init__(id_servicio)
        if not nombre or not isinstance(nombre, str) or len(nombre.strip()) < 3:
            raise ParametroFaltanteError("El nombre del servicio es obligatorio (mínimo 3 caracteres).")
        if not isinstance(tarifa_base, (int, float)) or tarifa_base <= 0:
            raise DatoInvalidoError(f"La tarifa base debe ser un número positivo. Recibido: {tarifa_base}")

        self._nombre = nombre.strip()
        self._tarifa_base = float(tarifa_base)
        self._disponible = bool(disponible)

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def tarifa_base(self) -> float:
        return self._tarifa_base

    @property
    def disponible(self) -> bool:
        return self._disponible

    @disponible.setter
    def disponible(self, estado: bool) -> None:
        if not isinstance(estado, bool):
            raise DatoInvalidoError("El estado de disponibilidad debe ser booleano (True/False).")
        self._disponible = estado

    def verificar_disponibilidad(self) -> None:
        """Lanza excepción si el servicio no está disponible para reservar."""
        if not self._disponible:
            raise ServicioNoDisponibleError(
                f"El servicio '{self._nombre}' ({self.id_entidad}) no se encuentra disponible actualmente."
            )

    @abstractmethod
    def validar_parametros_servicio(self, duracion_horas: int) -> None:
        """Cada servicio especializado valida sus propias reglas de negocio."""
        pass

    @abstractmethod
    def calcular_costo_base_especializado(self, duracion_horas: int) -> float:
        """Método polimórfico que calcula el subtotal según la naturaleza de cada servicio."""
        pass

    @abstractmethod
    def describir_servicio(self) -> str:
        """Método polimórfico que retorna los detalles técnicos del servicio."""
        pass

    @singledispatchmethod
    def calcular_costo(self, duracion_horas: int, descuento: float = 0.0, impuesto_iva: float = 0.19) -> float:
        """
        Sobrecarga 1 (Por defecto con int): Calcula el costo total aplicando descuento e IVA.
        """
        self.validar_parametros_servicio(duracion_horas)

        if not (0.0 <= descuento <= 0.50):
            raise CalculoInconsistenteError(f"Descuento fuera de rango permitido (0% a 50%): {descuento * 100}%")
        if not (0.0 <= impuesto_iva <= 0.30):
            raise CalculoInconsistenteError(f"IVA fuera de rango permitido (0% a 30%): {impuesto_iva * 100}%")

        subtotal = self.calcular_costo_base_especializado(duracion_horas)
        monto_descuento = subtotal * descuento
        base_gravable = subtotal - monto_descuento
        total = base_gravable * (1 + impuesto_iva)

        if total <= 0:
            raise CalculoInconsistenteError("El cálculo final del servicio arrojó un valor menor o igual a cero.")

        return round(total, 2)

    @calcular_costo.register
    def _(self, configuracion: dict) -> float:
        """
        Sobrecarga 2 (Con diccionario de parámetros): Permite pasar un paquete de configuración
        con llaves opcionales {'horas': int, 'descuento': float, 'iva': float, 'exento_iva': bool}.
        """
        if "horas" not in configuracion:
            raise ParametroFaltanteError("El diccionario de cálculo debe incluir la clave 'horas'.")
        horas = configuracion["horas"]
        descuento = configuracion.get("descuento", 0.0)
        iva = 0.0 if configuracion.get("exento_iva", False) else configuracion.get("iva", 0.19)
        return self.calcular_costo(horas, descuento=descuento, impuesto_iva=iva)

    def validar_integridad(self) -> bool:
        return self._tarifa_base > 0 and bool(self._nombre)

    def obtener_resumen(self) -> str:
        estado = "Disponible" if self._disponible else "No Disponible"
        return f"[{self.id_entidad}] {self.describir_servicio()} | Estado: {estado}"


class ReservaSala(Servicio):
    """Servicio especializado 1: Reserva de salas de conferencias o coworking."""

    def __init__(self, id_servicio: str, nombre: str, tarifa_hora: float, capacidad_personas: int, tiene_videobeam: bool = True, disponible: bool = True):
        super().__init__(id_servicio, nombre, tarifa_hora, disponible)
        if not isinstance(capacidad_personas, int) or capacidad_personas < 2 or capacidad_personas > 100:
            raise DatoInvalidoError(f"Capacidad de sala inválida ({capacidad_personas}). Debe estar entre 2 y 100 personas.")
        self._capacidad_personas = capacidad_personas
        self._tiene_videobeam = bool(tiene_videobeam)

    def validar_parametros_servicio(self, duracion_horas: int) -> None:
        if not isinstance(duracion_horas, int) or duracion_horas < 1 or duracion_horas > 12:
            raise DatoInvalidoError(f"La reserva de sala requiere entre 1 y 12 horas. Solicitado: {duracion_horas}")

    def calcular_costo_base_especializado(self, duracion_horas: int) -> float:
        recargo_audiovisual = 25000.0 if self._tiene_videobeam else 0.0
        return (self._tarifa_base * duracion_horas) + recargo_audiovisual

    def describir_servicio(self) -> str:
        equipo = "con VideoBeam" if self._tiene_videobeam else "sin equipo audiovisual"
        return f"Sala '{self._nombre}' (Capacidad: {self._capacidad_personas} pers., {equipo}) - ${self._tarifa_base:,.0f}/hora"


class AlquilerEquipo(Servicio):
    """Servicio especializado 2: Alquiler de hardware, servidores portátiles o estaciones de trabajo."""

    def __init__(self, id_servicio: str, nombre: str, tarifa_hora: float, categoria_hardware: str, deposito_garantia: float, disponible: bool = True):
        super().__init__(id_servicio, nombre, tarifa_hora, disponible)
        if not categoria_hardware or not isinstance(categoria_hardware, str):
            raise ParametroFaltanteError("La categoría de hardware es obligatoria.")
        if not isinstance(deposito_garantia, (int, float)) or deposito_garantia < 0:
            raise DatoInvalidoError("El depósito de garantía no puede ser negativo.")

        self._categoria_hardware = categoria_hardware.strip()
        self._deposito_garantia = float(deposito_garantia)

    def validar_parametros_servicio(self, duracion_horas: int) -> None:
        if not isinstance(duracion_horas, int) or duracion_horas < 2 or duracion_horas > 72:
            raise DatoInvalidoError(f"El alquiler de equipos requiere mínimo 2 horas y máximo 72 horas. Solicitado: {duracion_horas}")

    def calcular_costo_base_especializado(self, duracion_horas: int) -> float:
        return (self._tarifa_base * duracion_horas) + self._deposito_garantia

    def describir_servicio(self) -> str:
        return (
            f"Alquiler Equipo '{self._nombre}' [Cat: {self._categoria_hardware}] - "
            f"${self._tarifa_base:,.0f}/hora + Garantía ${self._deposito_garantia:,.0f}"
        )


class AsesoriaEspecializada(Servicio):
    """Servicio especializado 3: Consultoría en arquitectura de software, redes o ciberseguridad."""

    def __init__(self, id_servicio: str, nombre: str, tarifa_hora: float, area_especialidad: str, nivel_senior: bool = True, disponible: bool = True):
        super().__init__(id_servicio, nombre, tarifa_hora, disponible)
        if not area_especialidad or not isinstance(area_especialidad, str):
            raise ParametroFaltanteError("El área de especialidad de la asesoría es obligatoria.")
        self._area_especialidad = area_especialidad.strip()
        self._nivel_senior = bool(nivel_senior)

    def validar_parametros_servicio(self, duracion_horas: int) -> None:
        if not isinstance(duracion_horas, int) or duracion_horas < 1 or duracion_horas > 40:
            raise DatoInvalidoError(f"La asesoría especializada admite entre 1 y 40 horas. Solicitado: {duracion_horas}")

    def calcular_costo_base_especializado(self, duracion_horas: int) -> float:
        factor = 1.25 if self._nivel_senior else 1.0
        return self._tarifa_base * factor * duracion_horas

    def describir_servicio(self) -> str:
        nivel = "Consultor Senior" if self._nivel_senior else "Consultor Semi-Senior"
        return f"Asesoría '{self._nombre}' [{self._area_especialidad} - {nivel}] - ${self._tarifa_base:,.0f}/hora"

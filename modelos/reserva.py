"""
Módulo de Reserva que integra Cliente, Servicio, duración y máquina de estados.
Implementa confirmación, cancelación, procesamiento y encadenamiento de excepciones.
"""

from modelos.entidad_base import EntidadSistema
from modelos.cliente import Cliente
from modelos.servicio import Servicio
from utilidades.excepciones import (
    DatoInvalidoError,
    OperacionNoPermitidaError,
    ErrorSistemaFJ,
)
from utilidades.logger import GestorLogs


class Reserva(EntidadSistema):
    """Gestiona el ciclo de vida completo de una reserva en Software FJ."""

    ESTADOS_VALIDOS = ("PENDIENTE", "CONFIRMADA", "PROCESADA", "CANCELADA")

    def __init__(self, id_reserva: str, cliente: Cliente, servicio: Servicio, duracion_horas: int, descuento: float = 0.0):
        super().__init__(id_reserva)
        self._logger = GestorLogs()

        if not isinstance(cliente, Cliente):
            raise DatoInvalidoError("La reserva requiere una instancia válida de Cliente.")
        if not isinstance(servicio, Servicio):
            raise DatoInvalidoError("La reserva requiere una instancia válida de Servicio.")

        servicio.verificar_disponibilidad()
        servicio.validar_parametros_servicio(duracion_horas)

        self._cliente = cliente
        self._servicio = servicio
        self._duracion_horas = duracion_horas
        self._descuento = descuento
        self._estado = "PENDIENTE"
        self._costo_total = 0.0

        try:
            self._costo_total = self._servicio.calcular_costo(self._duracion_horas, descuento=self._descuento)
        except Exception as error_original:
            raise ErrorSistemaFJ(
                f"Fallo crítico al calcular tarifa inicial para la reserva {self.id_entidad}.",
                codigo_error="ERR-RES-CALC"
            ) from error_original

    @property
    def estado(self) -> str:
        return self._estado

    @property
    def costo_total(self) -> float:
        return self._costo_total

    def confirmar(self) -> None:
        """Confirma una reserva pendiente utilizando bloque try/except/else/finally."""
        try:
            if self._estado != "PENDIENTE":
                raise OperacionNoPermitidaError(
                    f"No se puede confirmar la reserva {self.id_entidad} porque su estado actual es '{self._estado}'."
                )
            self._servicio.verificar_disponibilidad()
        except ErrorSistemaFJ as e:
            self._logger.registrar_error(f"Error al confirmar reserva {self.id_entidad}: {e}")
            raise
        else:
            self._estado = "CONFIRMADA"
            self._cliente.agregar_reserva_historial(self.id_entidad)
            self._logger.registrar_info(
                f"Reserva {self.id_entidad} CONFIRMADA para {self._cliente.nombre_completo} | Total: ${self._costo_total:,.2f}"
            )
        finally:
            self._logger.registrar_info(f"Auditoría de transición ejecutada sobre {self.id_entidad} (Estado: {self._estado}).")

    def procesar(self, exento_iva: bool = False) -> float:
        """
        Procesa el cobro y ejecución final de una reserva confirmada.
        Utiliza la variante sobrecargada de calcular_costo con diccionario.
        """
        try:
            if self._estado != "CONFIRMADA":
                raise OperacionNoPermitidaError(
                    f"La reserva {self.id_entidad} debe estar CONFIRMADA para procesarse (Estado actual: '{self._estado}')."
                )
            parametros_calculo = {
                "horas": self._duracion_horas,
                "descuento": self._descuento,
                "exento_iva": exento_iva,
            }
            self._costo_total = self._servicio.calcular_costo(parametros_calculo)
        except Exception as exc:
            self._logger.registrar_error(f"Fallo en procesamiento de {self.id_entidad}: {exc}")
            raise OperacionNoPermitidaError(
                f"Imposible procesar la reserva {self.id_entidad} debido a un error operativo."
            ) from exc
        else:
            self._estado = "PROCESADA"
            self._logger.registrar_info(
                f"Reserva {self.id_entidad} PROCESADA exitosamente. Valor final facturado: ${self._costo_total:,.2f}"
            )
            return self._costo_total
        finally:
            self._logger.registrar_info(f"Cierre de transacción de procesamiento para {self.id_entidad}.")

    def cancelar(self, motivo: str) -> None:
        """Cancela una reserva siempre y cuando no haya sido procesada ni cancelada previamente."""
        if not motivo or not motivo.strip():
            raise DatoInvalidoError("Debe proporcionar un motivo válido para cancelar la reserva.")

        if self._estado in ("PROCESADA", "CANCELADA"):
            raise OperacionNoPermitidaError(
                f"Operación denegada: la reserva {self.id_entidad} ya se encuentra en estado '{self._estado}'."
            )

        self._estado = "CANCELADA"
        self._logger.registrar_advertencia(
            f"Reserva {self.id_entidad} CANCELADA. Motivo: {motivo.strip()}"
        )

    def validar_integridad(self) -> bool:
        return self._estado in self.ESTADOS_VALIDOS and self._costo_total > 0

    def obtener_resumen(self) -> str:
        return (
            f"Reserva [{self.id_entidad}] | Estado: {self._estado} | "
            f"Cliente: {self._cliente.nombre_completo} | Servicio: {self._servicio.nombre} | "
            f"Duración: {self._duracion_horas}h | Total: ${self._costo_total:,.2f}"
        )

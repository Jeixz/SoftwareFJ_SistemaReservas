"""
Módulo de excepciones personalizadas para el sistema de gestión de Software FJ.
Permite capturar y diferenciar errores específicos del dominio sin detener el programa.
"""


class ErrorSistemaFJ(Exception):
    """Excepción base para todos los errores controlados del sistema Software FJ."""

    def __init__(self, mensaje: str, codigo_error: str = "ERR-000"):
        self.codigo_error = codigo_error
        super().__init__(f"[{codigo_error}] {mensaje}")


class DatoInvalidoError(ErrorSistemaFJ):
    """Se lanza cuando un parámetro tiene un formato, tipo o rango incorrecto."""

    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo_error="ERR-DATO-001")


class ParametroFaltanteError(ErrorSistemaFJ):
    """Se lanza cuando falta un argumento obligatorio para construir o procesar una entidad."""

    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo_error="ERR-PARAM-002")


class ServicioNoDisponibleError(ErrorSistemaFJ):
    """Se lanza cuando se intenta reservar o usar un servicio inactivo o sin cupo."""

    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo_error="ERR-SERV-003")


class OperacionNoPermitidaError(ErrorSistemaFJ):
    """Se lanza al intentar realizar una transición de estado inválida (ej. cancelar una reserva finalizada)."""

    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo_error="ERR-OPER-004")


class CalculoInconsistenteError(ErrorSistemaFJ):
    """Se lanza cuando un cálculo financiero arroja valores negativos, nulos o fuera de política."""

    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo_error="ERR-CALC-005")

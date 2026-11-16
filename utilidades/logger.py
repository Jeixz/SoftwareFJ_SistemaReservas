"""
Módulo de registro de eventos y errores (Logging) en archivo plano.
Cumple con el requisito de persistencia únicamente para trazabilidad y auditoría.
"""

import logging
import os


class GestorLogs:
    """Clase encargada de configurar y centralizar el registro de eventos y errores."""

    _instancia = None

    def __new__(cls, ruta_archivo: str = "logs/sistema_fj.log"):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia._inicializar_logger(ruta_archivo)
        return cls._instancia

    def _inicializar_logger(self, ruta_archivo: str) -> None:
        """Crea el directorio de logs si no existe y configura el formato de salida."""
        directorio = os.path.dirname(ruta_archivo)
        if directorio and not os.path.exists(directorio):
            os.makedirs(directorio)

        self.logger = logging.getLogger("SoftwareFJ")
        self.logger.setLevel(logging.DEBUG)

        if not self.logger.handlers:
            archivo_handler = logging.FileHandler(ruta_archivo, mode="a", encoding="utf-8")
            formato = logging.Formatter(
                "%(asctime)s | %(levelname)-8s | %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )
            archivo_handler.setFormatter(formato)
            self.logger.addHandler(archivo_handler)

    def registrar_info(self, mensaje: str) -> None:
        """Registra una operación exitosa o evento informativo."""
        self.logger.info(mensaje)

    def registrar_advertencia(self, mensaje: str) -> None:
        """Registra una situación anómala controlada."""
        self.logger.warning(mensaje)

    def registrar_error(self, mensaje: str, exc_info: bool = False) -> None:
        """Registra un error o excepción capturada con opción de traza completa."""
        self.logger.error(mensaje, exc_info=exc_info)

"""
Clase abstracta base para todas las entidades del sistema Software FJ.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from utilidades.excepciones import ParametroFaltanteError


class EntidadSistema(ABC):
    """
    Clase abstracta que representa cualquier entidad general del sistema
    (Clientes, Servicios, Reservas).
    """

    def __init__(self, id_entidad: str):
        if not id_entidad or not isinstance(id_entidad, str) or not id_entidad.strip():
            raise ParametroFaltanteError("El identificador de la entidad es obligatorio y debe ser texto válido.")
        self._id_entidad = id_entidad.strip().upper()
        self._fecha_creacion = datetime.now()

    @property
    def id_entidad(self) -> str:
        """Retorna el identificador único encapsulado de la entidad."""
        return self._id_entidad

    @property
    def fecha_creacion(self) -> datetime:
        """Retorna la marca de tiempo en que fue instanciada la entidad."""
        return self._fecha_creacion

    @abstractmethod
    def validar_integridad(self) -> bool:
        """Método abstracto que obliga a las clases hijas a validar su estado interno."""
        pass

    @abstractmethod
    def obtener_resumen(self) -> str:
        """Método abstracto para obtener una representación textual estandarizada."""
        pass

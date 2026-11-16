"""
Módulo que define la clase Cliente con encapsulación y validaciones estrictas.
"""

import re
from modelos.entidad_base import EntidadSistema
from utilidades.excepciones import DatoInvalidoError, ParametroFaltanteError


class Cliente(EntidadSistema):
    """Representa un cliente registrado en Software FJ."""

    def __init__(self, id_cliente: str, nombre_completo: str, documento: str, correo: str, telefono: str):
        super().__init__(id_cliente)
        self.nombre_completo = nombre_completo
        self.documento = documento
        self.correo = correo
        self.telefono = telefono
        self._historial_reservas = []
        self.validar_integridad()

    @property
    def nombre_completo(self) -> str:
        return self._nombre_completo

    @nombre_completo.setter
    def nombre_completo(self, valor: str) -> None:
        if not valor or not isinstance(valor, str) or len(valor.strip()) < 3:
            raise DatoInvalidoError(f"Nombre de cliente inválido: '{valor}'. Debe tener al menos 3 caracteres.")
        self._nombre_completo = valor.strip().title()

    @property
    def documento(self) -> str:
        return self._documento

    @documento.setter
    def documento(self, valor: str) -> None:
        if not valor or not isinstance(valor, str) or not valor.strip().isdigit() or not (6 <= len(valor.strip()) <= 12):
            raise DatoInvalidoError(f"Documento inválido: '{valor}'. Debe contener entre 6 y 12 dígitos numéricos.")
        self._documento = valor.strip()

    @property
    def correo(self) -> str:
        return self._correo

    @correo.setter
    def correo(self, valor: str) -> None:
        patron_email = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
        if not valor or not isinstance(valor, str) or not re.match(patron_email, valor.strip()):
            raise DatoInvalidoError(f"Correo electrónico con formato inválido: '{valor}'.")
        self._correo = valor.strip().lower()

    @property
    def telefono(self) -> str:
        return self._telefono

    @telefono.setter
    def telefono(self, valor: str) -> None:
        if not valor or not isinstance(valor, str) or not valor.strip().isdigit() or len(valor.strip()) != 10:
            raise DatoInvalidoError(f"Teléfono inválido: '{valor}'. Debe tener exactamente 10 dígitos.")
        self._telefono = valor.strip()

    @property
    def historial_reservas(self) -> list:
        """Retorna una copia de la lista interna para proteger la encapsulación."""
        return list(self._historial_reservas)

    def agregar_reserva_historial(self, id_reserva: str) -> None:
        """Registra el identificador de una reserva en el historial interno del cliente."""
        if not id_reserva:
            raise ParametroFaltanteError("No se puede agregar un ID de reserva vacío al historial.")
        self._historial_reservas.append(id_reserva)

    def validar_integridad(self) -> bool:
        """Verifica que todos los atributos obligatorios estén correctamente inicializados."""
        if not all([self._id_entidad, self._nombre_completo, self._documento, self._correo, self._telefono]):
            raise ParametroFaltanteError("Faltan datos obligatorios en el perfil del cliente.")
        return True

    def obtener_resumen(self) -> str:
        return (
            f"Cliente [{self.id_entidad}] | {self.nombre_completo} | "
            f"Doc: {self.documento} | Email: {self.correo} | Reservas: {len(self._historial_reservas)}"
        )

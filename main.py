"""
Archivo principal de ejecución del Sistema Integral de Gestión de Clientes,
Servicios y Reservas de la empresa Software FJ.

Simula 12 operaciones completas demostrando estabilidad, encapsulación,
polimorfismo, sobrecarga de métodos y manejo avanzado de excepciones sin bases de datos.
"""

from modelos.cliente import Cliente
from modelos.servicio import Servicio, ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from modelos.reserva import Reserva
from utilidades.excepciones import ErrorSistemaFJ
from utilidades.logger import GestorLogs


class SistemaGestionSoftwareFJ:
    """Controlador central que administra listas internas de clientes, servicios y reservas."""

    def __init__(self):
        self._clientes: list[Cliente] = []
        self._servicios: list[Servicio] = []
        self._reservas: list[Reserva] = []
        self._logger = GestorLogs()
        self._logger.registrar_info("=== INICIO DE SESIÓN DEL SISTEMA SOFTWARE FJ ===")

    def registrar_cliente(self, cliente: Cliente) -> None:
        if any(c.documento == cliente.documento for c in self._clientes):
            raise ErrorSistemaFJ(f"Ya existe un cliente registrado con el documento {cliente.documento}.", "ERR-DUP-CLI")
        self._clientes.append(cliente)
        self._logger.registrar_info(f"Cliente registrado en memoria: {cliente.obtener_resumen()}")

    def registrar_servicio(self, servicio: Servicio) -> None:
        if any(s.id_entidad == servicio.id_entidad for s in self._servicios):
            raise ErrorSistemaFJ(f"Ya existe un servicio con el ID {servicio.id_entidad}.", "ERR-DUP-SRV")
        self._servicios.append(servicio)
        self._logger.registrar_info(f"Servicio registrado en memoria: {servicio.obtener_resumen()}")

    def registrar_reserva(self, reserva: Reserva) -> None:
        self._reservas.append(reserva)
        self._logger.registrar_info(f"Reserva creada en memoria: {reserva.obtener_resumen()}")

    def mostrar_reporte_general(self) -> None:
        print("\n" + "=" * 85)
        print("REPORTE FINAL DE ESTADO EN MEMORIA - SOFTWARE FJ")
        print("=" * 85)
        print(f"\n1. CLIENTES ACTIVOS ({len(self._clientes)}):")
        for c in self._clientes:
            print(f"   - {c.obtener_resumen()}")

        print(f"\n2. CATÁLOGO DE SERVICIOS ({len(self._servicios)}):")
        for s in self._servicios:
            print(f"   - {s.obtener_resumen()}")

        print(f"\n3. HISTORIAL DE RESERVAS ({len(self._reservas)}):")
        for r in self._reservas:
            print(f"   - {r.obtener_resumen()}")
        print("=" * 85)


def ejecutar_simulacion() -> None:
    """Ejecuta 12 operaciones completas con casos exitosos y fallos controlados."""
    sistema = SistemaGestionSoftwareFJ()
    logger = GestorLogs()

    print("\n--- INICIANDO SIMULACIÓN DE 12 OPERACIONES EN SOFTWARE FJ ---\n")

    # OPERACIÓN 1: Registro válido de Cliente 1 (try / except / else)
    print("[Op 01] Registrando cliente válido (Laura Mendoza)...")
    try:
        cli_1 = Cliente("CLI-001", "Laura Valentina Mendoza", "1090456789", "laura.mendoza@correo.com", "3104567890")
    except ErrorSistemaFJ as e:
        print(f"   -> Error inesperado: {e}")
    else:
        sistema.registrar_cliente(cli_1)
        print(f"   -> ÉXITO: {cli_1.obtener_resumen()}")

    # OPERACIÓN 2: Registro válido de Cliente 2
    print("[Op 02] Registrando cliente válido (Carlos Andrés Pérez)...")
    try:
        cli_2 = Cliente("CLI-002", "Carlos Andrés Pérez", "88234567", "carlos.perez@empresa.co", "3209876543")
        sistema.registrar_cliente(cli_2)
        print(f"   -> ÉXITO: {cli_2.obtener_resumen()}")
    except ErrorSistemaFJ as e:
        print(f"   -> Error: {e}")

    # OPERACIÓN 3: Registro INVÁLIDO de Cliente
    print("[Op 03] Intentando registrar cliente con datos inválidos...")
    try:
        cli_invalido = Cliente("CLI-003", "Pedro", "12345678", "correo_sin_arroba.com", "12345")
        sistema.registrar_cliente(cli_invalido)
    except ErrorSistemaFJ as e:
        logger.registrar_error(f"Operación 3 controlada: {e}")
        print(f"   -> EXCEPCIÓN CONTROLADA: {e}")

    # OPERACIÓN 4: Creación válida de Servicio 1 (ReservaSala)
    print("[Op 04] Creando servicio especializado: Sala de Juntas Ejecutiva...")
    try:
        srv_sala = ReservaSala("SRV-01", "Sala Innovación Norte", tarifa_hora=80000, capacidad_personas=15, tiene_videobeam=True)
        sistema.registrar_servicio(srv_sala)
        print(f"   -> ÉXITO: {srv_sala.obtener_resumen()}")
    except ErrorSistemaFJ as e:
        print(f"   -> Error: {e}")

    # OPERACIÓN 5: Creación válida de Servicio 2 (AlquilerEquipo)
    print("[Op 05] Creando servicio especializado: Estación Workstation GPU...")
    try:
        srv_equipo = AlquilerEquipo("SRV-02", "Workstation Dell Precision", tarifa_hora=45000, categoria_hardware="Cómputo Alto Rendimiento", deposito_garantia=100000)
        sistema.registrar_servicio(srv_equipo)
        print(f"   -> ÉXITO: {srv_equipo.obtener_resumen()}")
    except ErrorSistemaFJ as e:
        print(f"   -> Error: {e}")

    # OPERACIÓN 6: Creación válida de Servicio 3 (AsesoriaEspecializada)
    print("[Op 06] Creando servicio especializado: Asesoría en Arquitectura Cloud...")
    try:
        srv_asesoria = AsesoriaEspecializada("SRV-03", "Auditoría Cloud AWS", tarifa_hora=120000, area_especialidad="Cloud Computing", nivel_senior=True)
        sistema.registrar_servicio(srv_asesoria)
        print(f"   -> ÉXITO: {srv_asesoria.obtener_resumen()}")
    except ErrorSistemaFJ as e:
        print(f"   -> Error: {e}")

    # OPERACIÓN 7: Creación INVÁLIDA de Servicio
    print("[Op 07] Intentando crear servicio con tarifa negativa...")
    try:
        srv_malo = ReservaSala("SRV-99", "Sala Defectuosa", tarifa_hora=-50000, capacidad_personas=1)
        sistema.registrar_servicio(srv_malo)
    except ErrorSistemaFJ as e:
        logger.registrar_error(f"Operación 7 controlada: {e}")
        print(f"   -> EXCEPCIÓN CONTROLADA: {e}")

    # OPERACIÓN 8: Reserva EXITOSA, Confirmación y Procesamiento
    print("[Op 08] Creando, confirmando y procesando reserva de Sala para Laura...")
    try:
        res_1 = Reserva("RES-101", cli_1, srv_sala, duracion_horas=4, descuento=0.10)
        sistema.registrar_reserva(res_1)
        res_1.confirmar()
        total_pagado = res_1.procesar(exento_iva=False)
        print(f"   -> ÉXITO: Reserva procesada. Total facturado con IVA y 10% dcto: ${total_pagado:,.2f}")
    except ErrorSistemaFJ as e:
        print(f"   -> Error: {e}")

    # OPERACIÓN 9: Reserva FALLIDA por incumplir horas mínimas
    print("[Op 09] Intentando reservar Workstation por 1 hora (mínimo exigido: 2h)...")
    try:
        res_invalida_horas = Reserva("RES-102", cli_2, srv_equipo, duracion_horas=1)
        sistema.registrar_reserva(res_invalida_horas)
    except ErrorSistemaFJ as e:
        logger.registrar_error(f"Operación 9 controlada: {e}")
        print(f"   -> EXCEPCIÓN CONTROLADA: {e}")

    # OPERACIÓN 10: Reserva EXITOSA de Asesoría con posterior CANCELACIÓN controlada
    print("[Op 10] Creando reserva de Asesoría para Carlos y cancelándola por cambio de agenda...")
    try:
        res_2 = Reserva("RES-103", cli_2, srv_asesoria, duracion_horas=3, descuento=0.05)
        sistema.registrar_reserva(res_2)
        res_2.confirmar()
        res_2.cancelar("El cliente solicitó reprogramar la auditoría para la próxima semana.")
        print(f"   -> ÉXITO CONTROLADO: Estado actual de RES-103 -> {res_2.estado}")
    except ErrorSistemaFJ as e:
        print(f"   -> Error: {e}")

    # OPERACIÓN 11: Operación NO PERMITIDA (procesar reserva CANCELADA)
    print("[Op 11] Intentando procesar la reserva RES-103 que ya fue cancelada...")
    try:
        res_2.procesar()
    except ErrorSistemaFJ as e:
        logger.registrar_error(f"Operación 11 controlada (Encadenada): {e} | Causa: {e.__cause__}")
        print(f"   -> EXCEPCIÓN ENCADENADA CONTROLADA: {e}")
        print(f"      Causa original capturada: {e.__cause__}")

    # OPERACIÓN 12: Intento de reservar un servicio NO DISPONIBLE (try/except/finally)
    print("[Op 12] Marcando Workstation como no disponible e intentando reservarla (try/except/finally)...")
    try:
        srv_equipo.disponible = False
        res_no_disp = Reserva("RES-104", cli_1, srv_equipo, duracion_horas=5)
        sistema.registrar_reserva(res_no_disp)
    except ErrorSistemaFJ as e:
        logger.registrar_error(f"Operación 12 controlada: {e}")
        print(f"   -> EXCEPCIÓN CONTROLADA: {e}")
    finally:
        print("   -> Bloque FINALLY ejecutado: Verificación de cierre de simulación completada sin caídas.")

    sistema.mostrar_reporte_general()
    print("\nRevise el archivo 'logs/sistema_fj.log' para auditar la traza completa de eventos y errores.\n")


if __name__ == "__main__":
    ejecutar_simulacion()

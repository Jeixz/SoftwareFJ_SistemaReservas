# Sistema Integral de Gestión de Clientes, Servicios y Reservas - Software FJ

Proyecto desarrollado para la **Fase 4 - Componente Práctico (Prácticas simuladas)** del curso **Programación (Código: 213023)** de la Universidad Nacional Abierta y a Distancia (UNAD).

**Autor:** Jeison Alexander Guerrero Miranda  
**Programa:** Ingeniería de Sistemas - ECBTI  

## Descripción de la Solución
Aplicación orientada a objetos desarrollada en Python 3 sin uso de motores de bases de datos, enfocada en la estabilidad, modularidad y tolerancia a fallos mediante manejo avanzado de excepciones y registro de auditoría en archivos planos (`logs/sistema_fj.log`).

## Principios POO Aplicados
* **Abstracción:** Clases base `EntidadSistema` y `Servicio` implementadas con el módulo `abc` (`ABC`, `@abstractmethod`).
* **Encapsulación:** Atributos privados (`_nombre`, `_documento`, `_correo`, `_estado`) protegidos mediante decoradores `@property` y setters con validación estricta.
* **Herencia y Polimorfismo:** Especialización de tres servicios (`ReservaSala`, `AlquilerEquipo`, `AsesoriaEspecializada`) que sobrescriben reglas de negocio, cálculo de tarifas y descripciones.
* **Sobrecarga de Métodos:** Implementada en `Servicio.calcular_costo()` mediante `@singledispatchmethod` para soportar llamadas directas con argumentos numéricos o paquetes de configuración por diccionario.
* **Manejo Avanzado de Excepciones:** Jerarquía personalizada (`ErrorSistemaFJ`), bloques `try/except`, `try/except/else`, `try/except/finally` y encadenamiento de excepciones (`raise ... from e`).

## Ejecución
```bash
python main.py
```

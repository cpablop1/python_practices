# Sistema de Monitoreo de Sensores en Tiempo Real

## 📋 Descripción del Proyecto

Este proyecto implementa un sistema de monitoreo concurrente que simula el funcionamiento de tres sensores industriales (temperatura, humedad y presión) en una planta de producción. El sistema utiliza programación concurrente con hilos para recopilar, analizar y alertar sobre lecturas de sensores en tiempo real.

## 🎯 Características Principales

- **Lectura Concurrente**: Tres sensores funcionando simultáneamente con diferentes períodos de lectura
- **Análisis Automático**: Verificación continua de rangos seguros para cada sensor
- **Sistema de Alertas**: Generación automática de alertas cuando los valores están fuera de rango
- **Comunicación Thread-Safe**: Uso de colas para comunicación segura entre hilos
- **Finalización Controlada**: Sistema de parada limpia de todos los hilos

## 🏗️ Arquitectura del Sistema

### Componentes Principales

1. **Clase `LecturaSensor`**: Representa una lectura individual de sensor
2. **Clase `MonitorSensores`**: Gestiona todo el sistema de monitoreo
3. **Hilos de Sensores**: Simulan la lectura periódica de sensores
4. **Hilo Analizador**: Procesa lecturas y detecta valores anómalos
5. **Hilo de Alertas**: Muestra notificaciones de alerta

### Flujo de Datos

```
Sensores → Cola de Lecturas → Analizador → Cola de Alertas → Sistema de Alertas
```

## 📊 Rangos Seguros Configurados

| Sensor | Rango Mínimo | Rango Máximo | Unidad |
|--------|--------------|--------------|--------|
| Temperatura | 18.0 | 28.0 | °C |
| Humedad | 35.0 | 65.0 | % |
| Presión | 2.0 | 3.0 | Unidades |

## 🚀 Uso del Sistema

### Ejecución Básica

```bash
python monitor_sensores.py
```

### Personalización

```python
from monitor_sensores import MonitorSensores

# Crear instancia del monitor
monitor = MonitorSensores()

# Modificar rangos seguros
monitor.rangos['temperatura'] = (20.0, 30.0)

# Iniciar sistema por 30 segundos
monitor.iniciar_sistema(duracion_segundos=30)
```

## 🧵 Hilos del Sistema

### Hilos de Sensores
- **Sensor Temperatura**: Lectura cada 0.2 segundos
- **Sensor Humedad**: Lectura cada 0.3 segundos  
- **Sensor Presión**: Lectura cada 0.4 segundos

### Hilos de Procesamiento
- **Analizador**: Procesa todas las lecturas y detecta anomalías
- **Alertas**: Muestra notificaciones de alerta al usuario

## 🔧 Configuración Técnica

### Dependencias
- Python 3.7+
- Módulos estándar: `threading`, `queue`, `time`, `random`, `datetime`, `dataclasses`

### Características de Seguridad
- **Thread-Safe**: Uso de `queue.Queue` para comunicación entre hilos
- **Manejo de Excepciones**: Captura y manejo de errores en cada hilo
- **Timeouts**: Evita bloqueos indefinidos en las colas
- **Finalización Limpia**: Parada controlada de todos los hilos

## 📈 Simulación Realista

### Valores Base
- **Temperatura**: 23°C (temperatura ambiente típica)
- **Humedad**: 50% (humedad relativa media)
- **Presión**: 2.5 unidades (presión normal del sistema)

### Variaciones Simuladas
- **Temperatura**: ±2°C de variación normal
- **Humedad**: ±5% de variación normal
- **Presión**: ±0.2 unidades de variación normal

### Valores Anómalos
- **Probabilidad**: 10% de generar valores fuera de rango
- **Propósito**: Probar el sistema de alertas

## 🎮 Ejemplo de Salida

```
============================================================
🏭 SISTEMA DE MONITOREO DE SENSORES - INICIANDO
============================================================
📊 Rangos seguros:
   temperatura: 18.0 - 28.0
   humedad: 35.0 - 65.0
   presion: 2.0 - 3.0
============================================================
[SENSOR TEMPERATURA] Iniciado - Período: 0.2s
[SENSOR HUMEDAD] Iniciado - Período: 0.3s
[SENSOR PRESION] Iniciado - Período: 0.4s
[ANALIZADOR] Iniciado
[ALERTAS] Iniciado
✅ Sistema iniciado - Monitoreando por 10 segundos...
============================================================

[SENSOR TEMPERATURA] Lectura: 24.59
[ANALIZADOR] temperatura: 24.59 - OK
[SENSOR HUMEDAD] Lectura: 54.76
[ANALIZADOR] humedad: 54.76 - OK
[SENSOR PRESION] Lectura: 2.45
[ANALIZADOR] presion: 2.45 - OK

🚨 [ALERTA] presion=8.10 (Rango: 2.0-3.0) 🚨
⏰ Tiempo: 11:13:10
--------------------------------------------------
```

## 🔍 Conceptos de Programación Concurrente

### Patrones Implementados
- **Producer-Consumer**: Sensores producen datos, analizador los consume
- **Thread Pool**: Múltiples hilos especializados
- **Message Passing**: Comunicación mediante colas thread-safe

### Ventajas del Diseño
- **Escalabilidad**: Fácil agregar nuevos sensores
- **Modularidad**: Cada componente tiene responsabilidad específica
- **Robustez**: Manejo de errores independiente por hilo
- **Eficiencia**: Procesamiento paralelo de datos

## 🛠️ Extensibilidad

### Agregar Nuevos Sensores
```python
# En el método iniciar_sistema()
hilo_nuevo_sensor = threading.Thread(
    target=self.hilo_sensor,
    args=("nuevo_sensor", 0.5),
    name="SensorNuevo"
)
```

### Modificar Rangos
```python
monitor.rangos['nuevo_sensor'] = (min_val, max_val)
```

### Personalizar Períodos
```python
# Cambiar frecuencia de lectura
hilo_temp = threading.Thread(
    target=self.hilo_sensor,
    args=("temperatura", 1.0),  # Cada 1 segundo
    name="SensorTemperatura"
)
```

## 📚 Aprendizajes del Proyecto

### Conceptos de Threading
- Creación y gestión de hilos
- Comunicación thread-safe entre hilos
- Sincronización y coordinación
- Finalización controlada de hilos

### Patrones de Diseño
- Separación de responsabilidades
- Comunicación asíncrona
- Manejo de estado compartido
- Gestión de recursos

### Buenas Prácticas
- Documentación completa con docstrings
- Manejo robusto de excepciones
- Código modular y extensible
- Logging y monitoreo

## 🎓 Casos de Uso Educativos

Este proyecto es ideal para aprender:
- **Programación Concurrente** en Python
- **Patrones de Diseño** para sistemas distribuidos
- **Simulación de Sistemas** industriales
- **Manejo de Hilos** y sincronización
- **Arquitectura de Software** modular

## 📝 Notas de Implementación

- El sistema utiliza `queue.Queue` para comunicación thread-safe
- Los hilos son marcados como `daemon` para finalización automática
- Se implementan timeouts para evitar bloqueos
- El sistema maneja interrupciones de teclado (Ctrl+C)
- La simulación incluye valores anómalos para probar alertas

## 🔮 Posibles Mejoras

- **Persistencia**: Guardar lecturas en base de datos
- **Interfaz Gráfica**: Dashboard en tiempo real
- **Configuración Externa**: Archivos de configuración
- **Métricas**: Estadísticas de rendimiento
- **Logging**: Sistema de logs más robusto
- **API REST**: Interfaz web para monitoreo remoto

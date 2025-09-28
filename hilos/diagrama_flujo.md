# Diagrama de Flujo del Sistema de Monitoreo de Sensores

## Arquitectura General del Sistema

```
┌─────────────────────────────────────────────────────────────────┐
│                    SISTEMA DE MONITOREO                        │
│                     (MonitorSensores)                          │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    INICIALIZACIÓN                               │
│  • Configurar colas (lecturas, alertas)                        │
│  • Definir rangos seguros                                      │
│  • Establecer valores base para simulación                     │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    CREACIÓN DE HILOS                           │
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │ HILO SENSOR │  │ HILO SENSOR │  │ HILO SENSOR │             │
│  │ TEMPERATURA │  │   HUMEDAD   │  │  PRESIÓN    │             │
│  │ (0.2s)      │  │ (0.3s)      │  │ (0.4s)      │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
│         │                 │                 │                 │
│         ▼                 ▼                 ▼                 │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │                COLA DE LECTURAS                           │ │
│  │              (queue.Queue)                                │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                │                               │
│                                ▼                               │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │                HILO ANALIZADOR                             │ │
│  │  • Procesa lecturas de la cola                            │ │
│  │  • Verifica rangos seguros                                │ │
│  │  • Genera alertas si es necesario                         │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                │                               │
│                                ▼                               │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │                COLA DE ALERTAS                             │ │
│  │              (queue.Queue)                                │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                │                               │
│                                ▼                               │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │                HILO DE ALERTAS                            │ │
│  │  • Recibe alertas de la cola                              │ │
│  │  • Muestra notificaciones al usuario                     │ │
│  └─────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FINALIZACIÓN                                │
│  • Desactivar sistema_activo                                  │
│  • Esperar que todos los hilos terminen                       │
│  • Liberar recursos                                           │
└─────────────────────────────────────────────────────────────────┘
```

## Flujo de Datos Detallado

### 1. Proceso de Lectura de Sensores

```
HILO SENSOR
    │
    ▼
┌─────────────────┐
│ Leer Sensor     │ ◄─── Simular valor con variaciones
│ (leer_sensor)   │
└─────────────────┘
    │
    ▼
┌─────────────────┐
│ Crear Lectura   │ ◄─── LecturaSensor(sensor, valor, tiempo)
│ (LecturaSensor) │
└─────────────────┘
    │
    ▼
┌─────────────────┐
│ Enviar a Cola   │ ◄─── cola_lecturas.put(lectura)
│ (cola_lecturas) │
└─────────────────┘
    │
    ▼
┌─────────────────┐
│ Esperar Período │ ◄─── time.sleep(periodo)
│ (time.sleep)    │
└─────────────────┘
    │
    └───────────────┐
                   │
                   ▼
            [Repetir mientras sistema_activo]
```

### 2. Proceso de Análisis

```
HILO ANALIZADOR
    │
    ▼
┌─────────────────┐
│ Obtener Lectura │ ◄─── cola_lecturas.get(timeout=1.0)
│ (cola_lecturas) │
└─────────────────┘
    │
    ▼
┌─────────────────┐
│ Obtener Rangos  │ ◄─── rangos[sensor] = (min, max)
│ (rangos)        │
└─────────────────┘
    │
    ▼
┌─────────────────┐
│ ¿Valor en Rango?│
│ (verificación)  │
└─────────────────┘
    │
    ├─ SÍ ──────────────┐
    │                   ▼
    │            ┌─────────────────┐
    │            │ Mostrar "OK"    │
    │            │ (print)         │
    │            └─────────────────┘
    │
    └─ NO ──────────────┐
                        ▼
                ┌─────────────────┐
                │ Generar Alerta  │ ◄─── Crear mensaje de alerta
                │ (alerta)        │
                └─────────────────┘
                        │
                        ▼
                ┌─────────────────┐
                │ Enviar a Cola   │ ◄─── cola_alertas.put(alerta)
                │ (cola_alertas)  │
                └─────────────────┘
                        │
                        ▼
                ┌─────────────────┐
                │ Marcar Completado│ ◄─── cola_lecturas.task_done()
                │ (task_done)     │
                └─────────────────┘
```

### 3. Proceso de Alertas

```
HILO ALERTAS
    │
    ▼
┌─────────────────┐
│ Obtener Alerta  │ ◄─── cola_alertas.get(timeout=1.0)
│ (cola_alertas)  │
└─────────────────┘
    │
    ▼
┌─────────────────┐
│ Formatear Alerta│ ◄─── Agregar emojis y timestamp
│ (formato)       │
└─────────────────┘
    │
    ▼
┌─────────────────┐
│ Mostrar Alerta  │ ◄─── print() con formato especial
│ (print)         │
└─────────────────┘
    │
    ▼
┌─────────────────┐
│ Marcar Completado│ ◄─── cola_alertas.task_done()
│ (task_done)     │
└─────────────────┘
```

## Estados del Sistema

### Estado Inicial
```
sistema_activo = True
cola_lecturas = Queue()
cola_alertas = Queue()
hilos = []
```

### Estado Ejecutándose
```
sistema_activo = True
├─ Hilos de Sensores: Generando lecturas
├─ Hilo Analizador: Procesando lecturas
└─ Hilo Alertas: Mostrando alertas
```

### Estado Finalizando
```
sistema_activo = False
├─ Hilos de Sensores: Saliendo de bucles
├─ Hilo Analizador: Saliendo de bucles
└─ Hilo Alertas: Saliendo de bucles
```

### Estado Finalizado
```
sistema_activo = False
├─ Todos los hilos terminados
├─ Colas vacías
└─ Recursos liberados
```

## Comunicación Entre Hilos

### Patrón Producer-Consumer

```
PRODUCERS (Sensores)     CONSUMERS (Analizador)
        │                        │
        ▼                        ▼
┌─────────────┐         ┌─────────────┐
│ Generar     │────────▶│ Procesar    │
│ Lecturas    │         │ Lecturas    │
└─────────────┘         └─────────────┘
        │                        │
        ▼                        ▼
┌─────────────┐         ┌─────────────┐
│ Enviar a    │         │ Generar     │
│ Cola        │         │ Alertas    │
└─────────────┘         └─────────────┘
```

### Sincronización

```
HILO SENSOR ──┐
              │
              ▼
    ┌─────────────────┐
    │ Cola de Lecturas│ ◄─── Thread-Safe
    │ (queue.Queue)   │
    └─────────────────┘
              │
              ▼
    ┌─────────────────┐
    │ HILO ANALIZADOR │
    └─────────────────┘
              │
              ▼
    ┌─────────────────┐
    │ Cola de Alertas │ ◄─── Thread-Safe
    │ (queue.Queue)   │
    └─────────────────┘
              │
              ▼
    ┌─────────────────┐
    │ HILO ALERTAS    │
    └─────────────────┘
```

## Manejo de Errores

### Timeouts en Colas
```
cola.get(timeout=1.0)
    │
    ├─ Éxito ──────────┐
    │                  ▼
    │            ┌─────────────┐
    │            │ Procesar    │
    │            │ Datos       │
    │            └─────────────┘
    │
    └─ Timeout ─────────┐
                        ▼
                ┌─────────────┐
                │ Continuar   │ ◄─── Verificar sistema_activo
                │ Bucle       │
                └─────────────┘
```

### Excepciones
```
try:
    # Operación del hilo
except queue.Empty:
    # Timeout - continuar
except Exception as e:
    # Error crítico - salir del hilo
```

## Configuración de Rangos

### Rangos por Defecto
```
temperatura: (18.0, 28.0)  # °C
humedad:    (35.0, 65.0)  # %
presion:    (2.0, 3.0)     # unidades
```

### Verificación de Rangos
```
valor < limite_inferior OR valor > limite_superior
    │
    ├─ True ──────────┐
    │                 ▼
    │          ┌─────────────┐
    │          │ Generar     │
    │          │ Alerta      │
    │          └─────────────┘
    │
    └─ False ─────────┐
                      ▼
              ┌─────────────┐
              │ Valor OK    │
              │ (continuar) │
              └─────────────┘
```

Este diagrama muestra la arquitectura completa del sistema de monitoreo, incluyendo el flujo de datos, la comunicación entre hilos, y los diferentes estados del sistema.

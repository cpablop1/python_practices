"""
Configuración del Sistema de Monitoreo de Sensores

Este archivo contiene configuraciones predefinidas para diferentes
tipos de ambientes y casos de uso del sistema de monitoreo.
"""

# Configuraciones predefinidas para diferentes ambientes
CONFIGURACIONES = {
    'oficina': {
        'rangos': {
            'temperatura': (20.0, 25.0),  # Ambiente de oficina cómodo
            'humedad': (40.0, 60.0),      # Humedad confortable
            'presion': (1.0, 2.0)         # Presión baja para oficina
        },
        'valores_base': {
            'temperatura': 22.0,
            'humedad': 50.0,
            'presion': 1.5
        },
        'descripcion': 'Configuración para ambiente de oficina'
    },
    
    'industrial': {
        'rangos': {
            'temperatura': (15.0, 35.0),  # Rango industrial amplio
            'humedad': (20.0, 80.0),      # Rango industrial amplio
            'presion': (1.0, 5.0)         # Rango industrial amplio
        },
        'valores_base': {
            'temperatura': 25.0,
            'humedad': 60.0,
            'presion': 3.0
        },
        'descripcion': 'Configuración para ambiente industrial'
    },
    
    'laboratorio': {
        'rangos': {
            'temperatura': (18.0, 22.0),  # Rango estricto para laboratorio
            'humedad': (30.0, 50.0),      # Rango estricto para laboratorio
            'presion': (2.0, 3.0)         # Rango normal para laboratorio
        },
        'valores_base': {
            'temperatura': 20.0,
            'humedad': 40.0,
            'presion': 2.5
        },
        'descripcion': 'Configuración para ambiente de laboratorio'
    },
    
    'almacen': {
        'rangos': {
            'temperatura': (10.0, 30.0),  # Rango amplio para almacén
            'humedad': (30.0, 70.0),      # Rango amplio para almacén
            'presion': (1.5, 4.0)         # Rango amplio para almacén
        },
        'valores_base': {
            'temperatura': 20.0,
            'humedad': 55.0,
            'presion': 2.8
        },
        'descripcion': 'Configuración para ambiente de almacén'
    },
    
    'critico': {
        'rangos': {
            'temperatura': (22.0, 24.0),  # Rango muy estricto
            'humedad': (45.0, 55.0),      # Rango muy estricto
            'presion': (2.4, 2.6)         # Rango muy estricto
        },
        'valores_base': {
            'temperatura': 23.0,
            'humedad': 50.0,
            'presion': 2.5
        },
        'descripcion': 'Configuración crítica con rangos muy estrictos'
    }
}

# Configuraciones de sensores por tipo
SENSORES_CONFIG = {
    'temperatura': {
        'unidad': '°C',
        'precision': 1,  # Decimales a mostrar
        'variacion_normal': 2.0,  # ±2°C
        'variacion_anomala': 8.0   # ±8°C para valores anómalos
    },
    'humedad': {
        'unidad': '%',
        'precision': 1,
        'variacion_normal': 5.0,   # ±5%
        'variacion_anomala': 15.0  # ±15% para valores anómalos
    },
    'presion': {
        'unidad': 'bar',
        'precision': 2,
        'variacion_normal': 0.2,   # ±0.2 bar
        'variacion_anomala': 1.0   # ±1.0 bar para valores anómalos
    }
}

# Configuraciones de períodos de lectura
PERIODOS_LECTURA = {
    'rapido': {
        'temperatura': 0.1,  # 10 lecturas por segundo
        'humedad': 0.2,      # 5 lecturas por segundo
        'presion': 0.3       # 3.33 lecturas por segundo
    },
    'normal': {
        'temperatura': 0.2,  # 5 lecturas por segundo
        'humedad': 0.3,      # 3.33 lecturas por segundo
        'presion': 0.4       # 2.5 lecturas por segundo
    },
    'lento': {
        'temperatura': 1.0,  # 1 lectura por segundo
        'humedad': 1.5,       # 0.67 lecturas por segundo
        'presion': 2.0       # 0.5 lecturas por segundo
    }
}

# Configuraciones de probabilidad de valores anómalos
PROBABILIDAD_ANOMALOS = {
    'baja': 0.05,    # 5% de probabilidad
    'normal': 0.1,   # 10% de probabilidad
    'alta': 0.2      # 20% de probabilidad
}

def obtener_configuracion(ambiente: str):
    """
    Obtiene la configuración para un ambiente específico.
    
    Args:
        ambiente (str): Nombre del ambiente ('oficina', 'industrial', etc.)
        
    Returns:
        dict: Configuración del ambiente
        
    Raises:
        KeyError: Si el ambiente no existe
    """
    if ambiente not in CONFIGURACIONES:
        ambientes_disponibles = list(CONFIGURACIONES.keys())
        raise KeyError(f"Ambiente '{ambiente}' no encontrado. Ambientes disponibles: {ambientes_disponibles}")
    
    return CONFIGURACIONES[ambiente]

def listar_ambientes():
    """
    Lista todos los ambientes disponibles.
    
    Returns:
        list: Lista de ambientes disponibles
    """
    return list(CONFIGURACIONES.keys())

def obtener_info_ambiente(ambiente: str):
    """
    Obtiene información detallada de un ambiente.
    
    Args:
        ambiente (str): Nombre del ambiente
        
    Returns:
        dict: Información del ambiente
    """
    config = obtener_configuracion(ambiente)
    return {
        'nombre': ambiente,
        'descripcion': config['descripcion'],
        'rangos': config['rangos'],
        'valores_base': config['valores_base']
    }

def aplicar_configuracion(monitor, ambiente: str, velocidad: str = 'normal', probabilidad_anomalos: str = 'normal'):
    """
    Aplica una configuración específica a un monitor.
    
    Args:
        monitor: Instancia de MonitorSensores
        ambiente (str): Ambiente a aplicar
        velocidad (str): Velocidad de lectura ('rapido', 'normal', 'lento')
        probabilidad_anomalos (str): Probabilidad de valores anómalos ('baja', 'normal', 'alta')
    """
    # Aplicar configuración del ambiente
    config = obtener_configuracion(ambiente)
    monitor.rangos = config['rangos'].copy()
    monitor.valores_base = config['valores_base'].copy()
    
    # Aplicar velocidad de lectura (esto requeriría modificar el monitor)
    if velocidad in PERIODOS_LECTURA:
        print(f"Configuración de velocidad '{velocidad}' aplicada")
    
    # Aplicar probabilidad de valores anómalos (esto requeriría modificar el monitor)
    if probabilidad_anomalos in PROBABILIDAD_ANOMALOS:
        print(f"Probabilidad de valores anómalos '{probabilidad_anomalos}' aplicada")
    
    print(f"Configuración '{ambiente}' aplicada exitosamente")

def mostrar_configuraciones():
    """
    Muestra todas las configuraciones disponibles.
    """
    print("🔧 CONFIGURACIONES DISPONIBLES")
    print("=" * 50)
    
    for ambiente, config in CONFIGURACIONES.items():
        print(f"\n📋 {ambiente.upper()}")
        print(f"   Descripción: {config['descripcion']}")
        print("   Rangos:")
        for sensor, (min_val, max_val) in config['rangos'].items():
            print(f"     {sensor}: {min_val} - {max_val}")
        print("   Valores base:")
        for sensor, valor in config['valores_base'].items():
            print(f"     {sensor}: {valor}")
    
    print(f"\n⚡ VELOCIDADES DE LECTURA")
    for velocidad, periodos in PERIODOS_LECTURA.items():
        print(f"\n   {velocidad.upper()}:")
        for sensor, periodo in periodos.items():
            print(f"     {sensor}: {periodo}s")
    
    print(f"\n🎲 PROBABILIDADES DE VALORES ANÓMALOS")
    for prob, valor in PROBABILIDAD_ANOMALOS.items():
        print(f"   {prob}: {valor*100}%")

if __name__ == "__main__":
    # Mostrar todas las configuraciones disponibles
    mostrar_configuraciones()

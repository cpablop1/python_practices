"""
Ejemplos de Uso del Sistema de Monitoreo de Sensores

Este archivo contiene ejemplos prácticos de cómo usar el sistema de monitoreo
de sensores, incluyendo configuraciones personalizadas y casos de uso avanzados.
"""

from monitor_sensores import MonitorSensores
import time

def ejemplo_basico():
    """
    Ejemplo básico de uso del sistema de monitoreo.
    """
    print("=== EJEMPLO BÁSICO ===")
    
    # Crear instancia del monitor
    monitor = MonitorSensores()
    
    # Ejecutar por 5 segundos
    monitor.iniciar_sistema(duracion_segundos=5)

def ejemplo_personalizado():
    """
    Ejemplo con configuración personalizada de rangos.
    """
    print("\n=== EJEMPLO PERSONALIZADO ===")
    
    # Crear monitor
    monitor = MonitorSensores()
    
    # Modificar rangos seguros para ser más estrictos
    monitor.rangos['temperatura'] = (20.0, 25.0)  # Rango más estricto
    monitor.rangos['humedad'] = (40.0, 60.0)      # Rango más estricto
    monitor.rangos['presion'] = (2.2, 2.8)        # Rango más estricto
    
    print("Rangos personalizados:")
    for sensor, (min_val, max_val) in monitor.rangos.items():
        print(f"  {sensor}: {min_val} - {max_val}")
    
    # Ejecutar por 8 segundos
    monitor.iniciar_sistema(duracion_segundos=8)

def ejemplo_valores_base_personalizados():
    """
    Ejemplo con valores base personalizados para la simulación.
    """
    print("\n=== EJEMPLO CON VALORES BASE PERSONALIZADOS ===")
    
    # Crear monitor
    monitor = MonitorSensores()
    
    # Modificar valores base para simular condiciones específicas
    monitor.valores_base['temperatura'] = 15.0  # Ambiente frío
    monitor.valores_base['humedad'] = 80.0      # Ambiente húmedo
    monitor.valores_base['presion'] = 1.5       # Presión baja
    
    print("Valores base personalizados:")
    for sensor, valor in monitor.valores_base.items():
        print(f"  {sensor}: {valor}")
    
    # Ejecutar por 6 segundos
    monitor.iniciar_sistema(duracion_segundos=6)

def ejemplo_monitoreo_extendido():
    """
    Ejemplo de monitoreo extendido con múltiples ejecuciones.
    """
    print("\n=== EJEMPLO DE MONITOREO EXTENDIDO ===")
    
    monitor = MonitorSensores()
    
    # Primera fase: Monitoreo normal
    print("Fase 1: Monitoreo normal (5 segundos)")
    monitor.iniciar_sistema(duracion_segundos=5)
    
    # Segunda fase: Rangos más estrictos
    print("\nFase 2: Rangos estrictos (5 segundos)")
    monitor.rangos['temperatura'] = (22.0, 24.0)
    monitor.rangos['humedad'] = (45.0, 55.0)
    monitor.rangos['presion'] = (2.4, 2.6)
    
    monitor.iniciar_sistema(duracion_segundos=5)

def ejemplo_manejo_errores():
    """
    Ejemplo que demuestra el manejo de errores del sistema.
    """
    print("\n=== EJEMPLO DE MANEJO DE ERRORES ===")
    
    try:
        monitor = MonitorSensores()
        
        # Simular interrupción después de 3 segundos
        import threading
        
        def interrumpir():
            time.sleep(3)
            print("\n⚠️  Simulando interrupción del sistema...")
            monitor.finalizar_sistema()
        
        # Crear hilo para interrumpir
        hilo_interrupcion = threading.Thread(target=interrumpir)
        hilo_interrupcion.daemon = True
        hilo_interrupcion.start()
        
        # Iniciar sistema
        monitor.iniciar_sistema(duracion_segundos=10)
        
    except KeyboardInterrupt:
        print("\n⚠️  Interrupción del usuario detectada")
    except Exception as e:
        print(f"\n❌ Error en el sistema: {e}")

def ejemplo_estadisticas():
    """
    Ejemplo que muestra cómo se podrían agregar estadísticas al sistema.
    """
    print("\n=== EJEMPLO CON ESTADÍSTICAS ===")
    
    monitor = MonitorSensores()
    
    # Variables para estadísticas
    lecturas_totales = 0
    alertas_generadas = 0
    
    # Función personalizada para mostrar estadísticas
    def mostrar_estadisticas():
        print(f"\n📊 ESTADÍSTICAS:")
        print(f"   Lecturas procesadas: {lecturas_totales}")
        print(f"   Alertas generadas: {alertas_generadas}")
        if lecturas_totales > 0:
            porcentaje_alertas = (alertas_generadas / lecturas_totales) * 100
            print(f"   Porcentaje de alertas: {porcentaje_alertas:.1f}%")
    
    # Ejecutar sistema
    monitor.iniciar_sistema(duracion_segundos=7)
    
    # Mostrar estadísticas finales
    mostrar_estadisticas()

def ejemplo_configuracion_avanzada():
    """
    Ejemplo de configuración avanzada del sistema.
    """
    print("\n=== EJEMPLO DE CONFIGURACIÓN AVANZADA ===")
    
    monitor = MonitorSensores()
    
    # Configuración para ambiente industrial
    print("Configurando para ambiente industrial...")
    
    # Rangos industriales típicos
    monitor.rangos = {
        'temperatura': (15.0, 35.0),  # Rango industrial amplio
        'humedad': (20.0, 80.0),      # Rango industrial amplio
        'presion': (1.0, 5.0)         # Rango industrial amplio
    }
    
    # Valores base para ambiente industrial
    monitor.valores_base = {
        'temperatura': 25.0,  # Temperatura industrial típica
        'humedad': 60.0,      # Humedad industrial típica
        'presion': 3.0        # Presión industrial típica
    }
    
    print("Configuración industrial aplicada:")
    print("Rangos:")
    for sensor, (min_val, max_val) in monitor.rangos.items():
        print(f"  {sensor}: {min_val} - {max_val}")
    
    print("Valores base:")
    for sensor, valor in monitor.valores_base.items():
        print(f"  {sensor}: {valor}")
    
    # Ejecutar monitoreo industrial
    monitor.iniciar_sistema(duracion_segundos=10)

def main():
    """
    Función principal que ejecuta todos los ejemplos.
    """
    print("🔧 EJEMPLOS DE USO DEL SISTEMA DE MONITOREO DE SENSORES")
    print("=" * 60)
    
    try:
        # Ejecutar ejemplos
        ejemplo_basico()
        ejemplo_personalizado()
        ejemplo_valores_base_personalizados()
        ejemplo_monitoreo_extendido()
        ejemplo_manejo_errores()
        ejemplo_estadisticas()
        ejemplo_configuracion_avanzada()
        
        print("\n✅ Todos los ejemplos completados exitosamente")
        
    except KeyboardInterrupt:
        print("\n⚠️  Ejecución interrumpida por el usuario")
    except Exception as e:
        print(f"\n❌ Error durante la ejecución de ejemplos: {e}")

if __name__ == "__main__":
    main()

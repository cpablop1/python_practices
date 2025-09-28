"""
Sistema de Monitoreo de Sensores en Tiempo Real

Este módulo implementa un sistema de monitoreo concurrente que simula el funcionamiento
de tres sensores (temperatura, humedad y presión) en una planta de producción.

Características principales:
- Lectura concurrente de múltiples sensores
- Análisis automático de rangos seguros
- Generación de alertas en tiempo real
- Comunicación entre hilos mediante colas

Autor: Sistema de Monitoreo Industrial
Versión: 1.0
"""

import threading
import queue
import time
import random
from datetime import datetime
from dataclasses import dataclass
from typing import Dict, Tuple

@dataclass
class LecturaSensor:
    """
    Clase para representar una lectura de sensor.
    
    Atributos:
        sensor (str): Nombre del sensor que generó la lectura
        valor (float): Valor numérico de la lectura
        tiempo (datetime): Timestamp de cuando se tomó la lectura
    """
    sensor: str
    valor: float
    tiempo: datetime

class MonitorSensores:
    """
    Clase principal que gestiona el sistema de monitoreo de sensores.
    
    Esta clase coordina múltiples hilos para simular el funcionamiento de sensores
    industriales, analizar sus lecturas y generar alertas cuando los valores están
    fuera de los rangos seguros.
    
    Atributos:
        cola_lecturas (queue.Queue): Cola thread-safe para almacenar lecturas de sensores
        cola_alertas (queue.Queue): Cola thread-safe para almacenar alertas generadas
        rangos (Dict[str, Tuple[float, float]]): Rangos seguros para cada tipo de sensor
        sistema_activo (bool): Flag para controlar el estado del sistema
        hilos (List[threading.Thread]): Lista de hilos activos del sistema
        valores_base (Dict[str, float]): Valores base para simulación realista
    """
    
    def __init__(self):
        """
        Inicializa el sistema de monitoreo con configuraciones por defecto.
        
        Configura las colas de comunicación, define los rangos seguros para cada
        sensor y establece los valores base para la simulación.
        """
        # Colas thread-safe para comunicación entre hilos
        self.cola_lecturas = queue.Queue()
        self.cola_alertas = queue.Queue()
        
        # Rangos seguros para cada sensor (mínimo, máximo)
        self.rangos = {
            'temperatura': (18.0, 28.0),  # Grados Celsius
            'humedad': (35.0, 65.0),      # Porcentaje
            'presion': (2.0, 3.0)         # Unidades de presión
        }
        
        # Control del sistema - permite detener todos los hilos
        self.sistema_activo = True
        self.hilos = []
        
        # Valores base para simulación realista de cada sensor
        self.valores_base = {
            'temperatura': 23.0,  # Temperatura ambiente típica
            'humedad': 50.0,      # Humedad relativa media
            'presion': 2.5        # Presión normal del sistema
        }

    def leer_sensor(self, nombre_sensor: str) -> float:
        """
        Simula la lectura de un sensor con variaciones realistas.
        
        Este método simula el comportamiento de sensores reales generando valores
        que varían alrededor de un valor base, con ocasionalmente valores fuera
        de rango para probar el sistema de alertas.
        
        Args:
            nombre_sensor (str): Nombre del sensor a simular
            
        Returns:
            float: Valor simulado del sensor
            
        Raises:
            KeyError: Si el nombre del sensor no existe en valores_base
        """
        valor_base = self.valores_base[nombre_sensor]
        
        # Simular variaciones realistas según el tipo de sensor
        if nombre_sensor == 'temperatura':
            variacion = random.uniform(-2.0, 2.0)  # ±2°C de variación
        elif nombre_sensor == 'humedad':
            variacion = random.uniform(-5.0, 5.0)  # ±5% de variación
        else:  # presion
            variacion = random.uniform(-0.2, 0.2)  # ±0.2 unidades de variación
        
        # Ocasionalmente generar valores fuera de rango para probar alertas
        # Esto simula fallos o condiciones anómalas en sensores reales
        if random.random() < 0.1:  # 10% de probabilidad de valor anómalo
            if random.random() < 0.5:  # 50% probabilidad de valor bajo vs alto
                # Valor muy bajo (simula fallo de sensor o condición extrema)
                return valor_base - random.uniform(5.0, 10.0)
            else:
                # Valor muy alto (simula sobrecarga o mal funcionamiento)
                return valor_base + random.uniform(5.0, 10.0)
        
        # Retornar valor normal con variación
        return valor_base + variacion

    def hilo_sensor(self, nombre: str, periodo: float):
        """
        Hilo que simula un sensor enviando datos periódicamente.
        
        Este método se ejecuta en un hilo separado y simula el comportamiento
        de un sensor real que toma lecturas a intervalos regulares.
        
        Args:
            nombre (str): Nombre del sensor (temperatura, humedad, presion)
            periodo (float): Intervalo en segundos entre lecturas
        """
        print(f"[SENSOR {nombre.upper()}] Iniciado - Período: {periodo}s")
        
        while self.sistema_activo:  # Bucle principal del hilo sensor
            try:
                # Simular lectura del sensor con variaciones realistas
                valor = self.leer_sensor(nombre)
                
                # Crear objeto de lectura con timestamp para trazabilidad
                lectura = LecturaSensor(
                    sensor=nombre,
                    valor=valor,
                    tiempo=datetime.now()  # Timestamp preciso de la lectura
                )
                
                # Enviar lectura a la cola thread-safe para procesamiento posterior
                self.cola_lecturas.put(lectura)
                print(f"[SENSOR {nombre.upper()}] Lectura: {valor:.2f}")
                
                # Esperar el período especificado antes de la siguiente lectura
                # Esto simula el comportamiento real de sensores que no pueden leer continuamente
                time.sleep(periodo)
                
            except Exception as e:
                # Manejo de errores específico del hilo sensor
                print(f"[ERROR SENSOR {nombre}] {e}")
                break  # Salir del bucle en caso de error crítico

    def hilo_analizador(self):
        """
        Hilo que analiza las lecturas y genera alertas si es necesario.
        
        Este hilo procesa continuamente las lecturas de sensores desde la cola,
        verifica si están dentro de los rangos seguros y genera alertas cuando
        detecta valores anómalos.
        """
        print("[ANALIZADOR] Iniciado")
        
        while self.sistema_activo:  # Bucle principal del analizador
            try:
                # Obtener lectura de la cola con timeout para evitar bloqueo indefinido
                # El timeout permite que el hilo salga cuando sistema_activo = False
                lectura = self.cola_lecturas.get(timeout=1.0)
                
                # Obtener rangos seguros para este tipo de sensor desde la configuración
                limite_inferior, limite_superior = self.rangos[lectura.sensor]
                
                # Verificar si el valor está fuera del rango seguro definido
                if lectura.valor < limite_inferior or lectura.valor > limite_superior:
                    # Generar alerta para valor fuera de rango con información detallada
                    alerta = f"[ALERTA] {lectura.sensor}={lectura.valor:.2f} (Rango: {limite_inferior}-{limite_superior})"
                    self.cola_alertas.put(alerta)  # Enviar alerta a la cola de alertas
                    print(f"[ANALIZADOR] {alerta}")
                else:
                    # Valor dentro del rango seguro - operación normal
                    print(f"[ANALIZADOR] {lectura.sensor}: {lectura.valor:.2f} - OK")
                
                # Marcar tarea como completada en la cola para liberar recursos
                self.cola_lecturas.task_done()
                
            except queue.Empty:
                # Timeout en la cola - continuar el bucle (permite salir cuando sistema_activo = False)
                # Esto es normal y permite que el hilo responda a la señal de parada
                continue
            except Exception as e:
                # Manejo de errores específico del analizador
                print(f"[ERROR ANALIZADOR] {e}")
                break  # Salir del bucle en caso de error crítico

    def hilo_alertas(self):
        """
        Hilo que procesa y muestra las alertas del sistema.
        
        Este hilo recibe alertas desde la cola de alertas y las presenta
        al usuario con formato visual llamativo para llamar la atención
        sobre condiciones anómalas en el sistema.
        """
        print("[ALERTAS] Iniciado")
        
        while self.sistema_activo:  # Bucle principal del hilo de alertas
            try:
                # Obtener alerta de la cola con timeout para evitar bloqueo indefinido
                # El timeout permite que el hilo salga cuando sistema_activo = False
                alerta = self.cola_alertas.get(timeout=1.0)
                
                # Mostrar alerta con formato especial y emojis para llamar la atención
                # El formato visual ayuda a identificar rápidamente las alertas críticas
                print(f"\n🚨 {alerta} 🚨")
                print(f"⏰ Tiempo: {datetime.now().strftime('%H:%M:%S')}")
                print("-" * 50)
                
                # Marcar tarea como completada en la cola para liberar recursos
                self.cola_alertas.task_done()
                
            except queue.Empty:
                # Timeout en la cola - continuar el bucle (permite salir cuando sistema_activo = False)
                # Esto es normal y permite que el hilo responda a la señal de parada
                continue
            except Exception as e:
                # Manejo de errores específico del hilo de alertas
                print(f"[ERROR ALERTAS] {e}")
                break  # Salir del bucle en caso de error crítico

    def iniciar_sistema(self, duracion_segundos: int = 10):
        """
        Inicia el sistema de monitoreo con todos los hilos necesarios.
        
        Este método crea e inicia todos los hilos del sistema:
        - 3 hilos de sensores (temperatura, humedad, presión)
        - 1 hilo analizador
        - 1 hilo de alertas
        
        Args:
            duracion_segundos (int): Duración en segundos que funcionará el sistema
        """
        print("=" * 60)
        print("🏭 SISTEMA DE MONITOREO DE SENSORES - INICIANDO")
        print("=" * 60)
        print(f"📊 Rangos seguros:")
        for sensor, (min_val, max_val) in self.rangos.items():
            print(f"   {sensor}: {min_val} - {max_val}")
        print("=" * 60)
        
        # Crear hilos para cada sensor con diferentes períodos de lectura
        hilo_temp = threading.Thread(
            target=self.hilo_sensor, 
            args=("temperatura", 0.2),  # Lectura cada 0.2 segundos
            name="SensorTemperatura"
        )
        
        hilo_humedad = threading.Thread(
            target=self.hilo_sensor, 
            args=("humedad", 0.3),      # Lectura cada 0.3 segundos
            name="SensorHumedad"
        )
        
        hilo_presion = threading.Thread(
            target=self.hilo_sensor, 
            args=("presion", 0.4),      # Lectura cada 0.4 segundos
            name="SensorPresion"
        )
        
        # Crear hilo analizador que procesa todas las lecturas
        hilo_analizador = threading.Thread(
            target=self.hilo_analizador,
            name="Analizador"
        )
        
        # Crear hilo de alertas que muestra las notificaciones
        hilo_alertas = threading.Thread(
            target=self.hilo_alertas,
            name="Alertas"
        )
        
        # Guardar referencias a todos los hilos para control posterior
        self.hilos = [hilo_temp, hilo_humedad, hilo_presion, hilo_analizador, hilo_alertas]
        
        # Iniciar todos los hilos de forma secuencial
        for hilo in self.hilos:
            hilo.daemon = True  # Los hilos se cerrarán automáticamente cuando termine el programa principal
            hilo.start()  # Iniciar el hilo (no bloquea la ejecución)
        
        print(f"✅ Sistema iniciado - Monitoreando por {duracion_segundos} segundos...")
        print("=" * 60)
        
        # Esperar el tiempo especificado antes de finalizar
        time.sleep(duracion_segundos)
        
        # Finalizar sistema de forma controlada
        self.finalizar_sistema()

    def finalizar_sistema(self):
        """
        Finaliza el sistema de monitoreo de forma controlada.
        
        Este método detiene todos los hilos del sistema de manera segura,
        esperando a que terminen sus operaciones antes de cerrar el programa.
        """
        print("\n" + "=" * 60)
        print("🛑 FINALIZANDO SISTEMA DE MONITOREO")
        print("=" * 60)
        
        # Desactivar el sistema para que todos los hilos salgan de sus bucles
        # Esta es la señal de parada que todos los hilos monitorean
        self.sistema_activo = False
        
        # Esperar a que todos los hilos terminen de forma controlada
        # El join() asegura que los hilos terminen antes de continuar
        for hilo in self.hilos:
            if hilo.is_alive():  # Solo esperar hilos que aún están ejecutándose
                hilo.join(timeout=2.0)  # Esperar máximo 2 segundos por hilo
        
        print("✅ Sistema finalizado correctamente")
        print("=" * 60)

def main():
    """
    Función principal del sistema de monitoreo.
    
    Esta función crea una instancia del monitor y maneja las excepciones
    para asegurar una finalización limpia del sistema.
    """
    monitor = MonitorSensores()
    
    try:
        # Iniciar el sistema por 10 segundos por defecto
        monitor.iniciar_sistema(duracion_segundos=10)
    except KeyboardInterrupt:
        print("\n⚠️  Interrupción del usuario - Finalizando sistema...")
        monitor.finalizar_sistema()
    except Exception as e:
        print(f"\n❌ Error en el sistema: {e}")
        monitor.finalizar_sistema()

if __name__ == "__main__":
    main()

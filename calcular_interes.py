"""
Herramienta para calcular interés de cuenta de plaza fija
Refactorizada para mejor mantenibilidad y reutilización
"""

from typing import Optional
import sys


class CalculadoraInteres:
    """Clase para calcular intereses de cuentas de plaza fija con impuestos."""
    
    def __init__(self, isr: float = 0.10):
        """
        Inicializa la calculadora con la tasa de ISR.
        
        Args:
            isr: Tasa de impuesto sobre la renta (por defecto 10%)
        """
        self.isr = isr
    
    def obtener_monto_inicial(self) -> float:
        """Obtiene y valida el monto inicial del usuario."""
        while True:
            try:
                print('\nIngrese el monto inicial:')
                monto = float(input())
                if monto <= 0:
                    print("Error: El monto debe ser mayor a 0. Intente nuevamente.")
                    continue
                return monto
            except ValueError:
                print("Error: Ingrese un número válido. Intente nuevamente.")
    
    def obtener_tasa_interes(self) -> float:
        """Obtiene y valida la tasa de interés del usuario."""
        while True:
            try:
                print('Ingrese la tasa de interés, por ejemplo (0.07, 0.06, 0.05):')
                tasa = float(input())
                if tasa < 0 or tasa > 1:
                    print("Error: La tasa debe estar entre 0 y 1 (0% a 100%). Intente nuevamente.")
                    continue
                return tasa
            except ValueError:
                print("Error: Ingrese un número válido. Intente nuevamente.")
    
    def obtener_dias_plazo(self) -> int:
        """Obtiene y valida los días de plazo del usuario."""
        while True:
            try:
                print('Ingrese la cantidad de días del plazo, por ejemplo (90, 180, 360):')
                dias = int(input())
                if dias <= 0:
                    print("Error: Los días deben ser mayor a 0. Intente nuevamente.")
                    continue
                return dias
            except ValueError:
                print("Error: Ingrese un número entero válido. Intente nuevamente.")
    
    def calcular_interes_bruto(self, monto_inicial: float, tasa_interes: float, dias_plazo: int) -> float:
        """
        Calcula el interés bruto antes de impuestos.
        
        Args:
            monto_inicial: Monto inicial de la inversión
            tasa_interes: Tasa de interés anual
            dias_plazo: Días del plazo de la inversión
            
        Returns:
            Interés bruto calculado
        """
        return monto_inicial * tasa_interes * (dias_plazo / 365)
    
    def calcular_interes_neto(self, interes_bruto: float) -> float:
        """
        Calcula el interés neto después de aplicar el ISR.
        
        Args:
            interes_bruto: Interés bruto antes de impuestos
            
        Returns:
            Interés neto después de impuestos
        """
        return interes_bruto - (interes_bruto * self.isr)
    
    def calcular_interes_completo(self, monto_inicial: float, tasa_interes: float, dias_plazo: int) -> tuple[float, float]:
        """
        Calcula tanto el interés bruto como el neto.
        
        Args:
            monto_inicial: Monto inicial de la inversión
            tasa_interes: Tasa de interés anual
            dias_plazo: Días del plazo de la inversión
            
        Returns:
            Tupla con (interés_bruto, interés_neto)
        """
        interes_bruto = self.calcular_interes_bruto(monto_inicial, tasa_interes, dias_plazo)
        interes_neto = self.calcular_interes_neto(interes_bruto)
        return interes_bruto, interes_neto
    
    def mostrar_resultado(self, monto_inicial: float, interes_neto: float, dias_plazo: int) -> None:
        """
        Muestra el resultado del cálculo de manera formateada.
        
        Args:
            monto_inicial: Monto inicial de la inversión
            interes_neto: Interés neto calculado
            dias_plazo: Días del plazo de la inversión
        """
        print(f'\nTu depósito de Q {monto_inicial:,.2f} genera un interés de Q {interes_neto:,.2f} en {dias_plazo} días.\n')
    
    def ejecutar_calculo(self) -> None:
        """Ejecuta el proceso completo de cálculo de intereses."""
        try:
            monto_inicial = self.obtener_monto_inicial()
            tasa_interes = self.obtener_tasa_interes()
            dias_plazo = self.obtener_dias_plazo()
            
            interes_bruto, interes_neto = self.calcular_interes_completo(
                monto_inicial, tasa_interes, dias_plazo
            )
            
            self.mostrar_resultado(monto_inicial, interes_neto, dias_plazo)
            
        except KeyboardInterrupt:
            print("\n\nOperación cancelada por el usuario.")
            sys.exit(0)
        except Exception as e:
            print(f"\nError inesperado: {e}")
            sys.exit(1)


def main():
    """Función principal que ejecuta la calculadora."""
    calculadora = CalculadoraInteres()
    calculadora.ejecutar_calculo()


if __name__ == "__main__":
    main()
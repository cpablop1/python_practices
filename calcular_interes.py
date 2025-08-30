# Herramienta para calcular intéres de cuenta de plaza fija

print('\nIngrese el monto inicial:')
monto_inicial = float(input()) # Ingresamos el monto inicial para calcular
print('Ingrese la tasa de interés, por ejemplo (0.07, 0.06, 0.05)')
tasa_interes = float(input()) # Ingresamos la tasa de interés que se aplica sobre el monto inicial
print('Ingrese la cantiad de días del plazo, por ejemplo (90, 180, 360)')
dias_plazo = int(input()) # Ingresamos la cantidad de días que estará el monto en el banco de plaza fija

# Hacemos los cálculos con los datos obtenidos
calculo = monto_inicial * tasa_interes * (dias_plazo / 365)

print(f'\nTu depósito de Q {monto_inicial} generá un interés de Q {calculo} en {dias_plazo} días.')
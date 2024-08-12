a = 'abra'
b = 'cad'
print('{0:<5}{1:^10}{0:>5}'.format(a, b))

for x in range(1, 11):
    print('{3}{0:2d}{3} {3}{1:3d}{3} {3}{2:4d}{3}'.format(x, x * x, x * x * x, '|'))

studentsList = [['Juan', 'Carmelo', 5, 7, 9, 7], ['Laura', 'Jazmine', 7, 8, 5, 6.66],
 ['Dario', 'Villalobos', 5, 6, 3, 4.66], ['Marito', 'Tasolo', 4, 7, 9, 6.666],
  ['Esteban', 'Quito', 9, 9, 8, 8.66]]

table = """\
+---------------------------------------------------------------------+
| Nombre    Apellido        Primero Segundo Tercero     Promedio anual|
|---------------------------------------------------------------------|
{}
+---------------------------------------------------------------------+\
"""

table = (table.format('\n'.join("| {:<8} {:<10} {:>8} {:>6} {:>7} {:>23} |".format(*row)
 for row in studentsList)))

print(table)
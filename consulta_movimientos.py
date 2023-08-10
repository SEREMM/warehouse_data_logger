import pandas as pd
import numpy as np
# ctrl + b to run file

data = pd.read_csv('C:/Users/Sergio Ordaz/Downloads/gastosIngresosBod.csv')
ingresos = data.query('type == "ingreso"')
ingresos = ingresos.drop(columns=['type','importe'])
gastos = data.query('type == "gasto"')
gastos = gastos.drop(columns=['type','kg','price','total'])

print('ingresos\n')
print(ingresos.query('date > "2023-05-24"'))
print('\ngastos\n')
print(gastos.query('date > "2023-05-24"'))
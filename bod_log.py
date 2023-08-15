import numpy as np
import pandas as pd
import datetime
import csv
import pytz

def formato(func):
    def wrapper(*args, **kwargs):
        titulo = args[0]
        linea = "=" * len(titulo)
        print(linea,'\n' + titulo,'\n')
        resultado = func(*args, **kwargs)
        print(linea,'\n')
        return resultado
    return wrapper

def get_current_hour():
    return (datetime.datetime.utcnow() - datetime.timedelta(hours=6)).strftime('%H:%M:%S')

def get_current_date():
    timezone = pytz.timezone('America/Mexico_City')
    gmt_minus_6 = datetime.datetime.now(timezone)
    date_gmt_minus_6 = gmt_minus_6.strftime('%Y-%m-%d')
    return date_gmt_minus_6

def create_csv_file():
    df = pd.DataFrame(columns=['type','date','hour','kg','price','total','importe','concept','comment'])
    df.to_csv('movimientos_bod.csv', index=False)

def append_csv_row(row):
    with open('movimientos_bod.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(row)

@formato
def ing(titulo):
    try:
        kg = input("Ingrese la cantidad en kilogramos: ")
        if kg == '':
            kg = float(0)
            price = float(0)
            total = float(input('Ingrese el total de ingreso: '))
        else:
            kg = float(kg)
            price = float(input("Ingrese el precio por kilogramo: "))
            total = round(kg * price, 2)
            print('\n:::')
            print(total)
            print(':::\n')
        concept = input("Ingrese el concepto: ")
        comment = input("Ingrese el comentario: ")
        row = ['ing',get_current_date(),get_current_hour(),kg,price,total,0,concept,comment]
        append_csv_row(row)
    except:
        print('--- Dato no válido ---')

@formato
def gas(titulo):
    try:
        importe = float(input("Ingrese el importe: "))
        concept = input("Ingrese el concepto: ")
        comment = input("Ingrese el comentario: ")
        row = ['gas',get_current_date(),get_current_hour(),0,0,0,importe,concept,comment]
        append_csv_row(row)
    except:
        print('--- Dato no válido ---')

@formato
def comentario(titulo):
    concept = input("Ingrese el titulo del comentario: ")
    comment = input("Ingrese el cuerpo del comentario: ")
    row = ['coment',get_current_date(),get_current_hour(),0,0,0,0,concept,comment]
    append_csv_row(row)

@formato
def delete_and_repeat(titulo):
    try:
      df = pd.read_csv('movimientos_bod.csv')
      last_row = df.iloc[-1:,:]
      df = df.drop(df.index[-1])
      df.to_csv('movimientos_bod.csv', index=False)
      print(f"Deleted row: {last_row}")
    except FileNotFoundError:
        print("--- No previous row to delete ---")

@formato
def start(titulo):
    option = ''
    while option != 'c':
        print("enter. Ingreso")
        print("1. Gasto")
        print("2. Comentario")
        print("c. Cerrar")
        print('d. borrar registro anterior')
        option = input()
        print('')
        if option == '':
            ing('Ingreso')
        elif option == '1':
            gas('Gasto')
        elif option == '2':
            comentario('Comentario')
        elif option == 'c':
            print("Programa finalizado.")
        elif option == 'd':
            delete_and_repeat('Eliminar fila')
        else:
            print("--- Opción no válida ---")

# main
try:
    df = pd.read_csv('movimientos_bod.csv')
except FileNotFoundError:
    create_csv_file()

start('Seleccione una opción')

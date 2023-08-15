import numpy as np
import pandas as pd
import datetime
import csv
import pytz

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


def ing():
    print('===')
    print('')
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
            print('')
            print(':::')
            print(total)
            print(':::')
            print('')
        concept = input("Ingrese el concepto: ")
        comment = input("Ingrese el comentario: ")
        row = ['ing',get_current_date(),get_current_hour(),kg,price,total,0,concept,comment]
        append_csv_row(row)
        print('...')
        print('')
    except:
        print('Dato no válido')
        print('...')
        print('')
        # start()


def gas():
    print('===')
    print('')
    try:
        importe = float(input("Ingrese el importe: "))
        concept = input("Ingrese el concepto: ")
        comment = input("Ingrese el comentario: ")
        row = ['gas',get_current_date(),get_current_hour(),0,0,0,importe,concept,comment]
        append_csv_row(row)
        print('...')
        print('')
    except:
        print('Dato no válido')
        print('...')
        print('')
        # start()


def comentario():
    print('===')
    print('')
    concept = input("Ingrese el titulo del comentario: ")
    comment = input("Ingrese el cuerpo del comentario: ")
    row = ['coment',get_current_date(),get_current_hour(),0,0,0,0,concept,comment]
    append_csv_row(row)
    print('...')
    print('')


def delete_and_repeat():
    print('===')
    print('')
    try:
      df = pd.read_csv('movimientos_bod.csv')
      last_row = df.iloc[-1:,:]
      df = df.drop(df.index[-1])
      df.to_csv('movimientos_bod.csv', index=False)
      print(f"Deleted row: {last_row}")
    except FileNotFoundError:
        print("No previous row to delete")
    print('...')
    print('')


def start():
    option = ''
    while option != 'c':
        print('===')
        print('')
        print("Seleccione una opción:")
        print('')
        print("enter. Ingreso")
        print("1. Gasto")
        print("2. Comentario")
        print("c. Cerrar")
        print('d. borrar registro anterior')
        option = input()
        print('')
        if option == '':
            ing()
        elif option == '1':
            gas()
        elif option == '2':
            comentario()
        elif option == 'c':
            print("Programa finalizado.")
        elif option == 'd':
            delete_and_repeat()
        else:
            print("Opción no válida.")
        print('...')
        print('')

# main
try:
    df = pd.read_csv('movimientos_bod.csv')
except FileNotFoundError:
    create_csv_file()

start()

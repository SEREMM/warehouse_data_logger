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

def get_date_minus_days(dias):
    timezone = pytz.timezone('America/Mexico_City')
    gmt_minus_6 = datetime.datetime.now(timezone) - datetime.timedelta(days=dias)
    date_gmt_minus_6 = gmt_minus_6.strftime('%Y-%m-%d')
    return date_gmt_minus_6

def create_csv_file():
    df = pd.DataFrame(columns=['type','date','hour','client-prov','kg-descarga','price-diadescarga','concept-camion','comment',
                                'alto','procedencia','semilla','caracteristicas'])
    df.to_csv('pedidos_descarga.csv', index=False)

def append_csv_row(row):
    with open('pedidos_descarga.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(row)

@formato
def pedido(titulo):
    cliente = input('Ingrese el cliente: ')
    kg = input("Ingrese los kilogramos del pedido: ")
    price = input('Ingrese el precio: ')
    concept = input("Ingrese el tipo de producto: ")
    fecha = input("fecha actual (enter), restar dias a actual (num, ej. 1),\notra fecha (fec, ej. 2023-09-01): ")
    if fecha == 'fec':
        row = ['pedido',fecha,get_current_hour(),cliente,kg,price,concept]
    else:
        try:
            dias_minus = int(fecha)
            fecha = get_date_minus_days(dias_minus)
            print(f'fecha: {fecha}')
            row = ['pedido',fecha,get_current_hour(),cliente,kg,price,concept]
        except ValueError:
            row = ['pedido',get_current_date(),get_current_hour(),cliente,kg,price,concept]
    append_csv_row(row)

@formato
def descarga(titulo):
    cantidad = input("Ingrese cuanto se descargó (1 entero, .5 medio): ")
    camion = input("Ingrese el camión: ")
    razo = input("Ingrese si venía razo o con copete: ")
    dia = input('Ingrese el día que lleva en bodega: ')
    comentario = input('Ingrese un comentario: ')
    procedencia = input('Ingrese la procedencia de la carga: ')
    proveedor = input('Ingrese nombre del proveedor: ')
    semilla = input('Ingrese la semilla: ')
    caracteristicas = input('Características del producto tamaño, color, enfermedades,\ncant. de hojas. Separador "-": ')
    fecha = input("fecha actual (enter), otra fecha (ej. 2023-01-01): ")
    if fecha != '':
        row = ['descarga',fecha,get_current_hour(),proveedor,cantidad,
            dia,camion,comentario,razo,procedencia,semilla,caracteristicas]
    else:
        row = ['descarga',get_current_date(),get_current_hour(),proveedor,cantidad,
            dia,camion,comentario,razo,procedencia,semilla,caracteristicas]
    append_csv_row(row)

@formato
def comentario(titulo):
    concept = input("Ingrese el titulo del comentario: ")
    comment = input("Ingrese el cuerpo del comentario: ")
    row = ['coment',get_current_date(),get_current_hour(),0,0,0,0,concept,comment]
    append_csv_row(row)

@formato
def delete_and_repeat(titulo):
    try:
      df = pd.read_csv('pedidos_descarga.csv')
      last_row = df.iloc[-1:,:]
      df = df.drop(df.index[-1])
      df.to_csv('pedidos_descarga.csv', index=False)
      print(f"Deleted row: {last_row}")
    except FileNotFoundError:
        print("--- No previous row to delete ---")
    except UnicodeDecodeError:
        df = pd.read_csv('pedidos_descarga.csv', encoding='latin_1')
        last_row = df.iloc[-1:,:]
        df = df.drop(df.index[-1])
        df.to_csv('pedidos_descarga.csv', index=False)
        print(f"Deleted row: {last_row}")

@formato
def start(titulo):
    option = ''
    while option != 'c':
        print("enter. Pedido")
        print("1. Descarga")
        print("2. Comentario")
        print("c. Cerrar")
        print('d. borrar registro anterior')
        option = input()
        print('')
        if option == '':
            pedido('Pedido')
        elif option == '1':
            descarga('Descarga')
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
    df = pd.read_csv('pedidos_descarga.csv')
except FileNotFoundError:
    create_csv_file()
except UnicodeDecodeError:
    df = pd.read_csv('pedidos_descarga.csv', encoding='latin_1')

start('Seleccione una opción')

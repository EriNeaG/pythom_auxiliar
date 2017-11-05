#!/usr/bin/env python
import csv
import sys
import pandas
from flask import Flask, render_template, request, redirect, url_for, flash, session
from formularios import Consulta_Cliente,Consulta_Producto,Consulta_Cantidad,Consulta_Precio, Formulario_Logueo,Formulario_Registro
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_script import Manager

app = Flask(__name__)
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)

app.config['SECRET_KEY'] = 'un string que funcione como llave'

#Creacion de una lista en donde se guadaran los datos de log de usuario.
#Se encampsulan los posibles errores que puede suceden al no encontrar los archivos csv.
users_check = []
try:
    with open('usuariosbase.csv') as archivo:
        leer_csv = csv.reader(archivo)
        for linea in leer_csv:
            users_check.append(linea[0])
except FileNotFoundError:
    print('Error de CSV de usuariosbase')

try:
    with open('Ventas.csv') as archivo:
        pass
except FileNotFoundError:
    print('No se encuentra el archivo CSV de Ventas')

#La pagina esta pensada para que descubra/muestre el menu si la persona se loggea.
@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html', username=session.get('username'))
    return render_template('sign_off.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form_logueo = Formulario_Logueo()
#Se abre el archivo que contiene los usuarios y contraseñas, y si las credenciales que ingresa el usuario son encontradas en el archivo, lo loguea.
    if form_logueo.validate_on_submit():
        try:
            with open('usuariosbase.csv') as archivo:
                #El siguiente try es por si se ingresa un unico campo lo campture en el IndexError
                try:
                    f = csv.reader(archivo)
                    for linea in f:
                        p = linea
                        a = p[0]
                        b = p[1]
                        if form_logueo.name.data == a and form_logueo.password.data == b:
                            session['username'] = form_logueo.name.data
                            #El return renderiza en index.html con la sesion iniciada (poder ver el menu).
                            return render_template('index.html', username=session.get('username'))
                except IndexError:
                    return 'Número de campos en archivo usuariosbase.csv es invalido'        
        except FileNotFoundError:
            return 'No se encuentra el archivo de usuariosbase'
    return render_template('login.html', form=form_logueo, username=session.get('username'))

#abre el archivo csv con la información a mostrar en la tabla, los headers los guarda en una variable, y el resto de la lista en la otra, luego se envía las variables a la plantilla html para que de formato y muestre la tabla.

@app.route('/ventas', methods=['GET', 'POST'])
def contactos():
    if 'username' in session:
        try:
            with open('Ventas.csv', 'r') as archivo:
                lista_ventas = csv.reader(archivo)                
                primera_linea = next(lista_ventas)                                
                return render_template('ventas.html', cabeza=primera_linea, cuerpo=lista_ventas, username=session.get('username'))
        except FileNotFoundError:
            return 'No se encuentra el archivo CSV'
    return render_template('sign_off.html')

#Busquedas en la tabla (para hacer las busquedas, utilizé el dataFrame de Pandas, que primero lee el archivo y lo guarda en una variable, luego, como argumento le hardcodeo el header de la columna en la cual quiero hacer la busqueda, y paso como dato lo que el usuario haya ingresado para buscar, si lo que se buscó se encuentra en el dataframe, guardara en la variable df2 el resultado. Luego, utilizando el metodo "to_csv" del dataframe, guardo en un archivo el resultado, con formato csv, y hago exactamente lo mismo que en la url anterior, abro el archivo, guardo los headers en una variable, los resultados en otra, y los envio a la plantilla html.

@app.route('/busqueda/cliente', methods=['GET', 'POST'])
def busqueda_cliente():
    if 'username' in session:        
        form_nombre = Consulta_Cliente()    
        try:
            df = pandas.read_csv('Ventas.csv')
        except FileNotFoundError:
            return 'No se encuentra el archivo CSV de Ventas'    
        if form_nombre.validate_on_submit():            
            with open('Ventas.csv') as archivo:
                try:
                    f = csv.reader(archivo)
                    ventas=[]
                    for linea in f:
                        p = linea
                        codigo = p[0]
                        cliente = p[1]
                        # El Array tupla, tiene los titulos del encabezado
                        if "CODIGO" == codigo:
                            tupla = [p[0],p[1],p[2],p[3],p[4]]
                        # Este Array guarda las ventas que coincide el cliente
                        if form_nombre.criterio.data.lower() in cliente.lower():
                            venta = [p[0],p[1],p[2],p[3],p[4]]
                            ventas.append(venta)
                    return render_template('resultado.html', form=form_nombre, cabeza=tupla, cuerpo=ventas, username=session.get('username'))
                except IndexError:
                    return 'Numero invalido de datos a corroborar.'           
        return render_template('busqueda_cliente.html', form=form_nombre, df=df, username=session.get('username'))
    return render_template('sign_off.html')

@app.route('/busqueda/producto', methods=['GET', 'POST'])
def busqueda_producto():
    if 'username' in session:        
        form_producto = Consulta_Producto()
        try:
            df = pandas.read_csv('Ventas.csv')
        except FileNotFoundError:
            return 'No se encuentra el archivo CSV de Ventas'
        if form_producto.validate_on_submit():
            with open('Ventas.csv') as archivo:
                try:
                    f = csv.reader(archivo)
                    ventas=[]
                    for linea in f:
                        p = linea
                        codigo = p[0]
                        producto = p[2]
                        # El Array tupla, tiene los titulos del encabezado
                        if "CODIGO" == codigo:
                            tupla = [p[0],p[1],p[2],p[3],p[4]]
                        # Este Array guarda las ventas que coincide el cliente
                        if form_producto.criterio.data.lower() in producto.lower():
                            venta = [p[0],p[1],p[2],p[3],p[4]]
                            ventas.append(venta)
                    return render_template('resultado.html', form=form_producto, cabeza=tupla, cuerpo=ventas, username=session.get('username'))
                except IndexError:
                    return 'Número de campos en archivo Usuarios es invalido'                           
        return render_template('busqueda_producto.html', form=form_producto, df=df, username=session.get('username'))
    return render_template('sign_off.html')

@app.route('/busqueda/cantidad', methods=['GET', 'POST'])
def busqueda_cantidad():
    if 'username' in session:
        form_cantidad = Consulta_Cantidad()
        try:
            df = pandas.read_csv('Ventas.csv')
        except FileNotFoundError:
            return 'No se encuentra el archivo CSV de Ventas'
        if form_cantidad.validate_on_submit():
            with open('Ventas.csv') as archivo:
                try:
                    f = csv.reader(archivo)
                    ventas=[]
                    for linea in f:
                        p = linea
                        codigo = p[0]
                        cantidad = p[3]                        
                        # El Array tupla, tiene los titulos del encabezado
                        if "CODIGO" == codigo:
                            tupla = [p[0],p[1],p[2],p[3],p[4]]
                        # Este Array guarda las ventas que coincide el cliente
                        if form_cantidad.criterio.data == cantidad:
                            venta = [p[0],p[1],p[2],p[3],p[4]]
                            ventas.append(venta)                            
                    return render_template('resultado.html', form=form_cantidad, cabeza=tupla, cuerpo=ventas, username=session.get('username'))
                except IndexError:
                    return 'Error al encontrar los usuarios y cantidad'                           
        return render_template('busqueda_cantidad.html', form=form_cantidad, df=df, username=session.get('username'))
    return render_template('sign_off.html')


@app.route('/busqueda/precio', methods=['GET', 'POST'])
def busqueda_precio():
    if 'username' in session:
        form_precio = Consulta_Precio()
        try:
            df = pandas.read_csv('Ventas.csv')
        except FileNotFoundError:
            return 'No se encuentra el archivo CSV de Ventas'
        if form_precio.validate_on_submit():
            with open('Ventas.csv') as archivo:
                try:
                    f = csv.reader(archivo)
                    ventas=[]
                    for linea in f:
                        p = linea
                        codigo = p[0]
                        precio = p[4]                        
                        # El Array tupla, tiene los titulos del encabezado
                        if "CODIGO" == codigo:
                            tupla = [p[0],p[1],p[2],p[3],p[4]]
                        # Este Array guarda las ventas que coincide el cliente
                        if form_precio.criterio.data == precio:
                            venta = [p[0],p[1],p[2],p[3],p[4]]
                            ventas.append(venta)                           
                    return render_template('resultado.html', form=form_precio, cabeza=tupla, cuerpo=ventas, username=session.get('username'))
                except IndexError:
                    return 'Error al buscar el usuario y su precio'                           
        return render_template('busqueda_precio.html', form=form_precio, df=df, username=session.get('username'))
    return render_template('sign_off.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form_registro = Formulario_Registro()
    if form_registro.validate_on_submit():
        if form_registro.password1.data == form_registro.password2.data:
            try:
                with open('usuariosbase.csv') as archivo:
                    escritor = csv.writer(archivo)
                    if form_registro.name.data in users_check:
                        return "Usuario existente"
                    else:
                        escritor.writerow([form_registro.name.data, form_registro.password1.data])
                        return redirect('login')
            except FileNotFoundError:
                return 'No se encuentra el CSV'
        return "Revise la contraseña"
    return render_template('register.html', form=form_registro)

@app.route('/signoff', methods=['GET', 'POST'])
def desloguearse():
    session.pop('username', None)
    return redirect('/login')

@app.errorhandler(404)
def no_encontrado(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def error_interno(e):
    return render_template('500.html'), 500

if __name__ == "__main__":
    manager.run()
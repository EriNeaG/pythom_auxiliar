#!/usr/bin/env python
import csv
import sys
import pandas
from flask import Flask, render_template, request, redirect, url_for, flash, session
from formularios import Consulta_Cliente,Consulta_Producto,Consulta_Cantidad,Consulta_Precio, Checkeo_Log,Formulario_Registro
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
    with open('bdatos.csv') as archivo:
        pass
except FileNotFoundError:
    print('Error al buscar el csv de base de datos')

#La pagina esta pensada para que descubra/muestre el menu si la persona se loggea.
@app.route('/')
def index():
    if 'usuarioLoggeado' in session:
        return render_template('index.html', username=session.get('usuarioLoggeado'))
    return render_template('sign_off.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    fomu_log= Checkeo_Log()
#Se abre el archivo que contiene los usuarios y contraseñas, y si las credenciales que ingresa el usuario son encontradas en el archivo, lo loguea.
    if fomu_log.validate_on_submit():
        try:
            with open('usuariosbase.csv') as archivo:
                #El siguiente try es por si se ingresa un unico campo lo campture en el IndexError
                try:
                    filecsv = csv.reader(archivo)
                    for linea in filecsv:
                        ubicacion = linea
                        nombre = ubicacion[0]
                        contrasenia = ubicacion[1]
                        if fomu_log.name.data == nombre and fomu_log.password.data == contrasenia:
                            session['usuarioLoggeado'] = fomu_log.name.data
                            #El return renderiza en index.html con la sesion iniciada (poder ver el menu).
                            return render_template('index.html', username=session.get('usuarioLoggeado'))
                except IndexError:
                    return 'usuario de usuariosbase.csv invalido'        
        except FileNotFoundError:
            return 'No se encuentra el archivo de usuariosbase'
    return render_template('login.html', form=fomu_log, username=session.get('usuarioLoggeado'))

#conformacion de la base de datos que solo sera visible si estas loggeado.
@app.route('/basededatos', methods=['GET', 'POST'])
def bdatos():
    if 'usuarioLoggeado' in session:
        try:
            with open('bdatos.csv', 'r') as archivo:
                datalines = csv.reader(archivo)                
                titulos = next(datalines)                                
                return render_template('tabla.html', cabeza=titulos, cuerpo=datalines, username=session.get('usuarioLoggeado'))
        except FileNotFoundError:
            return 'No se encuentra la base de datos de PharmaDino'
    return render_template('sign_off.html')

#Este menu aparece cuando se esta loggeado.
@app.route('/cliente', methods=['GET', 'POST'])
def busqueda_cliente():
    if 'usuarioLoggeado' in session:        
        form_nombre = Consulta_Cliente()    
        try:
            with open('bdatos.csv') as archivo:
                pass
        except FileNotFoundError:
            return 'cvs de base de datos inexistente'    
        if form_nombre.validate_on_submit():            
            with open('bdatos.csv') as archivo:
                try:
                    filecsv = csv.reader(archivo)
                    infos=[]
                    for linea in filecsv:
                        ubicacion = linea
                        codigo = ubicacion[0]
                        cliente = ubicacion[1]
                        # El Array tupla, tiene los titulos del encabezado
                        if "CODIGO" == codigo:
                            tupla = [ubicacion[0],ubicacion[1],ubicacion[2],ubicacion[3],ubicacion[4]]
                        # Este Array guarda las info que coincide el cliente
                        if form_nombre.criterio.data.lower() in cliente.lower():
                            info = [ubicacion[0],ubicacion[1],ubicacion[2],ubicacion[3],ubicacion[4]]
                            infos.append(info)
                    return render_template('tabla.html', form=form_nombre, cabeza=tupla, cuerpo=infos, username=session.get('usuarioLoggeado'))
                except IndexError:
                    return 'Numero invalido de datos a corroborar.'           
        return render_template('cliente.html', form=form_nombre, username=session.get('usuarioLoggeado'))
    return render_template('sign_off.html')

@app.route('/busqueda/producto', methods=['GET', 'POST'])
def busqueda_producto():
    if 'usuarioLoggeado' in session:        
        form_producto = Consulta_Producto()
        try:
            with open('bdatos.csv') as archivo:
                pass
        except FileNotFoundError:
            return 'Error al buscar el csv de base de datos'
        if form_producto.validate_on_submit():
            with open('bdatos.csv') as archivo:
                try:
                    filecsv = csv.reader(archivo)
                    infos=[]
                    for linea in filecsv:
                        ubicacion = linea
                        codigo = ubicacion[0]
                        producto = ubicacion[2]
                        # El Array tupla, tiene los titulos del encabezado
                        if "CODIGO" == codigo:
                            tupla = [ubicacion[0],ubicacion[1],ubicacion[2],ubicacion[3],ubicacion[4]]
                        # Este Array guarda las infos que coincide el cliente
                        if form_producto.criterio.data.lower() in producto.lower():
                            info = [ubicacion[0],ubicacion[1],ubicacion[2],ubicacion[3],ubicacion[4]]
                            infos.append(info)
                    return render_template('tabla.html', form=form_producto, cabeza=tupla, cuerpo=infos, username=session.get('usuarioLoggeado'))
                except IndexError:
                    return 'Número de campos en archivo Usuarios es invalido'                           
        return render_template('busqueda_producto.html', form=form_producto, username=session.get('usuarioLoggeado'))
    return render_template('sign_off.html')

@app.route('/busqueda/cantidad', methods=['GET', 'POST'])
def busqueda_cantidad():
    if 'usuarioLoggeado' in session:
        form_cantidad = Consulta_Cantidad()
        try:
            with open('bdatos.csv') as archivo:
                pass
        except FileNotFoundError:
            return 'Error al buscar el csv de base de datos'
        if form_cantidad.validate_on_submit():
            with open('bdatos.csv') as archivo:
                try:
                    filecsv = csv.reader(archivo)
                    infos=[]
                    for linea in filecsv:
                        ubicacion = linea
                        codigo = ubicacion[0]
                        cantidad = ubicacion[3]                        
                        # El Array tupla, tiene los titulos del encabezado
                        if "CODIGO" == codigo:
                            tupla = [ubicacion[0],ubicacion[1],ubicacion[2],ubicacion[3],ubicacion[4]]
                        # Este Array guarda las infos que coincide el cliente
                        if form_cantidad.criterio.data == cantidad:
                            info = [ubicacion[0],ubicacion[1],ubicacion[2],ubicacion[3],ubicacion[4]]
                            infos.append(info)                            
                    return render_template('tabla.html', form=form_cantidad, cabeza=tupla, cuerpo=infos, username=session.get('usuarioLoggeado'))
                except IndexError:
                    return 'Error al encontrar los usuarios y cantidad'                           
        return render_template('busqueda_cantidad.html', form=form_cantidad, username=session.get('usuarioLoggeado'))
    return render_template('sign_off.html')


@app.route('/busqueda/precio', methods=['GET', 'POST'])
def busqueda_precio():
    if 'usuarioLoggeado' in session:
        form_precio = Consulta_Precio()
        try:
            with open('bdatos.csv') as archivo:
                pass
        except FileNotFoundError:
            return 'No se encuentra el archivo CSV de infos'
        if form_precio.validate_on_submit():
            with open('bdatos.csv') as archivo:
                try:
                    filecsv = csv.reader(archivo)
                    infos=[]
                    for linea in filecsv:
                        ubicacion = linea
                        codigo = ubicacion[0]
                        precio = ubicacion[4]                        
                        # El Array tupla, tiene los titulos del encabezado
                        if "CODIGO" == codigo:
                            tupla = [ubicacion[0],ubicacion[1],ubicacion[2],ubicacion[3],ubicacion[4]]
                        # Este Array guarda las infos que coincide el cliente
                        if form_precio.criterio.data == precio:
                            info = [ubicacion[0],ubicacion[1],ubicacion[2],ubicacion[3],ubicacion[4]]
                            infos.append(info)                           
                    return render_template('tabla.html', form=form_precio, cabeza=tupla, cuerpo=infos, username=session.get('usuarioLoggeado'))
                except IndexError:
                    return 'Error al buscar el usuario y su precio'                           
        return render_template('busqueda_precio.html', form=form_precio, username=session.get('usuarioLoggeado'))
    return render_template('sign_off.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form_registro = Formulario_Registro()
    if form_registro.validate_on_submit():
        if form_registro.password1.data == form_registro.password2.data:
            try:
                with open('usuariosbase.csv', 'a') as archivo:
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
    session.pop('usuarioLoggeado', None)
    return redirect('/login')

@app.errorhandler(404)
def no_encontrado(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def error_interno(e):
    return render_template('500.html'), 500

if __name__ == "__main__":
    manager.run()
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField
from wtforms.validators import DataRequired,EqualTo,Regexp,Length

#Clases para las consultas:
class Consulta_Cliente(FlaskForm):
    criterio = StringField('Escriba el Nombre del Cliente: ', validators=[Length(min=3, max=100, message="Debe ingresar como minimo 3 caracteres"),DataRequired(message="Debe escribir valor")])

class Consulta_Producto(FlaskForm):
    criterio = StringField('Escriba el Nombre del Producto: ', validators=[DataRequired(message="Debe escribir un valor")])

class Consulta_Cantidad(FlaskForm):
    criterio = StringField('Escriba la Cantidad que Stock que desea buscar: ', validators=[DataRequired(message="Debe escribir un valor"),Regexp(regex="\d+", message="Solo nùmeros enteros por favor")])

class Consulta_Precio(FlaskForm):
    criterio = StringField('Escriba el Precio que busca: ', validators=[DataRequired(message="Debe escribir un valor"),Regexp(regex="^(\d|-)?(\d|,)*\.?\d*$", message="Ingrese un precio valido")])
    #/^[1-9]\d*$/

#Formulario para logueo del usuario.

class Formulario_Logueo(FlaskForm):
    name = StringField('Usuario:', validators=[DataRequired(message="Debe escribir un nombre de usuario")])
    password = PasswordField('Contraseña:', validators=[DataRequired(message="Debe escribir una contraseña")])

#Formulario para registro de un nuevo usuario.

class Formulario_Registro(FlaskForm):
    name = StringField('Usuario:', validators=[DataRequired(message="Debe escribir un nombre de usuario")])
    password1 = PasswordField('Contraseña:', validators=[DataRequired(message="Debe escribir una contraseña")])
    password2 = PasswordField('Repita Contraseña:', validators=[DataRequired(message="Debe escribir de nuevo su contraseña"),EqualTo('password1', message='Las contraseñas deben coincidir')])

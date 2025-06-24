from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from wtforms import IntegerField, FileField

class ContactForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(max=50)])
    apellido = StringField('Apellido', validators=[DataRequired(), Length(max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    comentario = TextAreaField('Comentario', validators=[DataRequired(), Length(max=500)])
    enviar = SubmitField('Enviar')

class ServicioForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    detalle = StringField('Detalle', validators=[DataRequired()])
    precio = IntegerField('Precio', validators=[DataRequired()])
    imagen = FileField('Imagen')
    enviar = SubmitField('Agregar Servicio')

class ProductoForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    detalle = StringField('Detalle', validators=[DataRequired()])
    precio = IntegerField('Precio', validators=[DataRequired()])
    imagen = FileField('Imagen')
    enviar = SubmitField('Agregar Producto')
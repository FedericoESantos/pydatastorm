from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms.fields.numeric import FloatField, IntegerField
from wtforms.fields.simple import StringField, SubmitField
from wtforms.validators import DataRequired, NumberRange

from database import db

class Servicio(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(250))
    detalle = db.Column(db.Text)
    precio = db.Column(db.Integer)
    imagen = db.Column(db.String(100))

    def __str__(self):
        return (f'ID: {self.id} \n'
                f'NOMBRE: {self.nombre} \n'
                f'DESCRIPCION: {self.detalle} \n'
                f'PRECIO: {self.precio} \n'
                f'IMAGEN: {self.imagen}'
                )

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(250))
    detalle = db.Column(db.Text)
    precio = db.Column(db.Integer)
    imagen = db.Column(db.String(100))

    def __str__(self):
        return (f'ID: {self.id} \n'
                f'NOMBRE: {self.nombre} \n'
                f'DESCRIPCION: {self.detalle} \n'
                f'PRECIO: {self.precio} \n'
                f'IMAGEN: {self.imagen}'
                )

class ProductoForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    detalle = StringField('Detalle', validators=[DataRequired()])
    precio = IntegerField('Precio', validators=[DataRequired(), NumberRange(min=0)])
    imagen = FileField('Imagen', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'webp'], 'Solo imágenes.')])
    imagen_nombre = StringField('Nombre de imagen')
    enviar = SubmitField('enviar')


class ServicioForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    detalle = StringField('Detalle', validators=[DataRequired()])
    precio = IntegerField('Precio', validators=[DataRequired(), NumberRange(min=0)])
    imagen = FileField('Imagen', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'webp'], 'Solo imágenes.')])
    imagen_nombre = StringField('Nombre de imagen')
    enviar = SubmitField('enviar')

class VisitasUnicas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contador = db.Column(db.Integer, default=0)
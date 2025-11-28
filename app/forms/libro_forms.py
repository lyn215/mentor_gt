from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, BooleanField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, NumberRange

class LibroForm(FlaskForm):
    """Formulario para libros y capítulos"""
    titulo = StringField('Título', validators=[DataRequired(), Length(max=500)],
                        render_kw={"placeholder": "Ej: Introducción a la programación"})
    editorial = StringField('Editorial', validators=[Optional(), Length(max=255)],
                           render_kw={"placeholder": "Ej: Pearson, McGraw-Hill"})
    anio = IntegerField('Año de Publicación', validators=[Optional(), NumberRange(min=1900, max=2100)],
                       render_kw={"placeholder": "Ej: 2023"})
    pais = StringField('País', validators=[Optional(), Length(max=100)],
                      render_kw={"placeholder": "Ej: México"})
    idioma = StringField('Idioma', validators=[Optional(), Length(max=50)],
                        render_kw={"placeholder": "Ej: Español"})
    isbn = StringField('ISBN', validators=[Optional(), Length(max=50)],
                      render_kw={"placeholder": "Ej: 978-607-1234-56-7"})
    tipo = SelectField('Tipo', choices=[
        ('', 'Seleccionar'),
        ('Libro completo', 'Libro completo'),
        ('Capítulo de libro', 'Capítulo de libro'),
        ('Libro coordinado', 'Libro coordinado')
    ], validators=[Optional()])
    numero_capitulo = StringField('Número de Capítulo', validators=[Optional(), Length(max=50)])
    titulo_capitulo = StringField('Título del Capítulo', validators=[Optional(), Length(max=500)])
    rol_participacion = SelectField('Rol de Participación', choices=[
        ('', 'Seleccionar'),
        ('Autor', 'Autor'),
        ('Coautor', 'Coautor'),
        ('Coordinador', 'Coordinador'),
        ('Editor', 'Editor')
    ], validators=[Optional()])
    autores = TextAreaField('Autores', validators=[Optional()],
                           render_kw={"placeholder": "Ej: García J.; López M.; Pérez R.", "rows": 2})
    producto_destacado = BooleanField('Producto Destacado')
    submit = SubmitField('Guardar')


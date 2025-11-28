from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, SelectField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, NumberRange

class ArticuloForm(FlaskForm):
    titulo = StringField('Título', validators=[DataRequired(), Length(max=500)])
    revista = StringField('Revista', validators=[Optional(), Length(max=255)])
    anio = IntegerField('Año', validators=[Optional(), NumberRange(min=1900, max=2100)])
    volumen = StringField('Volumen', validators=[Optional(), Length(max=50)])
    numero = StringField('Número', validators=[Optional(), Length(max=50)])
    paginas = StringField('Páginas', validators=[Optional(), Length(max=50)])
    rol_participacion = SelectField('Rol de Participación', choices=[
        ('', 'Seleccionar'), ('autor', 'Autor'), ('coautor', 'Coautor'),
        ('editor', 'Editor'), ('revisor', 'Revisor')
    ], validators=[Optional()])
    objetivo = TextAreaField('Objetivo', validators=[Optional()])
    estado = SelectField('Estado', choices=[
        ('', 'Seleccionar'), ('publicado', 'Publicado'), ('aceptado', 'Aceptado'),
        ('en_revision', 'En Revisión'), ('enviado', 'Enviado')
    ], validators=[Optional()])
    issn_impreso = StringField('ISSN Impreso', validators=[Optional(), Length(max=50)])
    issn_electronico = StringField('ISSN Electrónico', validators=[Optional(), Length(max=50)])
    doi = StringField('DOI', validators=[Optional(), Length(max=255)])
    indexacion = StringField('Indexación', validators=[Optional(), Length(max=255)])
    autores = TextAreaField('Autores', validators=[Optional()])
    producto_destacado = BooleanField('Producto Destacado', default=False)
    submit = SubmitField('Guardar')


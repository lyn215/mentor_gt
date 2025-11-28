from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Optional

class CongresoForm(FlaskForm):
    """Formulario para congresos y ponencias"""
    nombre_congreso = StringField('Nombre del Congreso', validators=[DataRequired(), Length(max=500)],
                                  render_kw={"placeholder": "Ej: Congreso Internacional de Computación"})
    titulo_ponencia = StringField('Título de la Ponencia', validators=[Optional(), Length(max=500)],
                                  render_kw={"placeholder": "Ej: Impacto de la IA en educación"})
    tipo = SelectField('Tipo', choices=[
        ('', 'Seleccionar'),
        ('Internacional', 'Internacional'),
        ('Nacional', 'Nacional'),
        ('Regional', 'Regional'),
        ('Local', 'Local')
    ], validators=[Optional()])
    fecha = DateField('Fecha', validators=[Optional()])
    pais = StringField('País', validators=[Optional(), Length(max=100)],
                      render_kw={"placeholder": "Ej: México"})
    ciudad = StringField('Ciudad', validators=[Optional(), Length(max=100)],
                        render_kw={"placeholder": "Ej: Ciudad de México"})
    modalidad = SelectField('Modalidad', choices=[
        ('', 'Seleccionar'),
        ('Presencial', 'Presencial'),
        ('Virtual', 'Virtual'),
        ('Híbrido', 'Híbrido')
    ], validators=[Optional()])
    tipo_participacion = SelectField('Tipo de Participación', choices=[
        ('', 'Seleccionar'),
        ('Ponente', 'Ponente'),
        ('Asistente', 'Asistente'),
        ('Organizador', 'Organizador'),
        ('Moderador', 'Moderador'),
        ('Panelista', 'Panelista')
    ], validators=[Optional()])
    producto_destacado = BooleanField('Producto Destacado')
    submit = SubmitField('Guardar')


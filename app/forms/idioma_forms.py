from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Optional

class IdiomaForm(FlaskForm):
    """Formulario para idiomas"""
    idioma = StringField('Idioma', validators=[DataRequired(), Length(max=100)], 
                         render_kw={"placeholder": "Ej: Inglés"})
    nivel = SelectField('Nivel', choices=[
        ('', 'Seleccionar nivel'),
        ('A1', 'Básico (A1)'),
        ('A2', 'Elemental (A2)'),
        ('B1', 'Intermedio (B1)'),
        ('B2', 'Intermedio Alto (B2)'),
        ('C1', 'Avanzado (C1)'),
        ('C2', 'Maestría (C2)'),
        ('Nativo', 'Nativo')
    ], validators=[DataRequired()])
    certificacion = StringField('Certificación', validators=[Optional(), Length(max=255)],
                                render_kw={"placeholder": "Ej: TOEFL 620 puntos"})
    certificado = BooleanField('¿Tiene certificado?')
    submit = SubmitField('Guardar')


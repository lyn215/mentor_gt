from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Optional

class TesisDirigidaForm(FlaskForm):
    """Formulario para tesis dirigidas"""
    titulo = StringField('Título de la Tesis', validators=[DataRequired(), Length(max=500)],
                        render_kw={"placeholder": "Ej: Sistema de predicción de rendimiento académico"})
    estudiante_nombre = StringField('Nombre del Estudiante', validators=[Optional(), Length(max=255)],
                                    render_kw={"placeholder": "Ej: Juan Pérez García"})
    nivel = SelectField('Nivel', choices=[
        ('', 'Seleccionar'),
        ('Licenciatura', 'Licenciatura'),
        ('Maestría', 'Maestría'),
        ('Doctorado', 'Doctorado'),
        ('Especialidad', 'Especialidad')
    ], validators=[Optional()])
    institucion = StringField('Institución', validators=[Optional(), Length(max=255)],
                             render_kw={"placeholder": "Ej: UTTEC"})
    clave_institucion = StringField('Clave de Institución', validators=[Optional(), Length(max=50)])
    pais = StringField('País', validators=[Optional(), Length(max=100)],
                      render_kw={"placeholder": "Ej: México"})
    fecha_inicio = DateField('Fecha de Inicio', validators=[Optional()])
    fecha_fin = DateField('Fecha de Fin', validators=[Optional()])
    estado = SelectField('Estado', choices=[
        ('', 'Seleccionar'),
        ('En proceso', 'En proceso'),
        ('Concluida', 'Concluida'),
        ('Abandonada', 'Abandonada')
    ], validators=[Optional()])
    submit = SubmitField('Guardar')


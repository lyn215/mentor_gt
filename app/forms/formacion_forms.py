from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Optional

class FormacionAcademicaForm(FlaskForm):
    nivel = SelectField('Nivel', choices=[
        ('licenciatura', 'Licenciatura'),
        ('maestria', 'Maestría'),
        ('doctorado', 'Doctorado'),
        ('especialidad', 'Especialidad')
    ], validators=[DataRequired()])
    grado_obtenido = StringField('Grado Obtenido', validators=[Optional(), Length(max=255)])
    institucion = StringField('Institución', validators=[Optional(), Length(max=255)])
    pais = StringField('País', validators=[Optional(), Length(max=100)])
    fecha_inicio = DateField('Fecha de Inicio', validators=[Optional()])
    fecha_fin = DateField('Fecha de Fin', validators=[Optional()])
    titulo_trabajo = TextAreaField('Título del Trabajo', validators=[Optional()])
    area_conocimiento = StringField('Área de Conocimiento', validators=[Optional(), Length(max=255)])
    campo = StringField('Campo', validators=[Optional(), Length(max=255)])
    disciplina = StringField('Disciplina', validators=[Optional(), Length(max=255)])
    subdisciplina = StringField('Subdisciplina', validators=[Optional(), Length(max=255)])
    submit = SubmitField('Guardar')


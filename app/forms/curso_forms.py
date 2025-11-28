from flask_wtf import FlaskForm
from wtforms import StringField, DateField, FloatField, BooleanField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Optional

class CursoImpartidoForm(FlaskForm):
    """Formulario para cursos impartidos"""
    nombre_curso = StringField('Nombre del Curso', validators=[DataRequired(), Length(max=255)],
                               render_kw={"placeholder": "Ej: Programación Avanzada"})
    programa_educativo = StringField('Programa Educativo', validators=[Optional(), Length(max=255)],
                                     render_kw={"placeholder": "Ej: Ingeniería en Sistemas"})
    nivel = SelectField('Nivel', choices=[
        ('', 'Seleccionar'),
        ('Licenciatura', 'Licenciatura'),
        ('Maestría', 'Maestría'),
        ('Doctorado', 'Doctorado'),
        ('Especialidad', 'Especialidad'),
        ('Técnico', 'Técnico'),
        ('Diplomado', 'Diplomado')
    ], validators=[Optional()])
    fecha_inicio = DateField('Fecha de Inicio', validators=[Optional()])
    fecha_fin = DateField('Fecha de Fin', validators=[Optional()])
    horas_semanales = FloatField('Horas Semanales', validators=[Optional()])
    snp = BooleanField('Sistema Nacional de Posgrados (SNP)')
    producto_destacado = BooleanField('Producto Destacado')
    submit = SubmitField('Guardar')


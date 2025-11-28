from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Optional

class EmpleoForm(FlaskForm):
    institucion = StringField('Institución', validators=[DataRequired(), Length(max=255)])
    puesto = StringField('Puesto', validators=[DataRequired(), Length(max=255)])
    tipo_contrato = SelectField('Tipo de Contrato', choices=[
        ('', 'Seleccionar'), ('indefinido', 'Indefinido'), ('temporal', 'Temporal'),
        ('honorarios', 'Honorarios'), ('otro', 'Otro')
    ], validators=[Optional()])
    fecha_inicio = DateField('Fecha de Inicio', validators=[Optional()])
    fecha_fin = DateField('Fecha de Fin', validators=[Optional()])
    actual = BooleanField('Empleo Actual', default=False)
    logros = TextAreaField('Logros', validators=[Optional()])
    area_adscripcion = StringField('Área de Adscripción', validators=[Optional(), Length(max=255)])
    submit = SubmitField('Guardar')


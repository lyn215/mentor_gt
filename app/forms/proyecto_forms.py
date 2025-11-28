from flask_wtf import FlaskForm
from wtforms import StringField, DateField, FloatField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Optional

class ProyectoInvestigacionForm(FlaskForm):
    """Formulario para proyectos de investigación"""
    nombre_proyecto = StringField('Nombre del Proyecto', validators=[DataRequired(), Length(max=500)],
                                  render_kw={"placeholder": "Ej: Sistema inteligente de monitoreo"})
    objetivo_general = TextAreaField('Objetivo General', validators=[Optional()],
                                     render_kw={"placeholder": "Descripción del objetivo principal", "rows": 3})
    descripcion = TextAreaField('Descripción', validators=[Optional()],
                               render_kw={"placeholder": "Descripción detallada del proyecto", "rows": 3})
    linea_investigacion = StringField('Línea de Investigación', validators=[Optional(), Length(max=255)],
                                      render_kw={"placeholder": "Ej: Inteligencia Artificial"})
    fecha_inicio = DateField('Fecha de Inicio', validators=[Optional()])
    fecha_fin = DateField('Fecha de Fin', validators=[Optional()])
    estado = SelectField('Estado', choices=[
        ('', 'Seleccionar'),
        ('En desarrollo', 'En desarrollo'),
        ('Concluido', 'Concluido'),
        ('Suspendido', 'Suspendido'),
        ('Cancelado', 'Cancelado')
    ], validators=[Optional()])
    financiamiento = StringField('Fuente de Financiamiento', validators=[Optional(), Length(max=255)],
                                 render_kw={"placeholder": "Ej: CONACYT, Fondos propios"})
    monto = FloatField('Monto ($)', validators=[Optional()])
    instituciones_colaboradoras = StringField('Instituciones Colaboradoras', validators=[Optional()],
                                              render_kw={"placeholder": "Ej: UNAM, IPN"})
    productos_obtenidos = TextAreaField('Productos Obtenidos', validators=[Optional()],
                                        render_kw={"placeholder": "Ej: Artículos, prototipos, patentes", "rows": 2})
    submit = SubmitField('Guardar')


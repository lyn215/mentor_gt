from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Optional

class DesarrolloTecnologicoForm(FlaskForm):
    """Formulario para desarrollos tecnológicos"""
    nombre = StringField('Nombre del Desarrollo', validators=[DataRequired(), Length(max=500)],
                        render_kw={"placeholder": "Ej: Plataforma de analítica educativa"})
    tipo = SelectField('Tipo', choices=[
        ('', 'Seleccionar'),
        ('Software', 'Software'),
        ('Hardware', 'Hardware'),
        ('Prototipo', 'Prototipo'),
        ('Patente', 'Patente'),
        ('Modelo de utilidad', 'Modelo de utilidad'),
        ('Diseño industrial', 'Diseño industrial')
    ], validators=[Optional()])
    nivel_madurez = SelectField('Nivel de Madurez (TRL)', choices=[
        ('', 'Seleccionar'),
        ('TRL 1', 'TRL 1 - Principios básicos'),
        ('TRL 2', 'TRL 2 - Concepto formulado'),
        ('TRL 3', 'TRL 3 - Prueba de concepto'),
        ('TRL 4', 'TRL 4 - Validación en laboratorio'),
        ('TRL 5', 'TRL 5 - Validación en entorno relevante'),
        ('TRL 6', 'TRL 6 - Demostración en entorno relevante'),
        ('TRL 7', 'TRL 7 - Demostración en entorno operativo'),
        ('TRL 8', 'TRL 8 - Sistema completo y calificado'),
        ('TRL 9', 'TRL 9 - Sistema probado en entorno real')
    ], validators=[Optional()])
    descripcion = TextAreaField('Descripción', validators=[Optional()],
                               render_kw={"placeholder": "Descripción del desarrollo tecnológico", "rows": 3})
    aplicacion_practica = TextAreaField('Aplicación Práctica', validators=[Optional()],
                                        render_kw={"placeholder": "¿Cómo se aplica en la práctica?", "rows": 2})
    otros_resultados = TextAreaField('Otros Resultados', validators=[Optional()],
                                     render_kw={"placeholder": "Resultados adicionales obtenidos", "rows": 2})
    producto_destacado = BooleanField('Producto Destacado')
    submit = SubmitField('Guardar')


# Forms package
from app.forms.auth_forms import LoginForm, RegistroForm
from app.forms.docente_forms import DocenteForm
from app.forms.formacion_forms import FormacionAcademicaForm
from app.forms.empleo_forms import EmpleoForm
from app.forms.articulo_forms import ArticuloForm

__all__ = [
    'LoginForm',
    'RegistroForm',
    'DocenteForm',
    'FormacionAcademicaForm',
    'EmpleoForm',
    'ArticuloForm'
]

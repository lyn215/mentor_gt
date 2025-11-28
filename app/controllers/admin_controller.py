from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models.user import User
from app.models.docente import Docente
from app.models.articulo import Articulo
from app.models.empleo import Empleo
from app.models.formacion_academica import FormacionAcademica
from app.utils.decorators import admin_required

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    """Dashboard del administrador"""
    total_docentes = Docente.query.count()
    total_usuarios = User.query.count()
    total_articulos = Articulo.query.count()
    total_empleos = Empleo.query.count()
    total_formaciones = FormacionAcademica.query.count()
    
    return render_template('admin/dashboard.html',
                         total_docentes=total_docentes,
                         total_usuarios=total_usuarios,
                         total_articulos=total_articulos,
                         total_empleos=total_empleos,
                         total_formaciones=total_formaciones)

@admin_bp.route('/docentes')
@login_required
@admin_required
def docentes():
    """Listar todos los docentes"""
    docentes_list = Docente.query.all()
    return render_template('admin/docentes.html', docentes=docentes_list)

@admin_bp.route('/docentes/<int:id>')
@login_required
@admin_required
def ver_docente(id):
    """Ver perfil completo de un docente"""
    docente = Docente.query.get_or_404(id)
    
    formaciones = docente.formaciones.all()
    empleos = docente.empleos.all()
    articulos = docente.articulos.all()
    idiomas = docente.idiomas.all()
    cursos = docente.cursos.all()
    proyectos = docente.proyectos.all()
    libros = docente.libros.all()
    congresos = docente.congresos.all()
    tesis = docente.tesis.all()
    desarrollos = docente.desarrollos.all()
    actividades = docente.actividades.all()
    
    return render_template('admin/ver_docente.html',
                         docente=docente,
                         formaciones=formaciones,
                         empleos=empleos,
                         articulos=articulos,
                         idiomas=idiomas,
                         cursos=cursos,
                         proyectos=proyectos,
                         libros=libros,
                         congresos=congresos,
                         tesis=tesis,
                         desarrollos=desarrollos,
                         actividades=actividades)

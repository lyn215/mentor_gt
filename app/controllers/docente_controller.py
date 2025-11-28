from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models.user import User
from app.models.docente import Docente
from app.models.formacion_academica import FormacionAcademica
from app.models.empleo import Empleo
from app.models.articulo import Articulo
from app.models.idioma import Idioma
from app.models.curso_impartido import CursoImpartido
from app.models.proyecto_investigacion import ProyectoInvestigacion
from app.models.libro import Libro
from app.models.congreso import Congreso
from app.models.tesis_dirigida import TesisDirigida
from app.models.desarrollo_tecnologico import DesarrolloTecnologico
from app.forms.docente_forms import DocenteForm
from app.forms.formacion_forms import FormacionAcademicaForm
from app.forms.empleo_forms import EmpleoForm
from app.forms.articulo_forms import ArticuloForm
from app.forms.idioma_forms import IdiomaForm
from app.forms.curso_forms import CursoImpartidoForm
from app.forms.proyecto_forms import ProyectoInvestigacionForm
from app.forms.libro_forms import LibroForm
from app.forms.congreso_forms import CongresoForm
from app.forms.tesis_forms import TesisDirigidaForm
from app.forms.desarrollo_forms import DesarrolloTecnologicoForm
from app.utils.decorators import docente_required

docente_bp = Blueprint('docente', __name__)

@docente_bp.route('/dashboard')
@login_required
@docente_required
def dashboard():
    """Dashboard del docente"""
    docente = Docente.query.filter_by(user_id=current_user.id).first()
    
    if not docente:
        flash('Por favor completa tu perfil primero', 'info')
        return redirect(url_for('docente.perfil'))
    
    # Estadísticas
    total_formaciones = FormacionAcademica.query.filter_by(docente_id=docente.id).count()
    total_empleos = Empleo.query.filter_by(docente_id=docente.id).count()
    total_articulos = Articulo.query.filter_by(docente_id=docente.id).count()
    total_cursos = CursoImpartido.query.filter_by(docente_id=docente.id).count()
    total_proyectos = ProyectoInvestigacion.query.filter_by(docente_id=docente.id).count()
    total_desarrollos = DesarrolloTecnologico.query.filter_by(docente_id=docente.id).count()
    
    # Actividades recientes
    actividades_recientes = []
    if total_articulos > 0:
        ultimo_articulo = Articulo.query.filter_by(docente_id=docente.id).order_by(Articulo.id.desc()).first()
        if ultimo_articulo:
            actividades_recientes.append({
                'titulo': 'Artículo publicado',
                'fecha': 'Hace 2 días',
                'color': '#0d6efd'
            })
    
    if total_proyectos > 0:
        ultimo_proyecto = ProyectoInvestigacion.query.filter_by(docente_id=docente.id).order_by(ProyectoInvestigacion.id.desc()).first()
        if ultimo_proyecto:
            actividades_recientes.append({
                'titulo': 'Proyecto actualizado',
                'fecha': 'Hace 5 días',
                'color': '#198754'
            })
    
    return render_template('docente/dashboard.html',
                         docente=docente,
                         total_formaciones=total_formaciones,
                         total_empleos=total_empleos,
                         total_articulos=total_articulos,
                         total_cursos=total_cursos,
                         total_proyectos=total_proyectos,
                         total_desarrollos=total_desarrollos,
                         actividades_recientes=actividades_recientes)

@docente_bp.route('/perfil', methods=['GET', 'POST'])
@login_required
@docente_required
def perfil():
    """Gestionar perfil del docente"""
    docente = Docente.query.filter_by(user_id=current_user.id).first()
    form = DocenteForm(obj=docente) if docente else DocenteForm()
    
    if form.validate_on_submit():
        if not docente:
            docente = Docente(user_id=current_user.id)
            db.session.add(docente)
        
        form.populate_obj(docente)
        db.session.commit()
        flash('Perfil actualizado exitosamente', 'success')
        return redirect(url_for('docente.perfil'))
    
    # Obtener datos relacionados para las pestañas
    formaciones = []
    empleos = []
    articulos = []
    idiomas_list = []
    cursos_list = []
    proyectos_list = []
    libros_list = []
    congresos_list = []
    tesis_list = []
    desarrollos_list = []
    
    if docente:
        formaciones = FormacionAcademica.query.filter_by(docente_id=docente.id).order_by(FormacionAcademica.fecha_fin.desc()).all()
        empleos = Empleo.query.filter_by(docente_id=docente.id).order_by(Empleo.fecha_inicio.desc()).all()
        articulos = Articulo.query.filter_by(docente_id=docente.id).order_by(Articulo.anio.desc()).all()
        idiomas_list = Idioma.query.filter_by(docente_id=docente.id).all()
        cursos_list = CursoImpartido.query.filter_by(docente_id=docente.id).all()
        proyectos_list = ProyectoInvestigacion.query.filter_by(docente_id=docente.id).all()
        libros_list = Libro.query.filter_by(docente_id=docente.id).all()
        congresos_list = Congreso.query.filter_by(docente_id=docente.id).all()
        tesis_list = TesisDirigida.query.filter_by(docente_id=docente.id).all()
        desarrollos_list = DesarrolloTecnologico.query.filter_by(docente_id=docente.id).all()
    
    # Formularios para modales
    idioma_form = IdiomaForm()
    curso_form = CursoImpartidoForm()
    proyecto_form = ProyectoInvestigacionForm()
    libro_form = LibroForm()
    congreso_form = CongresoForm()
    tesis_form = TesisDirigidaForm()
    desarrollo_form = DesarrolloTecnologicoForm()
    
    return render_template('docente/perfil.html', 
                          form=form, 
                          docente=docente,
                          formaciones=formaciones,
                          empleos=empleos,
                          articulos=articulos,
                          idiomas=idiomas_list,
                          cursos=cursos_list,
                          proyectos=proyectos_list,
                          libros=libros_list,
                          congresos=congresos_list,
                          tesis=tesis_list,
                          desarrollos=desarrollos_list,
                          idioma_form=idioma_form,
                          curso_form=curso_form,
                          proyecto_form=proyecto_form,
                          libro_form=libro_form,
                          congreso_form=congreso_form,
                          tesis_form=tesis_form,
                          desarrollo_form=desarrollo_form)

@docente_bp.route('/formacion', methods=['GET', 'POST'])
@login_required
@docente_required
def formacion():
    """Listar y crear formación académica"""
    docente = Docente.query.filter_by(user_id=current_user.id).first()
    if not docente:
        flash('Por favor completa tu perfil primero', 'warning')
        return redirect(url_for('docente.perfil'))
    
    formaciones = FormacionAcademica.query.filter_by(docente_id=docente.id).all()
    return render_template('docente/formacion.html', formaciones=formaciones)

@docente_bp.route('/formacion/nueva', methods=['GET', 'POST'])
@login_required
@docente_required
def nueva_formacion():
    """Crear nueva formación académica"""
    docente = Docente.query.filter_by(user_id=current_user.id).first()
    if not docente:
        flash('Por favor completa tu perfil primero', 'warning')
        return redirect(url_for('docente.perfil'))
    
    form = FormacionAcademicaForm()
    if form.validate_on_submit():
        formacion = FormacionAcademica(docente_id=docente.id)
        form.populate_obj(formacion)
        db.session.add(formacion)
        db.session.commit()
        flash('Formación académica agregada exitosamente', 'success')
        return redirect(url_for('docente.formacion'))
    
    return render_template('docente/nueva_formacion.html', form=form)

@docente_bp.route('/formacion/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@docente_required
def editar_formacion(id):
    """Editar formación académica"""
    docente = Docente.query.filter_by(user_id=current_user.id).first()
    formacion = FormacionAcademica.query.get_or_404(id)
    
    if formacion.docente_id != docente.id:
        flash('No tienes permisos para editar esto', 'danger')
        return redirect(url_for('docente.formacion'))
    
    form = FormacionAcademicaForm(obj=formacion)
    if form.validate_on_submit():
        form.populate_obj(formacion)
        db.session.commit()
        flash('Formación académica actualizada exitosamente', 'success')
        return redirect(url_for('docente.formacion'))
    
    return render_template('docente/editar_formacion.html', form=form, formacion=formacion)

@docente_bp.route('/formacion/<int:id>/eliminar', methods=['POST'])
@login_required
@docente_required
def eliminar_formacion(id):
    """Eliminar formación académica"""
    docente = Docente.query.filter_by(user_id=current_user.id).first()
    formacion = FormacionAcademica.query.get_or_404(id)
    
    if formacion.docente_id != docente.id:
        flash('No tienes permisos para eliminar esto', 'danger')
        return redirect(url_for('docente.formacion'))
    
    db.session.delete(formacion)
    db.session.commit()
    flash('Formación académica eliminada exitosamente', 'success')
    return redirect(url_for('docente.formacion'))

@docente_bp.route('/empleos')
@login_required
@docente_required
def empleos():
    """Listar empleos"""
    docente = Docente.query.filter_by(user_id=current_user.id).first()
    if not docente:
        flash('Por favor completa tu perfil primero', 'warning')
        return redirect(url_for('docente.perfil'))
    
    empleos_list = Empleo.query.filter_by(docente_id=docente.id).all()
    return render_template('docente/empleos.html', empleos=empleos_list)

@docente_bp.route('/empleos/nuevo', methods=['GET', 'POST'])
@login_required
@docente_required
def nuevo_empleo():
    """Crear nuevo empleo"""
    docente = Docente.query.filter_by(user_id=current_user.id).first()
    if not docente:
        flash('Por favor completa tu perfil primero', 'warning')
        return redirect(url_for('docente.perfil'))
    
    form = EmpleoForm()
    if form.validate_on_submit():
        empleo = Empleo(docente_id=docente.id)
        form.populate_obj(empleo)
        db.session.add(empleo)
        db.session.commit()
        flash('Empleo agregado exitosamente', 'success')
        return redirect(url_for('docente.empleos'))
    
    return render_template('docente/nuevo_empleo.html', form=form)

@docente_bp.route('/empleos/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@docente_required
def editar_empleo(id):
    """Editar empleo"""
    docente = Docente.query.filter_by(user_id=current_user.id).first()
    empleo = Empleo.query.get_or_404(id)
    
    if empleo.docente_id != docente.id:
        flash('No tienes permisos para editar esto', 'danger')
        return redirect(url_for('docente.empleos'))
    
    form = EmpleoForm(obj=empleo)
    if form.validate_on_submit():
        form.populate_obj(empleo)
        db.session.commit()
        flash('Empleo actualizado exitosamente', 'success')
        return redirect(url_for('docente.empleos'))
    
    return render_template('docente/editar_empleo.html', form=form, empleo=empleo)

@docente_bp.route('/empleos/<int:id>/eliminar', methods=['POST'])
@login_required
@docente_required
def eliminar_empleo(id):
    """Eliminar empleo"""
    docente = Docente.query.filter_by(user_id=current_user.id).first()
    empleo = Empleo.query.get_or_404(id)
    
    if empleo.docente_id != docente.id:
        flash('No tienes permisos para eliminar esto', 'danger')
        return redirect(url_for('docente.empleos'))
    
    db.session.delete(empleo)
    db.session.commit()
    flash('Empleo eliminado exitosamente', 'success')
    return redirect(url_for('docente.empleos'))

@docente_bp.route('/articulos')
@login_required
@docente_required
def articulos():
    """Listar artículos"""
    docente = Docente.query.filter_by(user_id=current_user.id).first()
    if not docente:
        flash('Por favor completa tu perfil primero', 'warning')
        return redirect(url_for('docente.perfil'))
    
    articulos_list = Articulo.query.filter_by(docente_id=docente.id).all()
    return render_template('docente/articulos.html', articulos=articulos_list)

@docente_bp.route('/articulos/nuevo', methods=['GET', 'POST'])
@login_required
@docente_required
def nuevo_articulo():
    """Crear nuevo artículo"""
    docente = Docente.query.filter_by(user_id=current_user.id).first()
    if not docente:
        flash('Por favor completa tu perfil primero', 'warning')
        return redirect(url_for('docente.perfil'))
    
    form = ArticuloForm()
    if form.validate_on_submit():
        articulo = Articulo(docente_id=docente.id)
        form.populate_obj(articulo)
        db.session.add(articulo)
        db.session.commit()
        flash('Artículo agregado exitosamente', 'success')
        return redirect(url_for('docente.articulos'))
    
    return render_template('docente/nuevo_articulo.html', form=form)

@docente_bp.route('/articulos/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@docente_required
def editar_articulo(id):
    """Editar artículo"""
    docente = Docente.query.filter_by(user_id=current_user.id).first()
    articulo = Articulo.query.get_or_404(id)
    
    if articulo.docente_id != docente.id:
        flash('No tienes permisos para editar esto', 'danger')
        return redirect(url_for('docente.articulos'))
    
    form = ArticuloForm(obj=articulo)
    if form.validate_on_submit():
        form.populate_obj(articulo)
        db.session.commit()
        flash('Artículo actualizado exitosamente', 'success')
        return redirect(url_for('docente.articulos'))
    
    return render_template('docente/editar_articulo.html', form=form, articulo=articulo)

@docente_bp.route('/articulos/<int:id>/eliminar', methods=['POST'])
@login_required
@docente_required
def eliminar_articulo(id):
    """Eliminar artículo"""
    docente = Docente.query.filter_by(user_id=current_user.id).first()
    articulo = Articulo.query.get_or_404(id)
    
    if articulo.docente_id != docente.id:
        flash('No tienes permisos para eliminar esto', 'danger')
        return redirect(url_for('docente.articulos'))
    
    db.session.delete(articulo)
    db.session.commit()
    flash('Artículo eliminado exitosamente', 'success')
    return redirect(url_for('docente.articulos'))

# ==================== IDIOMAS ====================

@docente_bp.route('/idiomas')
@login_required
@docente_required
def idiomas():
    """Listar idiomas"""
    docente = Docente.query.filter_by(user_id=current_user.id).first()
    if not docente:
        flash('Por favor completa tu perfil primero', 'warning')
        return redirect(url_for('docente.perfil'))
    
    idiomas_list = Idioma.query.filter_by(docente_id=docente.id).all()
    form = IdiomaForm()
    return render_template('docente/idiomas.html', idiomas=idiomas_list, form=form)

@docente_bp.route('/idiomas/nuevo', methods=['GET', 'POST'])
@login_required
@docente_required
def nuevo_idioma():
    """Crear nuevo idioma"""
    docente = Docente.query.filter_by(user_id=current_user.id).first()
    if not docente:
        flash('Por favor completa tu perfil primero', 'warning')
        return redirect(url_for('docente.perfil'))
    
    form = IdiomaForm()
    if form.validate_on_submit():
        idioma = Idioma(docente_id=docente.id)
        form.populate_obj(idioma)
        db.session.add(idioma)
        db.session.commit()
        flash('Idioma agregado exitosamente', 'success')
        return redirect(url_for('docente.idiomas'))
    
    return render_template('docente/nuevo_idioma.html', form=form)

@docente_bp.route('/idiomas/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@docente_required
def editar_idioma(id):
    """Editar idioma"""
    docente = Docente.query.filter_by(user_id=current_user.id).first()
    idioma = Idioma.query.get_or_404(id)
    
    if idioma.docente_id != docente.id:
        flash('No tienes permisos para editar esto', 'danger')
        return redirect(url_for('docente.idiomas'))
    
    form = IdiomaForm(obj=idioma)
    if form.validate_on_submit():
        form.populate_obj(idioma)
        db.session.commit()
        flash('Idioma actualizado exitosamente', 'success')
        return redirect(url_for('docente.idiomas'))
    
    return render_template('docente/editar_idioma.html', form=form, idioma=idioma)

@docente_bp.route('/idiomas/<int:id>/eliminar', methods=['POST'])
@login_required
@docente_required
def eliminar_idioma(id):
    """Eliminar idioma"""
    docente = Docente.query.filter_by(user_id=current_user.id).first()
    idioma = Idioma.query.get_or_404(id)
    
    if idioma.docente_id != docente.id:
        flash('No tienes permisos para eliminar esto', 'danger')
        return redirect(url_for('docente.idiomas'))
    
    db.session.delete(idioma)
    db.session.commit()
    flash('Idioma eliminado exitosamente', 'success')
    return redirect(url_for('docente.idiomas'))

# ==================== CURSOS IMPARTIDOS ====================

@docente_bp.route('/cursos')
@login_required
@docente_required
def cursos():
    """Listar cursos"""
    docente = Docente.query.filter_by(user_id=current_user.id).first()
    if not docente:
        return redirect(url_for('docente.perfil'))
    cursos_list = CursoImpartido.query.filter_by(docente_id=docente.id).all()
    return render_template('docente/cursos.html', cursos=cursos_list)

@docente_bp.route('/cursos/nuevo', methods=['GET', 'POST'])
@login_required
@docente_required
def nuevo_curso():
    docente = Docente.query.filter_by(user_id=current_user.id).first()
    if not docente:
        return redirect(url_for('docente.perfil'))
    form = CursoImpartidoForm()
    if form.validate_on_submit():
        curso = CursoImpartido(docente_id=docente.id)
        form.populate_obj(curso)
        db.session.add(curso)
        db.session.commit()
        flash('Curso agregado exitosamente', 'success')
        return redirect(url_for('docente.cursos'))
    return render_template('docente/nuevo_curso.html', form=form)

@docente_bp.route('/cursos/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@docente_required
def editar_curso(id):
    docente = Docente.query.filter_by(user_id=current_user.id).first()
    curso = CursoImpartido.query.get_or_404(id)
    if curso.docente_id != docente.id:
        return redirect(url_for('docente.cursos'))
    form = CursoImpartidoForm(obj=curso)
    if form.validate_on_submit():
        form.populate_obj(curso)
        db.session.commit()
        flash('Curso actualizado', 'success')
        return redirect(url_for('docente.cursos'))
    return render_template('docente/editar_curso.html', form=form, curso=curso)

@docente_bp.route('/cursos/<int:id>/eliminar', methods=['POST'])
@login_required
@docente_required
def eliminar_curso(id):
    docente = Docente.query.filter_by(user_id=current_user.id).first()
    curso = CursoImpartido.query.get_or_404(id)
    if curso.docente_id != docente.id:
        return redirect(url_for('docente.cursos'))
    db.session.delete(curso)
    db.session.commit()
    flash('Curso eliminado', 'success')
    return redirect(url_for('docente.cursos'))

# ==================== PROYECTOS ====================

@docente_bp.route('/proyectos')
@login_required
@docente_required
def proyectos():
    docente = Docente.query.filter_by(user_id=current_user.id).first()
    if not docente:
        return redirect(url_for('docente.perfil'))
    proyectos_list = ProyectoInvestigacion.query.filter_by(docente_id=docente.id).all()
    return render_template('docente/proyectos.html', proyectos=proyectos_list)

@docente_bp.route('/proyectos/nuevo', methods=['GET', 'POST'])
@login_required
@docente_required
def nuevo_proyecto():
    docente = Docente.query.filter_by(user_id=current_user.id).first()
    if not docente:
        return redirect(url_for('docente.perfil'))
    form = ProyectoInvestigacionForm()
    if form.validate_on_submit():
        proyecto = ProyectoInvestigacion(docente_id=docente.id)
        form.populate_obj(proyecto)
        db.session.add(proyecto)
        db.session.commit()
        flash('Proyecto agregado exitosamente', 'success')
        return redirect(url_for('docente.proyectos'))
    return render_template('docente/nuevo_proyecto.html', form=form)

@docente_bp.route('/proyectos/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@docente_required
def editar_proyecto(id):
    docente = Docente.query.filter_by(user_id=current_user.id).first()
    proyecto = ProyectoInvestigacion.query.get_or_404(id)
    if proyecto.docente_id != docente.id:
        return redirect(url_for('docente.proyectos'))
    form = ProyectoInvestigacionForm(obj=proyecto)
    if form.validate_on_submit():
        form.populate_obj(proyecto)
        db.session.commit()
        flash('Proyecto actualizado', 'success')
        return redirect(url_for('docente.proyectos'))
    return render_template('docente/editar_proyecto.html', form=form, proyecto=proyecto)

@docente_bp.route('/proyectos/<int:id>/eliminar', methods=['POST'])
@login_required
@docente_required
def eliminar_proyecto(id):
    docente = Docente.query.filter_by(user_id=current_user.id).first()
    proyecto = ProyectoInvestigacion.query.get_or_404(id)
    if proyecto.docente_id != docente.id:
        return redirect(url_for('docente.proyectos'))
    db.session.delete(proyecto)
    db.session.commit()
    flash('Proyecto eliminado', 'success')
    return redirect(url_for('docente.proyectos'))

# ==================== LIBROS ====================

@docente_bp.route('/libros')
@login_required
@docente_required
def libros():
    docente = Docente.query.filter_by(user_id=current_user.id).first()
    if not docente:
        return redirect(url_for('docente.perfil'))
    libros_list = Libro.query.filter_by(docente_id=docente.id).all()
    return render_template('docente/libros.html', libros=libros_list)

@docente_bp.route('/libros/nuevo', methods=['GET', 'POST'])
@login_required
@docente_required
def nuevo_libro():
    docente = Docente.query.filter_by(user_id=current_user.id).first()
    if not docente:
        return redirect(url_for('docente.perfil'))
    form = LibroForm()
    if form.validate_on_submit():
        libro = Libro(docente_id=docente.id)
        form.populate_obj(libro)
        db.session.add(libro)
        db.session.commit()
        flash('Libro agregado exitosamente', 'success')
        return redirect(url_for('docente.libros'))
    return render_template('docente/nuevo_libro.html', form=form)

@docente_bp.route('/libros/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@docente_required
def editar_libro(id):
    docente = Docente.query.filter_by(user_id=current_user.id).first()
    libro = Libro.query.get_or_404(id)
    if libro.docente_id != docente.id:
        return redirect(url_for('docente.libros'))
    form = LibroForm(obj=libro)
    if form.validate_on_submit():
        form.populate_obj(libro)
        db.session.commit()
        flash('Libro actualizado', 'success')
        return redirect(url_for('docente.libros'))
    return render_template('docente/editar_libro.html', form=form, libro=libro)

@docente_bp.route('/libros/<int:id>/eliminar', methods=['POST'])
@login_required
@docente_required
def eliminar_libro(id):
    docente = Docente.query.filter_by(user_id=current_user.id).first()
    libro = Libro.query.get_or_404(id)
    if libro.docente_id != docente.id:
        return redirect(url_for('docente.libros'))
    db.session.delete(libro)
    db.session.commit()
    flash('Libro eliminado', 'success')
    return redirect(url_for('docente.libros'))

# ==================== CONGRESOS ====================

@docente_bp.route('/congresos')
@login_required
@docente_required
def congresos():
    docente = Docente.query.filter_by(user_id=current_user.id).first()
    if not docente:
        return redirect(url_for('docente.perfil'))
    congresos_list = Congreso.query.filter_by(docente_id=docente.id).all()
    return render_template('docente/congresos.html', congresos=congresos_list)

@docente_bp.route('/congresos/nuevo', methods=['GET', 'POST'])
@login_required
@docente_required
def nuevo_congreso():
    docente = Docente.query.filter_by(user_id=current_user.id).first()
    if not docente:
        return redirect(url_for('docente.perfil'))
    form = CongresoForm()
    if form.validate_on_submit():
        congreso = Congreso(docente_id=docente.id)
        form.populate_obj(congreso)
        db.session.add(congreso)
        db.session.commit()
        flash('Congreso agregado exitosamente', 'success')
        return redirect(url_for('docente.congresos'))
    return render_template('docente/nuevo_congreso.html', form=form)

@docente_bp.route('/congresos/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@docente_required
def editar_congreso(id):
    docente = Docente.query.filter_by(user_id=current_user.id).first()
    congreso = Congreso.query.get_or_404(id)
    if congreso.docente_id != docente.id:
        return redirect(url_for('docente.congresos'))
    form = CongresoForm(obj=congreso)
    if form.validate_on_submit():
        form.populate_obj(congreso)
        db.session.commit()
        flash('Congreso actualizado', 'success')
        return redirect(url_for('docente.congresos'))
    return render_template('docente/editar_congreso.html', form=form, congreso=congreso)

@docente_bp.route('/congresos/<int:id>/eliminar', methods=['POST'])
@login_required
@docente_required
def eliminar_congreso(id):
    docente = Docente.query.filter_by(user_id=current_user.id).first()
    congreso = Congreso.query.get_or_404(id)
    if congreso.docente_id != docente.id:
        return redirect(url_for('docente.congresos'))
    db.session.delete(congreso)
    db.session.commit()
    flash('Congreso eliminado', 'success')
    return redirect(url_for('docente.congresos'))

# ==================== TESIS DIRIGIDAS ====================

@docente_bp.route('/tesis')
@login_required
@docente_required
def tesis():
    docente = Docente.query.filter_by(user_id=current_user.id).first()
    if not docente:
        return redirect(url_for('docente.perfil'))
    tesis_list = TesisDirigida.query.filter_by(docente_id=docente.id).all()
    return render_template('docente/tesis.html', tesis=tesis_list)

@docente_bp.route('/tesis/nueva', methods=['GET', 'POST'])
@login_required
@docente_required
def nueva_tesis():
    docente = Docente.query.filter_by(user_id=current_user.id).first()
    if not docente:
        return redirect(url_for('docente.perfil'))
    form = TesisDirigidaForm()
    if form.validate_on_submit():
        tesis = TesisDirigida(docente_id=docente.id)
        form.populate_obj(tesis)
        db.session.add(tesis)
        db.session.commit()
        flash('Tesis agregada exitosamente', 'success')
        return redirect(url_for('docente.tesis'))
    return render_template('docente/nueva_tesis.html', form=form)

@docente_bp.route('/tesis/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@docente_required
def editar_tesis(id):
    docente = Docente.query.filter_by(user_id=current_user.id).first()
    tesis = TesisDirigida.query.get_or_404(id)
    if tesis.docente_id != docente.id:
        return redirect(url_for('docente.tesis'))
    form = TesisDirigidaForm(obj=tesis)
    if form.validate_on_submit():
        form.populate_obj(tesis)
        db.session.commit()
        flash('Tesis actualizada', 'success')
        return redirect(url_for('docente.tesis'))
    return render_template('docente/editar_tesis.html', form=form, tesis=tesis)

@docente_bp.route('/tesis/<int:id>/eliminar', methods=['POST'])
@login_required
@docente_required
def eliminar_tesis(id):
    docente = Docente.query.filter_by(user_id=current_user.id).first()
    tesis = TesisDirigida.query.get_or_404(id)
    if tesis.docente_id != docente.id:
        return redirect(url_for('docente.tesis'))
    db.session.delete(tesis)
    db.session.commit()
    flash('Tesis eliminada', 'success')
    return redirect(url_for('docente.tesis'))

# ==================== DESARROLLOS TECNOLÓGICOS ====================

@docente_bp.route('/desarrollos')
@login_required
@docente_required
def desarrollos():
    docente = Docente.query.filter_by(user_id=current_user.id).first()
    if not docente:
        return redirect(url_for('docente.perfil'))
    desarrollos_list = DesarrolloTecnologico.query.filter_by(docente_id=docente.id).all()
    return render_template('docente/desarrollos.html', desarrollos=desarrollos_list)

@docente_bp.route('/desarrollos/nuevo', methods=['GET', 'POST'])
@login_required
@docente_required
def nuevo_desarrollo():
    docente = Docente.query.filter_by(user_id=current_user.id).first()
    if not docente:
        return redirect(url_for('docente.perfil'))
    form = DesarrolloTecnologicoForm()
    if form.validate_on_submit():
        desarrollo = DesarrolloTecnologico(docente_id=docente.id)
        form.populate_obj(desarrollo)
        db.session.add(desarrollo)
        db.session.commit()
        flash('Desarrollo agregado exitosamente', 'success')
        return redirect(url_for('docente.desarrollos'))
    return render_template('docente/nuevo_desarrollo.html', form=form)

@docente_bp.route('/desarrollos/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@docente_required
def editar_desarrollo(id):
    docente = Docente.query.filter_by(user_id=current_user.id).first()
    desarrollo = DesarrolloTecnologico.query.get_or_404(id)
    if desarrollo.docente_id != docente.id:
        return redirect(url_for('docente.desarrollos'))
    form = DesarrolloTecnologicoForm(obj=desarrollo)
    if form.validate_on_submit():
        form.populate_obj(desarrollo)
        db.session.commit()
        flash('Desarrollo actualizado', 'success')
        return redirect(url_for('docente.desarrollos'))
    return render_template('docente/editar_desarrollo.html', form=form, desarrollo=desarrollo)

@docente_bp.route('/desarrollos/<int:id>/eliminar', methods=['POST'])
@login_required
@docente_required
def eliminar_desarrollo(id):
    docente = Docente.query.filter_by(user_id=current_user.id).first()
    desarrollo = DesarrolloTecnologico.query.get_or_404(id)
    if desarrollo.docente_id != docente.id:
        return redirect(url_for('docente.desarrollos'))
    db.session.delete(desarrollo)
    db.session.commit()
    flash('Desarrollo eliminado', 'success')
    return redirect(url_for('docente.desarrollos'))


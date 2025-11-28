from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models.publicacion import Publicacion
# from app.forms.publicacion_forms import PublicacionForm  # Comentado - formulario eliminado
from app.utils.decorators import profesor_required

publicacion_bp = Blueprint('publicacion', __name__)

@publicacion_bp.route('/')
@login_required
@profesor_required
def listar():
    publicaciones = Publicacion.query.filter_by(usuario_id=current_user.id)\
        .order_by(Publicacion.año.desc()).all()
    return render_template('profesor/publicaciones.html', publicaciones=publicaciones)

@publicacion_bp.route('/nueva', methods=['GET', 'POST'])
@login_required
@profesor_required
def nueva():
    # Ruta temporalmente deshabilitada - formulario eliminado
    flash('Funcionalidad temporalmente deshabilitada', 'info')
    return redirect(url_for('publicacion.listar'))

@publicacion_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@profesor_required
def editar(id):
    # Ruta temporalmente deshabilitada - formulario eliminado
    flash('Funcionalidad temporalmente deshabilitada', 'info')
    return redirect(url_for('publicacion.listar'))

@publicacion_bp.route('/<int:id>/eliminar', methods=['POST'])
@login_required
@profesor_required
def eliminar(id):
    publicacion = Publicacion.query.get_or_404(id)
    if publicacion.usuario_id != current_user.id:
        flash('No tienes permisos para eliminar esta publicación', 'danger')
        return redirect(url_for('publicacion.listar'))
    
    db.session.delete(publicacion)
    db.session.commit()
    flash('Publicación eliminada exitosamente', 'success')
    return redirect(url_for('publicacion.listar'))


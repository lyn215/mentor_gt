from app import db

class ProyectoInvestigacion(db.Model):
    __tablename__ = 'proyectos_investigacion'
    
    id = db.Column(db.Integer, primary_key=True)
    docente_id = db.Column(db.Integer, db.ForeignKey('docentes.id', ondelete='CASCADE'), nullable=False)
    nombre_proyecto = db.Column(db.String(255), nullable=False)
    objetivo_general = db.Column(db.Text)
    descripcion = db.Column(db.Text)
    linea_investigacion = db.Column(db.String(255))
    fecha_inicio = db.Column(db.Date)
    fecha_fin = db.Column(db.Date)
    estado = db.Column(db.String(50))
    financiamiento = db.Column(db.String(255))
    monto = db.Column(db.Float)
    instituciones_colaboradoras = db.Column(db.Text)
    productos_obtenidos = db.Column(db.Text)
    
    def __repr__(self):
        return f'<ProyectoInvestigacion {self.nombre_proyecto}>'


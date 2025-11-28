from app import db

class TesisDirigida(db.Model):
    __tablename__ = 'tesis_dirigidas'
    
    id = db.Column(db.Integer, primary_key=True)
    docente_id = db.Column(db.Integer, db.ForeignKey('docentes.id', ondelete='CASCADE'), nullable=False)
    titulo = db.Column(db.String(500), nullable=False)
    nivel = db.Column(db.String(50))
    institucion = db.Column(db.String(255))
    fecha_inicio = db.Column(db.Date)
    fecha_fin = db.Column(db.Date)
    estado = db.Column(db.String(50))
    estudiante_nombre = db.Column(db.String(255))
    clave_institucion = db.Column(db.String(100))
    pais = db.Column(db.String(100))
    
    def __repr__(self):
        return f'<TesisDirigida {self.titulo[:50]}>'


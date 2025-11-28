from app import db

class ActividadGeneral(db.Model):
    __tablename__ = 'actividades_generales'
    
    id = db.Column(db.Integer, primary_key=True)
    docente_id = db.Column(db.Integer, db.ForeignKey('docentes.id', ondelete='CASCADE'), nullable=False)
    categoria = db.Column(db.String(50), nullable=False)  # idioma, premio, congreso, evaluacion, divulgacion, institucional
    # Nota: El CHECK constraint se maneja a nivel de aplicación o migración
    titulo = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.Text)
    fecha = db.Column(db.Date)
    archivo = db.Column(db.String(500))
    
    def __repr__(self):
        return f'<ActividadGeneral {self.titulo}>'


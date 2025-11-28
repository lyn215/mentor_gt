from app import db

class Empleo(db.Model):
    __tablename__ = 'empleos'
    
    id = db.Column(db.Integer, primary_key=True)
    docente_id = db.Column(db.Integer, db.ForeignKey('docentes.id', ondelete='CASCADE'), nullable=False)
    institucion = db.Column(db.String(255), nullable=False)
    puesto = db.Column(db.String(255), nullable=False)
    tipo_contrato = db.Column(db.String(100))
    fecha_inicio = db.Column(db.Date)
    fecha_fin = db.Column(db.Date)
    actual = db.Column(db.Boolean, default=False)
    logros = db.Column(db.Text)
    area_adscripcion = db.Column(db.String(255))
    
    def __repr__(self):
        return f'<Empleo {self.puesto} en {self.institucion}>'


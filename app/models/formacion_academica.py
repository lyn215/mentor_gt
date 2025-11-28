from app import db

class FormacionAcademica(db.Model):
    __tablename__ = 'formacion_academica'
    
    id = db.Column(db.Integer, primary_key=True)
    docente_id = db.Column(db.Integer, db.ForeignKey('docentes.id', ondelete='CASCADE'), nullable=False)
    nivel = db.Column(db.String(50), nullable=False)
    grado_obtenido = db.Column(db.String(255))
    institucion = db.Column(db.String(255))
    pais = db.Column(db.String(100))
    fecha_inicio = db.Column(db.Date)
    fecha_fin = db.Column(db.Date)
    titulo_trabajo = db.Column(db.Text)
    area_conocimiento = db.Column(db.String(255))
    campo = db.Column(db.String(255))
    disciplina = db.Column(db.String(255))
    subdisciplina = db.Column(db.String(255))
    
    def __repr__(self):
        return f'<FormacionAcademica {self.grado_obtenido}>'


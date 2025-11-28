from app import db

class CursoImpartido(db.Model):
    __tablename__ = 'cursos_impartidos'
    
    id = db.Column(db.Integer, primary_key=True)
    docente_id = db.Column(db.Integer, db.ForeignKey('docentes.id', ondelete='CASCADE'), nullable=False)
    nombre_curso = db.Column(db.String(255), nullable=False)
    programa_educativo = db.Column(db.String(255))
    nivel = db.Column(db.String(50))
    fecha_inicio = db.Column(db.Date)
    fecha_fin = db.Column(db.Date)
    horas_semanales = db.Column(db.Float)
    snp = db.Column(db.Boolean, default=False)
    producto_destacado = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f'<CursoImpartido {self.nombre_curso}>'


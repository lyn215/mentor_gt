from app import db

class Idioma(db.Model):
    __tablename__ = 'idiomas'
    
    id = db.Column(db.Integer, primary_key=True)
    docente_id = db.Column(db.Integer, db.ForeignKey('docentes.id', ondelete='CASCADE'), nullable=False)
    idioma = db.Column(db.String(100), nullable=False)
    nivel = db.Column(db.String(50))
    certificacion = db.Column(db.String(255))
    certificado = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f'<Idioma {self.idioma}>'


from app import db

class Congreso(db.Model):
    __tablename__ = 'congresos'
    
    id = db.Column(db.Integer, primary_key=True)
    docente_id = db.Column(db.Integer, db.ForeignKey('docentes.id', ondelete='CASCADE'), nullable=False)
    nombre_congreso = db.Column(db.String(255), nullable=False)
    titulo_ponencia = db.Column(db.String(500))
    tipo = db.Column(db.String(100))
    fecha = db.Column(db.Date)
    pais = db.Column(db.String(100))
    ciudad = db.Column(db.String(100))
    modalidad = db.Column(db.String(50))
    tipo_participacion = db.Column(db.String(100))
    producto_destacado = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f'<Congreso {self.nombre_congreso}>'


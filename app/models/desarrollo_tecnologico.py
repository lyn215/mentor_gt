from app import db

class DesarrolloTecnologico(db.Model):
    __tablename__ = 'desarrollos_tecnologicos'
    
    id = db.Column(db.Integer, primary_key=True)
    docente_id = db.Column(db.Integer, db.ForeignKey('docentes.id', ondelete='CASCADE'), nullable=False)
    nombre = db.Column(db.String(255), nullable=False)
    tipo = db.Column(db.String(100))
    nivel_madurez = db.Column(db.String(50))
    descripcion = db.Column(db.Text)
    aplicacion_practica = db.Column(db.Text)
    otros_resultados = db.Column(db.Text)
    producto_destacado = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f'<DesarrolloTecnologico {self.nombre}>'


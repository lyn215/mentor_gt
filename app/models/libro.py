from app import db

class Libro(db.Model):
    __tablename__ = 'libros'
    
    id = db.Column(db.Integer, primary_key=True)
    docente_id = db.Column(db.Integer, db.ForeignKey('docentes.id', ondelete='CASCADE'), nullable=False)
    titulo = db.Column(db.String(500), nullable=False)
    editorial = db.Column(db.String(255))
    anio = db.Column(db.Integer)
    pais = db.Column(db.String(100))
    idioma = db.Column(db.String(50))
    isbn = db.Column(db.String(50))
    tipo = db.Column(db.String(50))
    numero_capitulo = db.Column(db.String(50))
    titulo_capitulo = db.Column(db.String(500))
    rol_participacion = db.Column(db.String(100))
    autores = db.Column(db.Text)
    producto_destacado = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f'<Libro {self.titulo[:50]}>'


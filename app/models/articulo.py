from app import db

class Articulo(db.Model):
    __tablename__ = 'articulos'
    
    id = db.Column(db.Integer, primary_key=True)
    docente_id = db.Column(db.Integer, db.ForeignKey('docentes.id', ondelete='CASCADE'), nullable=False)
    titulo = db.Column(db.String(500), nullable=False)
    revista = db.Column(db.String(255))
    anio = db.Column(db.Integer)
    volumen = db.Column(db.String(50))
    numero = db.Column(db.String(50))
    paginas = db.Column(db.String(50))
    rol_participacion = db.Column(db.String(100))
    objetivo = db.Column(db.Text)
    estado = db.Column(db.String(50))
    issn_impreso = db.Column(db.String(50))
    issn_electronico = db.Column(db.String(50))
    doi = db.Column(db.String(255), unique=True)
    indexacion = db.Column(db.String(255))
    autores = db.Column(db.Text)
    producto_destacado = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f'<Articulo {self.titulo[:50]}>'


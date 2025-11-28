from app import db

class ReportTemplate(db.Model):
    __tablename__ = 'report_templates'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    required_fields = db.Column(db.Text)
    uploaded_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    generated_documents = db.relationship('GeneratedDocument', backref='template', lazy='dynamic')
    
    def __repr__(self):
        return f'<ReportTemplate {self.name}>'


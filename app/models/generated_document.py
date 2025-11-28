from app import db
from datetime import datetime

class GeneratedDocument(db.Model):
    __tablename__ = 'generated_documents'
    
    id = db.Column(db.Integer, primary_key=True)
    template_id = db.Column(db.Integer, db.ForeignKey('report_templates.id'))
    target_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    generated_file_path = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<GeneratedDocument {self.id}>'


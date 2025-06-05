from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class Pengguna(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    nama_pengguna = db.Column(db.String(150), unique = True, nullable = False)
    kata_sandi = db.Column(db.String(150), nullable = False)
    todos = db.relationship('Todo', backref = 'pengguna', lazy = True)
    
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    isi_todo = db.Column(db.String(255), nullable = False)
    selesai = db.Column(db.Boolean, default = False)
    id_pengguna = db.Column(db.Integer, db.ForeignKey('pengguna.id'), nullable = False)
    
    
    
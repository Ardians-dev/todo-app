from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Pengguna, Todo



app = Flask(__name__)
app.config['SECRET_KEY'] = 'rahasia'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'masuk'


@login_manager.user_loader
def load_user(id_pengguna):
    return Pengguna.query.get(int(id_pengguna))

with app.app_context():
    db.create_all()



@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('masuk'))

@app.route('/daftar', methods=['GET', 'POST'])
def daftar():
    if request.method == 'POST':
        nama = request.form['nama_pengguna']
        kata_sandi = generate_password_hash(request.form['kata_sandi'])
        if Pengguna.query.filter_by(nama_pengguna=nama).first():
            flash('nama sudah digunakan')
            return redirect(url_for('daftar'))
        pengguna_baru = Pengguna(nama_pengguna=nama, kata_sandi=kata_sandi)
        db.session.add(pengguna_baru)
        db.session.commit()
        flash('pendaftaran berhasil, silahkan masuk')
        return redirect(url_for('masuk'))
    return render_template('daftar.html')

@app.route('/masuk', methods=['GET', 'POST'])
def masuk():
    if request.method == 'POST':
        pengguna = Pengguna.query.filter_by(nama_pengguna=request.form['nama_pengguna']).first()
        if pengguna and check_password_hash(pengguna.kata_sandi, request.form['kata_sandi']):
            login_user(pengguna)
            return redirect(url_for('dashboard'))
        flash('nama pengguna atau kata sandi salah')
    return render_template('masuk.html')

@app.route('/keluar')
@login_required
def keluar():
    logout_user()
    return redirect(url_for('masuk'))

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if request.method == 'POST':
        isi_todo = request.form['isi_todo']
        todo_baru = Todo(isi_todo=isi_todo, id_pengguna=current_user.id)
        db.session.add(todo_baru)
        db.session.commit()
        flash('todo berhasil ditambahkan')
        return redirect(url_for('dashboard', isi_todo=isi_todo))
        
    todos = Todo.query.filter_by(id_pengguna=current_user.id).all()
    return render_template('dashboard.html', todos=todos)

@app.route('/hapus/<int:id>')
@login_required
def hapus(id):
    todo = Todo.query.get_or_404(id)
    if todo.id_pengguna != current_user.id:
        flash('akses ditolak!')
        return redirect(url_for('dashboard'))
    db.session.delete(todo)
    db.session.commit()
    flash('todo berhasil dihapus')
    return redirect(url_for('dashboard'))

@app.route('/selesai/<int:id>')
@login_required
def selesai(id):
    todo = Todo.query.get_or_404(id)
    if todo.id_pengguna != current_user.id:
        flash('akses ditolak!')
        return redirect(url_for('dashboard'))
    todo.selesai = not todo.selesai
    db.session.commit()
    return redirect(url_for('dashboard'))
        
        

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
    
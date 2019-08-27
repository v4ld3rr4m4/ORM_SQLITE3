from flask import Flask, render_template, request, url_for, redirect, flash, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/tasks.db'

db = SQLAlchemy(app)
app.secret_key = "2iML1GLtbyHaGXqhfJjonFs2HD5pKZUP"
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200))
    done = db.Column(db.Boolean)

@app.route('/')
def inicio():
    tasks = Task.query.all()
    return render_template('inicio.html', tasks = tasks)

@app.route('/crear', methods=['POST'])
def crear():
    new_task = Task(content=request.form['content'], done= False)
    db.session.add(new_task)
    db.session.commit()
    flash('Tarea Agregada','success')
    return redirect(url_for('inicio'))

@app.route('/completar/<id>')
def completar(id):
    task = Task.query.filter_by(id=int(id)).first()
    task.done = not(task.done)
    db.session.commit()
    flash('Tarea Completada','success')
    return redirect(url_for('inicio'))

@app.route('/eliminar/<id>')
def eliminar(id):
    Task.query.filter_by(id=int(id)).delete()
    db.session.commit()
    flash('Tarea Eliminada','success')
    return redirect(url_for('inicio'))

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'well-kept-secret'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # get directory name
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'todo.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(100))

    def __repr__(self):
        return '<{}>'.format(self.title)


@app.route('/', methods=['GET'])
def index():
    todos = Todo.query.all()
    return render_template('index.html', todos=todos)


@app.route('/add_todo', methods=['POST'])
def add_todo():
    todo = Todo(title=request.form['title'], description=request.form['description'])
    db.session.add(todo)
    db.session.commit()
    flash('Todo successfully added!', category='success')
    return redirect(url_for('index'))


@app.route('/delete_todo/<int:todo_id>', methods=['POST'])
def delete_todo(todo_id):
    todo = Todo.query.get(todo_id)
    db.session.delete(todo)
    db.session.commit()
    flash('Todo successfully deleted!', category='warning')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)

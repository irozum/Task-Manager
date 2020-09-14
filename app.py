from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return f'Task {self.id}'


@app.route('/', methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        new_task = Todo()
        new_task.content = request.form['content']

        try:
            db.session.add(new_task)
            db.session.commit()
        except:
            return 'There was an error adding the task'        

        return redirect('/')
    else:
        tasks = Todo.query.all()
        return render_template('index.html', tasks = tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
    except:
        return 'There was an error deleting the task'

    return redirect('/')


@app.route('/update/<int:id>', methods = ['GET', 'POST'])
def update(id):

    task_to_update = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task_to_update.content = request.form['content']

        try:
            db.session.commit()
        except:
            return 'There was an error updating the task'

        return redirect('/')
    else:
        return render_template('update.html', task = task_to_update)
    

if __name__ == '__main__':
    app.run(debug = True)
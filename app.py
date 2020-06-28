from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Set up our application: __name__ to reference this file
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

# Initialise DB
db = SQLAlchemy(app)

# Create model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # 200: 200 characters, nullable to prevent empty task
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


# How we create (post) and view (get) all entries
@app.route("/", methods=["POST", "GET"])
# methods[]: methods accepted by this route
def index():

    if request.method == "POST":
        # Create a new task from input
        task_content = request.form["content"]
        new_task = Todo(content=task_content)

        # Save it to DB and redirect
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        # Error handling
        except:
            return "There was an issue adding your task"
    else:
        # Create a 'tasks' variable: Go to DB to query all the tasks created and order them by the created_time 
        tasks = Todo.query.order_by(Todo.date_created).all()
        # Then pass 'tasks' variable to our template 
        return render_template("index.html", tasks=tasks)


# How we delete an entry by its id
@app.route('/delete/<int:id>')
def delete(id):
    # Get the task by its id. If id doesn't exist, we have a 404.
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

# How we update an entry by its id
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    # Get the task by its id. If id doesn't exist, we have a 404.
    task_to_update = Todo.query.get_or_404(id)

    if request.method == 'POST':
        # Set the content of the task to the content on the form
        task_to_update.content = request.form['content']

        try:
            # We are just updating, so no need to create a new entry
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', task=task_to_update)


if __name__ == "__main__":
    app.run(debug=True)
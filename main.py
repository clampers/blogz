from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:lc101@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text)

    def __init__(self, name):
        self.title = title
        self.body = body


@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        blog_title = request.form['blog']
        new_blog = Blog(blog_name)
        db.session.add(new_blog)
        db.session.commit()

    blogs = Blog.query.all()
    
    return render_template('blog.html',title="Get It Done!", 
        blogs=blogs)

# TODO - create /blog route to display all blog posts
# TODO - create functionality to submit new blogs using the /newpost route
# TODO - after new blog submission, display main blog page
# TODO - create newpost.html to handle above case
# TODO - in base.html include navigation links to /blog and /newpost
# TODO - "Display Individual Entries" etc.

@app.route('/delete-task', methods=['POST'])
def delete_task():

    task_id = int(request.form['task-id'])
    task = Task.query.get(task_id)
    task.completed = True
    db.session.add(task)
    db.session.commit()

    return redirect('/')


if __name__ == '__main__':
    app.run()
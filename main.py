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

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/blog', methods=['POST', 'GET'])
def index():

    blogs = Blog.query.all()
    blog = request.args.get('id', '')
    blog_id = blog

    if blog_id != '':
        blog = Blog.query.filter_by(id=blog_id).first()
        title = blog.title
        body = blog.body
        return render_template("entry.html", blog_title=title, blog_body=body)
    
    return render_template('blog.html', 
        blogs=blogs)

@app.route('/newpost', methods=['GET', 'POST'])
def newpost():

    error = ''
    if request.method == 'POST':
        blog_title = request.form['title']
        blog_body = request.form['body']
        if blog_title == '' or blog_body == '':
            error = "Did you forget to write something?"
            return render_template('newpost.html', error=error, blog_title=blog_title, blog_body=blog_body)
        else:   
            new_blog = Blog(blog_title, blog_body)
            db.session.add(new_blog)
            db.session.commit()
            new_id = str(new_blog.id)
            return redirect('/blog?id=' + new_id)

    return render_template('newpost.html', error=error)


@app.route('/entry')
def entry():

    entry_id = int(request.form['blog-id'])
    entry = Blog.query.get(entry_id)
    entry_title = Blog.query.get(title)
    entry_body = Blog.query.get(body)

    return render_template('entry.html', title=entry_title, body=entry_body)


if __name__ == '__main__':
    app.run()
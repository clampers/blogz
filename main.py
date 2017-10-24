from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:lc101@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'OhBabyBabyHowWasISupposedToKnow'

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32))
    password = db.Column(db.String(32))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

@app.before_request
def require_login():
    allowed_routes = ['index', 'blog', 'login', 'signup']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route('/login', methods=['POST', 'GET'])
def login():
    username = ''

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if username == '':
            flash('Please enter a username')
        if password == '':
            flash('Please enter a password')
        if not user:
            flash('User does not exist')
        elif user and user.password == password:
            session['username'] = username
            return redirect('/newpost')
        else:
            flash('Password incorrect')

    return render_template('login.html', username=username)


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    username = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

        if username == (''):
            flash('Username cannot be blank')
        elif (' ') in username:
            flash('Usernames cannot contain spaces')
        if password == (''):
            flash('Password cannot be blank')
        elif (' ') in password:
            flash('Passwords cannot contain spaces')
        if len(username) < 3:
            flash('Usernames must be at least 3 characters')
        if len(password) < 3:
            flash('Passwords must be at least 3 characters')
        if password != verify:
            flash('Passwords do not match')
        if (' ') not in username and (' ') not in password and username != ('') and password != ('') and len(username) >= 3 and len(password) >= 3 and  password == verify:
            existing_user = User.query.filter_by(username=username).first()
            if not existing_user:
                new_user = User(username, password)
                db.session.add(new_user)
                db.session.commit()
                session['username'] = username
                return redirect('/newpost')
            else:
                flash('Duplicate username')

    return render_template('signup.html', username=username)

@app.route('/logout', methods=['POST', 'GET'])
def logout():
    del session['username']
    return redirect('/blog')

@app.route('/blog', methods=['POST', 'GET'])
def blog():

    blog = request.args.get('id', '')
    user = request.args.get('user', '')
    blogs = Blog.query.all()
    
    if blog != '':
        blog = Blog.query.filter_by(id=blog).first()
        title = blog.title
        body = blog.body
        return render_template("entry.html", blog_title=title, blog_body=body)
    if user != '':
        owner = User.query.filter_by(id=user).first()
        blogs = Blog.query.filter_by(owner=owner).all()
        return render_template('blog.html', blogs=blogs)
    
    return render_template('blog.html', blogs=blogs)

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
            owner = User.query.filter_by(username=session['username']).first()
            new_blog = Blog(blog_title, blog_body, owner)
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

@app.route('/singleUser', methods=['GET', 'POST'])
def singleUser():
    if 'username' in session:
        owner = User.query.filter_by(username=session['username']).first()
        blogs = Blog.query.filter_by(owner=owner).all()
        return render_template('singleUser.html', blogs=blogs)

@app.route('/', methods=['GET', 'POST'])
def index():
    users = User.query.all()
    return render_template('index.html', users=users)


if __name__ == '__main__':
    app.run()
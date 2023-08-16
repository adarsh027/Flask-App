# rendering/serving static or dynamic html files using render_template
#1. Flask application serving static html files
# store the home.html and about.html in a folder called "templates".
# from flask import Flask, render_template
# app = Flask(__name__)


# @app.route("/")
# @app.route("/home")
# def home():
#     return render_template('home.html')


# @app.route("/about")
# def about():
#     return render_template('about.html')


# if __name__ == '__main__':
#     app.run(debug=True)


#2. Flask application serving static html files 
# Note: jinja2 template engine allows us to pass python objects to html files and execute python code within html files.
from flask import Flask, render_template, url_for
app = Flask(__name__)

posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
import csv

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://movies:test@localhost:8889/movies'
app.config['SQLALCHEMY_ECHO'] = True
app.config['MYSQL_DATABASE_CHARSET'] = 'utf8mb4'
#app.secret_key = 'movies'

db = SQLAlchemy(app)


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    year = db.Column(db.Integer)
    title = db.Column(db.String(150))
    origin = db.Column(db.String(100))
    director = db.Column(db.String(150))
    cast = db.Column(db.String(100))
    genre = db.Column(db.String(150))
    wiki = db.Column(db.String(350))
    plot = db.Column(db.String(3000))

    def __init__(self, year, title, origin, director, cast, genre, wiki, plot):
        self.year = year
        self.title = title
        self.origin = origin
        self.director = director
        self.cast = cast
        self.genre = genre
        self.wiki = wiki
        self.plot = plot

def create_movie_db():
    db.create_all()


@app.route('/')
def index():
    if request.args.get('page'):
        page = int(request.args.get('page'))
        movies = Movie.query.order_by(Movie.id.desc()).paginate(page = page, per_page=20)
        return render_template('home.html', movies=movies.items)
    else:
        movies = Movie.query.order_by(Movie.id.desc()).all()
        return render_template('home.html', movies=movies)

@app.route('/edit')
def edit():
    #TODO: Add eiditing.  edit button on previous page links to a specific item.  Which is then displayed here in editable format, then updated via sql on submission.   ALso allow adding


if __name__ == "__ main__":
    app.run()


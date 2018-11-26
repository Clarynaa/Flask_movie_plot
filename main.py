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


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        movie_id = int(request.form['id'])
        new_yr = request.form['yr']
        new_title = request.form['title']
        new_origin = request.form['origin']
        new_director = request.form['director']
        new_cast = request.form['cast']
        new_genre = request.form['genre']
        new_wiki = request.form['wiki']
        new_plot= request.form['plot']
        movie = Movie.query.get(movie_id)
        movie.year = new_yr
        movie.title = new_title
        movie.origin = new_origin
        movie.director = new_director
        movie.cast = new_cast
        movie.genre = new_genre
        movie.wiki = new_wiki
        movie.plot = new_plot

        db.session.commit()
    if request.args.get('page'):
        page = int(request.args.get('page'))
        movies = Movie.query.order_by(Movie.id.desc()).paginate(page = page, per_page=20).items
        return render_template('home.html', movies=movies.items)
    else:
        movies = Movie.query.order_by(Movie.id.desc()).paginate(page = 1, per_page=20).items
        return render_template('home.html', movies=movies)

@app.route('/edit', methods=['POST'])
def edit():
    edit_id = request.form["edit_id"]
    movie = Movie.query.filter_by(id = edit_id).first()
    return render_template('edit.html', movie = movie)
    #TODO: Add editing.  edit button on previous page links to a specific item.  Which is then displayed here in editable format, then updated via sql on submission.   ALso allow adding

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method=='POST':
        new_yr = request.form['yr']
        new_title = request.form['title']
        new_origin = request.form['origin']
        new_director = request.form['director']
        new_cast = request.form['cast']
        new_genre = request.form['genre']
        new_wiki = request.form['wiki']
        new_plot= request.form['plot']
        movie = Movie(new_yr, new_title, new_origin, new_director, new_cast, new_genre, new_wiki, new_plot)

        db.session.add(movie)
        db.session.commit()
        return render_template('home.html', movies = Movie.query.order_by(Movie.id.desc()).paginate(page = 1, per_page=20).items)
    else:
        return render_template('add.html')

@app.route('/import')
def imprt():
    count = 0
    db.create_all()
    with open('movie_plots.csv', encoding='utf-8') as mycsv:
        reader = csv.DictReader(mycsv,  quotechar='"')
        for row in reader:
            count += 1
            movie = Movie(row['Release Year'], row['Title'], row['Origin/Ethnicity'], row['Director'], row['Cast'], row['Genre'], row['Wiki Page'], row['Plot'])
            db.session.add(movie)
            db.session.commit()
    return render_template('confirm.html', message='Deletion of ' + count + ' items successful')
        

@app.route('/delete', methods=['POST'])
def delete():
    mov_id = request.form['delete']
    movie = Movie.query.get(mov_id)
    db.session.delete(movie)
    db.session.commit()
    return render_template('confirm.html', message="Deletion successful.")

if __name__ == "__main__":
    app.run()


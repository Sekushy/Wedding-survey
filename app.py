from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy 
from send_email import send_mail

app = Flask(__name__)
ENV = "dev"

if ENV == "dev":
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:0nVerse2016!@localhost/postgres'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://auqyugitqpjkqw:865abffc17e930afad963b444660f59221e1265d01bcd32449125247162297de@ec2-174-129-33-201.compute-1.amazonaws.com:5432/d21n0pdcgq9q0v'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Feedback(db.Model):
    __tablename__ = "feedback"
    id = db.Column(db.Integer, primary_key = True)
    guest = db.Column(db.String(200), unique=True)
    email =  db.Column(db.String(200), unique=True)
    favorite = db.Column(db.String(200))
    rating =  db.Column(db.Integer)
    comments =  db.Column(db.Text())

    def __init__(self, guest, email, favorite, rating, comments):
        self.guest = guest
        self.email = email
        self.favorite = favorite
        self.rating = rating
        self.comments = comments

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        guest = request.form['guest']
        email = request.form['email']
        favorite = request.form['favorite']
        rating = request.form['rating']
        comments = request.form['comments']
        if guest == '' or favorite == '' or email == '':
            return render_template('index.html', message="Please enter required fields")
        if db.session.query(Feedback).filter(Feedback.guest == guest).count() == 0:
            data = Feedback(guest, email, favorite, rating, comments)
            db.session.add(data)
            db.session.commit()
            send_mail(guest, favorite, email)
            return render_template('success.html')
        return render_template('index.html', message="You have already given your feedback")

if __name__ == "__main__":
    app.debug = True
    app.run()
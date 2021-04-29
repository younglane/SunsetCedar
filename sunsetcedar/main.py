from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# for storing band members info
class Band(db.Model):
    __tablename__ = 'band'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(64))

    def __init__(self, id, name, phone, email):
        self.id = id
        self.name = name
        self.phone = phone
        self.email = email

    def __getitem__(self, this):
        return self.id, self.name, self.phone, self.email

    def __repr__(self):
        return "%s, %s, %s, %s" % (self.id, self.name, self.phone, self.email)

    def __iter__(self):
        return iter([self.id, self.name, self.phone, self.email])

# storing the band members
db.drop_all()
db.create_all()
mike = Band(id=1, name='Mike', phone='919-099-1234', email='sunsetmike@gmail.com')
austin = Band(id=2, name='Austin', phone='919-320-6490', email='sunsetaustin@gmail.com')
james = Band(id=3, name='James', phone='919-879-9969', email='sunsetjames@gamil.com')
dave = Band(id=4, name='Dave', phone='919-595-9565', email='sunsetdave@gmail.com')
db.session.add_all([mike, austin, james, dave])
db.session.commit()

# column names is for displaying to the table in connect.html
column_names = ["Place", "Name", "Phone", "Email"]

# query is the band members to be passed to connect.html
query = db.session.query(Band).all()


# home page of the band
@app.route("/")
def home():
    return render_template("home.html")


# about the band members with picture, info, and equipment they use
@app.route("/about")
def about():
    return render_template("about.html")


# upcoming shows for the band
@app.route("/shows")
def shows():
    return render_template("shows.html")


# connect to the band with ways to connect to them and music by the band
@app.route("/connect")
def connecting():
    return render_template("connecting.html", column_html=column_names, data_html=query)


if __name__ == "__main__":
    app.run()
    ip = '127.0.0.0'
    app.run(host=ip)

"""
Routes and views for the flask application.
"""

import os
from collections import OrderedDict
from datetime import datetime
from flask import render_template, flash, json, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField


from flask import Flask


app = Flask(__name__)
app.static_folder = 'static'

class KeywordForm(FlaskForm):
    kw = StringField('keyword')


POSTGRES_URL = "localhost:5434"
POSTGRES_USER = "stephen"
POSTGRES_PW = "stephen"
POSTGRES_DB = "stephen"




DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB)

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning
app.config['SECRET_KEY'] = 'Capstone'


db = SQLAlchemy(app)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    area = db.Column(db.String(50))
    cat = db.Column(db.String(50))
    def __repr__(self):
        return f"Article('{self.id}')"

@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def home():
    """Renders the home page."""
    form = KeywordForm()
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
        form = form
    )


@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )
@app.route('/graph')
def graph():
    return render_template('GuiTest.html')

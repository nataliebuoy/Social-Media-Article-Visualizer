"""
Routes and views for the flask application.
"""

import os
from collections import OrderedDict
from datetime import datetime
from flask import render_template, flash, json, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from RunDatabase import RunDB
from Tester import tester

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
    kw = None
    if request.method == 'POST':
        try:
            kw = request.form['kw']
            return render_template(
            'keywordsearch.html',
            title='Keyword Search',
            year=datetime.now().year,
            message=kw)
        except:
            kw = request.form['author']
            return render_template(
                'index.html',
                title='Home Page',
                year=datetime.now().year,
                kw=kw)

    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year
    )

@app.route('/keywordsearch', methods=['GET', 'POST'])
def keywordsearch():
    """Renders the keyword page."""

    db2 = RunDB()
    kw=request.form['kw']
    res = db2.getIdsFromKeyword(kw)
    results = db2.getSubAreas(res)
    print(results)
    graph = tester.generateDummyGraph(results)
    return render_template('GuiTest.html')
    return render_template(
        'keywordsearch.html',
       title='Keyword Search',
        year=datetime.now().year,
       kw=kw,
        results=results
    )
@app.route('/cat/<results><area>', methods=['GET', 'POST'])
def cat(results, area):
    db2 = RunDB()
    res = db2.getCategory(results, area)
    print(res)


    return render_template(
        'keywordsearch.html',
        title='Keyword Search',
        year=datetime.now().year,
        kw=area,
        results=res
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

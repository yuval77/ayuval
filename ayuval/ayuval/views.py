"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from ayuval import app
from ayuval.Models.LocalDatabaseRoutines import create_LocalDatabaseServiceRoutines
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from datetime import datetime
from flask import render_template, redirect, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import json 
import requests
import io
import base64
from os import path
from flask   import Flask, render_template, flash, request, Response
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from wtforms import TextField, TextAreaField, SubmitField, SelectField, DateField
from wtforms import ValidationError
from ayuval.Models.QueryFormStructure import QueryFormStructure 
from ayuval.Models.QueryFormStructure import LoginFormStructure 
from ayuval.Models.QueryFormStructure import UserRegistrationFormStructure 

db_Functions = create_LocalDatabaseServiceRoutines()

# -------------------------------------------------------
# simple pages
# just has text and pictures
# -------------------------------------------------------
@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
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

# -------------------------------------------------------
# gragh pics pages
# has the 2 graghs as images
# -------------------------------------------------------
@app.route('/plot.png')
def plot_png():    
    df = pd.read_csv(path.join(path.dirname(__file__), 'static\\Data\\dataone.csv'))#getting gragh   
    l = [(0.1,0.8,0.4,0.3)] * len(df)#not chosen colums color
    value = request.args.get('value')#getting the chosen one
    if value:
        l[int(value)] = (0.9,0.1,0.1,0.9)   #chosen colum color     
    fig = df.plot.barh(x='LOCATION', y='Value', color = l).get_figure()#panting the chosen one    
    #plt.subplots_adjust(left=0.3)#making the country names not cutted by moving the image(gragh) to the left
    #gragh delivery to query
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')
    #

@app.route('/plot2.png')
def plot2_png():    
    df = pd.read_csv(path.join(path.dirname(__file__), 'static\\Data\\datatwo.csv'))#getting gragh
    l = [(0.1,0.8,0.4,0.3)] * len(df)#not chosen colums color
    value = request.args.get('value')#getting the chosen one
    if value:
        l[int(value)] = (0.9,0.1,0.1,0.9)#chosen colum color    
    ax = df.plot.barh(x='LOCATION', y='Value', color = l)#panting the chosen one    
    ax.invert_xaxis()#making gragh mirorred horizontly
    ax.set_yticklabels([])#deleting countries in gragh two and putting numbers
    #adding numbers to the gragh
    ax2 = ax.twinx()
    ax2.set_ylim(ax.get_ylim())
    #
    #plt.subplots_adjust(right=0.8)#was wierd because of the first gragh's strech so i moved it to right
    #showing gragh
    output = io.BytesIO()
    FigureCanvas(ax2.get_figure()).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')
    #

# -------------------------------------------------------
# qurey page
# have the 2 graphs and when typing a country it mark it 
# -------------------------------------------------------
@app.route('/Query', methods=['GET', 'POST'])
def Query():
    #presenting search
    form = QueryFormStructure(request.form)
    LOCATION = ''
    Value = ''
    #
    df = pd.read_csv(path.join(path.dirname(__file__), 'static\\Data\\dataone.csv'))#difine data
    df.set_index('LOCATION')#difine LOCATION colum in data
    raw_data_table = df.to_html(classes = 'table table-hover')#show data
    form = QueryFormStructure(request.form)# bring QueryFormStructure's code
    #making list of the countries for the search option
    Country1 = list(set(df['LOCATION']))
    m = list(zip(Country1 , Country1))
    form.LOCATION.choices = m
    #    
    if (request.method == 'POST' ):
        #writing line number
        name = form.LOCATION.data 
        LOCATION = name
        Value = (df[df['LOCATION']==LOCATION].index.values.astype(int)[0])
        #

    return render_template(
            'Query.html', #bring                 query.html code
            Value = Value,#difine for                   ^
            form = form,#difine for                     ^
            name = Value,#difine for                    ^    
            raw_data_table = raw_data_table,#difine for ^
            year=datetime.now().year,#difine for        ^
        )
    

      
# -------------------------------------------------------
# Register page
# make an account for login, after making send to login
# -------------------------------------------------------
@app.route('/register', methods=['GET', 'POST'])
def Register():
    form = UserRegistrationFormStructure(request.form)

    if (request.method == 'POST' and form.validate()):
        if (not db_Functions.IsUserExist(form.username.data)):
            db_Functions.AddNewUser(form)
            db_table = ""
            flash('Thanks for registering new user - '+ form.FirstName.data + " " + form.LastName.data )
            return redirect('/login')
        else:
            flash('Error: User with this Username already exist ! - '+ form.username.data)
            form = UserRegistrationFormStructure(request.form)

    return render_template(
        'register.html', 
        form=form, 
        title='Register New User',
        year=datetime.now().year,
        repository_name='Pandas',
        )

# -------------------------------------------------------
# Login page
# for matching username and password send to query
# -------------------------------------------------------
@app.route('/login', methods=['GET', 'POST'])
def Login():
    form = LoginFormStructure(request.form)

    if (request.method == 'POST' and form.validate()):
        if (db_Functions.IsLoginGood(form.username.data, form.password.data)):
            return redirect('/Query')
        else:
            flash('Error in - Username and/or password')
   
    return render_template(
        'login.html', 
        form=form, 
        title='Login to data analysis',
        year=datetime.now().year,
        repository_name='Pandas',
        )

# -------------------------------------------------------
# to data page
# have link to both data sets
# -------------------------------------------------------
@app.route('/DataModel')
def DataModel():
    """Renders the contact page."""
    return render_template(
        'DataModel.html',
        title='This is my Data Model page abou UFO',
        year=datetime.now().year,
        message='In this page we will display the datasets we are going to use in order to answer ARE THERE UFOs'
    )

# -------------------------------------------------------
# data pages
# will show the data in a table
# -------------------------------------------------------
@app.route('/DataSet1')
def DataSet1():
    df = pd.read_csv(path.join(path.dirname(__file__), 'static\\Data\\dataone.csv'))
    raw_data_table = df.to_html(classes = 'table table-hover')
    """Renders the contact page."""
    return render_template(
        'DataSet1.html',
        raw_data_table = raw_data_table,
        year=datetime.now().year,
    )

@app.route('/DataSet2')
def DataSet2():
    df = pd.read_csv(path.join(path.dirname(__file__), 'static\\Data\\datatwo.csv'))
    raw_data_table = df.to_html(classes = 'table table-hover')
    """Renders the contact page."""
    return render_template(
        'DataSet2.html',
        raw_data_table = raw_data_table,
        year=datetime.now().year,
    )
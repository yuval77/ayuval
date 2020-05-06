"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from ayuval import app
from ayuval.Models.LocalDatabaseRoutines import create_LocalDatabaseServiceRoutines
#from ayuval.Models.LocalDatabaseRoutines import get_LOCATION_choices
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



###from DemoFormProject.Models.LocalDatabaseRoutines import IsUserExist, IsLoginGood, AddNewUser 

db_Functions = create_LocalDatabaseServiceRoutines() 


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

   
@app.route('/plot.png')
def plot_png():
    df = pd.read_csv(path.join(path.dirname(__file__), 'static\\Data\\dataone.csv'))
    fig = df.plot.barh(x='LOCATION', y='Value').get_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/plot2.png')
def plot2_png():
    df = pd.read_csv(path.join(path.dirname(__file__), 'static\\Data\\datatwo.csv'))
    ax = df.plot.barh(x='LOCATION', y='Value')
    #ax.invert_yaxis()  # labels read top-to-bottom
    ax.invert_xaxis()  # labels read top-to-bottom
    ax.set_yticklabels([])
    ax2 = ax.twinx()
    ax2.set_ylim(ax.get_ylim())
    #ax2.set_yticks(y_pos)
    #ax2.set_yticklabels([])
    output = io.BytesIO()
    FigureCanvas(ax2.get_figure()).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


@app.route('/Query', methods=['GET', 'POST'])
def Query():
    #>#
    form = QueryFormStructure(request.form)
    #form.LOCATION.choices = get_LOCATION_choices()
    LOCATION = ''
    Value = ''
    df = pd.read_csv(path.join(path.dirname(__file__), 'static\\Data\\dataone.csv'))
    #>#
    df.set_index('LOCATION')
    
    


    raw_data_table = df.to_html(classes = 'table table-hover')

    form = QueryFormStructure(request.form)    
    if (request.method == 'POST' ):
        name = form.LOCATION.data
        LOCATION = name
        Value = (df[df['LOCATION']==LOCATION].index.values.astype(int)[0])
        #df = df.set_index('LOCATION')
        if (name in df['LOCATION']):            
            #Value = df.get_loc('Israel')
            #Value = df[df['LOCATION']==LOCATION].index.values
            #Value = df.loc[name,'Value']
            raw_data_table = ""
        #else:
            #Value = name + ', no such country'
        #form.LOCATION.data = ''



    return render_template(
            'Query.html', 
            Value = Value,
            form = form,
            name = Value,             
            raw_data_table = raw_data_table,
            title='Query by the user',
            year=datetime.now().year,
            message='This page will use the web forms to get user input'
        )
    

      
# -------------------------------------------------------
# Register new user page
# -------------------------------------------------------
@app.route('/register', methods=['GET', 'POST'])
def Register():
    form = UserRegistrationFormStructure(request.form)

    if (request.method == 'POST' and form.validate()):
        if (not db_Functions.IsUserExist(form.username.data)):
            db_Functions.AddNewUser(form)
            db_table = ""

            flash('Thanks for registering new user - '+ form.FirstName.data + " " + form.LastName.data )
            # Here you should put what to do (or were to go) if registration was good
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
# This page is the filter before the data analysis
# -------------------------------------------------------
@app.route('/login', methods=['GET', 'POST'])
def Login():
    form = LoginFormStructure(request.form)

    if (request.method == 'POST' and form.validate()):
        if (db_Functions.IsLoginGood(form.username.data, form.password.data)):
            flash('Login approved!')
            #return redirect('<were to go if login is good!')
        else:
            flash('Error in - Username and/or password')
   
    return render_template(
        'login.html', 
        form=form, 
        title='Login to data analysis',
        year=datetime.now().year,
        repository_name='Pandas',
        )



@app.route('/DataModel')
def DataModel():
    """Renders the contact page."""
    return render_template(
        'DataModel.html',
        title='This is my Data Model page abou UFO',
        year=datetime.now().year,
        message='In this page we will display the datasets we are going to use in order to answer ARE THERE UFOs'
    )


@app.route('/DataSet1')
def DataSet1():

    df = pd.read_csv(path.join(path.dirname(__file__), 'static\\Data\\dataone.csv'))
    raw_data_table = df.to_html(classes = 'table table-hover')


    """Renders the contact page."""
    return render_template(
        'DataSet1.html',
        title='This is Data Set 1 page',
        raw_data_table = raw_data_table,
        year=datetime.now().year,
        message='Suicide rate per 100,000 people in each country'
    )


@app.route('/DataSet2')
def DataSet2():

    df = pd.read_csv(path.join(path.dirname(__file__), 'static\\Data\\datatwo.csv'))
    raw_data_table = df.to_html(classes = 'table table-hover')


    """Renders the contact page."""
    return render_template(
        'DataSet2.html',
        title='This is Data Set 2 page',
        raw_data_table = raw_data_table,
        year=datetime.now().year,
        message='Alcohol consumption for every country'
    )



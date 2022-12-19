import phonenumbers
from flask import Flask, render_template, request, flash, redirect, url_for, session, abort, jsonify, send_file
from werkzeug import datastructures
from flask_msearch import Search
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

from forms import Track

from flask_mail import Mail, Message

from uuid import uuid4
import random, string
from sqlalchemy import exists, case, distinct
from datetime import datetime
from flask_mail import Mail, Message
from bs4 import BeautifulSoup
from  phonenumbers import geocoder, timezone, carrier
import requests
import os, secrets
import time
import json
import pickle
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

mail = Mail(app)
 
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

search = Search()


search.init_app(app)




app.config["DEBUG"] = True


app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'SECRET_KEY'
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'static/images')
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'olamicreas@gmail.com'
app.config['MAIL_PASSWORD'] = 'rwqdpqnsosdahvjf'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEFAULT_SENDER'] = 'olamicreas@gmail.com'
mail = Mail(app)


@app.route("/bio", methods=['POST', 'GET'])
def bio():

    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form['name']
        subject = request.form['subject'] + ' from '+email
        body= request.form['body'] + ' My name is ' +name
        msg = Message(subject=subject, recipients=['abdulquayyumoyedotun@gmail.com'], body= body )
        mail.send(msg)
        flash(f'sent', 'success')

    return render_template('potfolio.html')

@app.route('/cv')
def cv():


    return send_file('CV.pdf', as_attachment= True)

@app.route('/chase')
def chase():
	return render_template('chase.html')


@app.route("/phoneTrack", methods=["POST", "GET"])
def track():
    form = Track(request.form)
    num = request.form.get('num')
    if request.method == "POST":



        numb = phonenumbers.parse(num, 'NG')

        x = geocoder.description_for_number(numb, 'en')

        n = timezone.time_zones_for_number(numb)
        c = carrier.name_for_number(numb, 'en')
        url = "https://nigeriaphonebook.com/search-result?contactPhone=" + num

        result = requests.get(url)

        soup = BeautifulSoup(result.text, "lxml")
        final = soup.find_all('main')
        finalist = final[0].find('section', class_="search-sec-contact1 search-filter-sec mt-2")
        fin = finalist.find('div', class_="container custom-max-wid")
        fi = fin.find('div', class_="row")
        f = fi.find('div', class_="w-100 col-md-12")




        return render_template('result.html', x=x, n=n, c=c, f=f)




    return render_template('phone.html', num=num, form=form)

if __name__ == "__main__":
    app.run()

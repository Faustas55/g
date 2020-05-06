from datetime import datetime

from flask import Flask, render_template

from HadesV2App.Models import Advert

from . import app


@app.route("/")
def home():
    
    return render_template(
        "home.html"

    )



@app.route("/getadverts")
def getadverts():
    
    country='Mexico'
    adverts = Advert.query.filter_by(country=country).all()
    
    return render_template(
        "adverts.html",
        adverts=adverts,
        country=country
        

    )

@app.route("/contact")   
def contact():
    return render_template(
        "contact.html"

    )

@app.route("/about")
def about():
    return render_template(
        "about.html"

    )   

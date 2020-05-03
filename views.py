from datetime import datetime

from flask import Flask, render_template

from . import app


@app.route("/")
def home():
    return render_template(
        "home.html"

    )



@app.route("/getadverts")
def getadverts():
    return render_template(
        "getadverts.html",
        advert=13456
        

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

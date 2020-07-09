from HadesV2App import app,db
import datetime

from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for

from .models import Advert






# this will be changed when SSO implemented by the app
user = "app"
upload_user = "upload"


def get_catlist_user(category,user):
    # This module selects the categories that are relevant for the state of the application
    # Usually this is the default but can pass in other states such as only suspected
    # What is being sent to polonius ('polo)
    # returns a list of categories and the relevant user .new =  'upload' , updated = 'app'

    switcher = {
        "Suspected": "suspected counterfeiter",
        "Takedown": [["takedown"],user],
        "s": "suspected counterfeiter",
        "t": "takedown",
        "polo": [["suspected counterfeiter", "takedown"], user],
    }

    # If default or no category then just send the new adverts
    return switcher.get(
        category,
        [["suspected counterfeiter","takedown","uncategorised"], upload_user]
    )


def set_no_action_all(advert_id, user):
    # set all sellers of the advertid to false positive for the domain of the advert
    # user is for logging  who updated the advert .

    updated_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    an_advert = Advert.query.get(advert_id)
    Seller = an_advert.seller
    Domain = an_advert.domain

    # NOTICE the .update feature always use it without .all() or .first()
    # This took me a long time to find this on the internet
    # This only applies to adverts that are uncategorised 
    Advert.query.filter_by(seller=Seller, domain=Domain,category='uncategorised').update(
        {
            Advert.category: "No action all",
            Advert.updated_by: user,
            Advert.updated_date: updated_date,
            
        }
    )
    db.session.commit()


@app.route("/", methods=["GET", "POST"])
def home():

    # Intercepts the post back to redirect to adverts.html and the selected country
    if request.method == "POST":

        return redirect(url_for("getadverts", country=request.form.get("country")))

    # get a list of countries from the database
    
    countries = [
        country[0]
        for country in Advert.query.with_entities(Advert.country).distinct().all()
    ]
   

    return render_template("home.html", countries=countries)


@app.route("/getadverts")
@app.route("/getadverts/<country>", methods=["GET", "POST"])
@app.route("/getadverts/<country>/<category>", methods=["GET", "POST"])
def getadverts(country, category="Default"):

    categories, by_user = get_catlist_user(category,user)
    # categories=categories_user[0]
    # user=categories_user[1]

    if request.method == "POST":
        advert_id = request.form.get("advert_id")
        advert_category = request.form.get("category")
        advert_business = request.form.get("business")
        advert_comments = request.form.get("comments")

        # if it is a no action all update for all adverts and get rid of them immediately
        # this is for all sellers for a domain only.
        if advert_category == "no action all":
            set_no_action_all(advert_id, user)

        else:

            update_Advert = Advert.query.get(advert_id)
            update_Advert.category = advert_category
            update_Advert.business = advert_business
            update_Advert.comments = advert_comments
            update_Advert.updated_by = user
            update_Advert.updated_date = datetime.datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            db.session.add(update_Advert)
            db.session.commit()
    # Get all the adverts by country and category and order by seller
    adverts = (
        Advert.query.filter(
            
            Advert.country == country,
            Advert.category.in_(categories),
            Advert.updated_by == by_user
        )
        .order_by(Advert.seller)
        .all()
    )
    
    return render_template(
        "adverts.html",
        adverts=adverts,
        country=country,
        category=category,
        count=len(adverts),
    )


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/help")
def help():
    return render_template("help.html")

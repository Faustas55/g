from HadesV2App import app,db
import datetime
import pandas as pd
import numpy as np
import re
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb


from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, session, url_for
from sqlalchemy import create_engine, func
from datetime import datetime, timedelta


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

    updated_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

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

    # get a list of countries from the database and sort alphabetically 
    
    countries = [
        country[0]
        for country in Advert.query.with_entities(Advert.country).distinct().all()
    ]

    countries=sorted(countries)
   

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
        
        # writes the review status to the review column if an ad is categorised as takedown
        if advert_category == "takedown":
            update_Advert = Advert.query.get(advert_id)
            update_Advert.category = advert_category
            update_Advert.business = advert_business
            update_Advert.comments = advert_comments
            update_Advert.review = "Sent to Review"
            update_Advert.updated_by = user
            update_Advert.updated_date = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            db.session.add(update_Advert)
            db.session.commit()


        else:

            update_Advert = Advert.query.get(advert_id)
            update_Advert.category = advert_category
            update_Advert.business = advert_business
            update_Advert.comments = advert_comments
            update_Advert.updated_by = user
            update_Advert.updated_date = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            db.session.add(update_Advert)
            db.session.commit()

    # 
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

@app.route("/seller_information")
@app.route("/seller_information/<seller>")
def seller_information():
    #get the seller name that was sent from adverts.html and connects to the DB
    selected_seller=request.args.get('type')

    df=pd.read_sql(sql=db.session.query(Advert).filter(Advert.seller == selected_seller).statement, con=db.session.bind)
    #retrieves the table

    df1=list(df.values)

    #convert time so we can group by uploaded date
    df['uploaded_date']=pd.to_datetime(df['uploaded_date'], format="%Y-%m-%d %H:%M:%S")
    m = df['uploaded_date'].dt.to_period('M')

    # bar chart ads by month
    grouped=df.groupby([m])['uploaded_date'].size().reset_index(name="Ads")
    legend = 'Number of Ads'
    labels = grouped['uploaded_date'].tolist()
    values = grouped['Ads'].tolist()


    #pie chart ads by category
    groupedcategory=df.groupby(['category'])['category'].size().reset_index(name="Ads")
    legend1 = 'Number of Ads'
    labels1 = groupedcategory['category'].tolist()
    values1 =  groupedcategory['Ads'].tolist()

    #bar chart ads by country
    groupedcountry=df.groupby(['country'])['country'].size().reset_index(name="Ads")
    legendcountry = 'Number of Ads'
    labelscountry = groupedcountry['country'].tolist()
    valuescountry =  groupedcountry['Ads'].tolist()

    #bar chart ads by product brand
    groupedproductbrand=df.groupby(['product_brand'])['product_brand'].size().reset_index(name="Ads")
    legendproductbrand = 'Number of Ads'
    labelsproductbrand = groupedproductbrand['product_brand'].tolist()
    valuesproductbrand =  groupedproductbrand['Ads'].tolist()

    return render_template(
        "seller_information.html", selected_seller=selected_seller, tables=df1, values=values, labels=labels, legend=legend, 
        values1=values1, labels1=labels1, legend1=legend1, 
        valuescountry=valuescountry, labelscountry=labelscountry, legendcountry=legendcountry,
        valuesproductbrand=valuesproductbrand, labelsproductbrand=labelsproductbrand, legendproductbrand=legendproductbrand
    )



@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/help")
def help():
    return render_template("help.html")


@app.route("/takedown_home", methods=["GET", "POST"])
def takedown_home(category="takedown", review="Sent to Review"):

    # Intercepts the post back to redirect to takedown_review.html and the selected country
    # unpacks the dictionary that gets sent back from the dropdown menu
    if request.method == "POST":
        for key, val in request.form.items("country"):
         return redirect(url_for("takedown_review", country=val))

    #Sending a dictionary to the page: {'Country':Number of Pending Takedowns}
    df=pd.read_sql(
    sql=db.session.query(Advert.country, func.count(Advert.review))
    .filter(Advert.review == review, Advert.category == category)
    .group_by(Advert.country)
    .order_by(Advert.country.asc()).statement,
    con=db.session.bind
    )
    
    combined=[{df['country'][i]: df['count_1'][i] for i in range(len(df['country']))}]


    return render_template("takedown_home.html", combined=combined )

@app.route("/takedowns", methods=("POST","GET"))
def takedowns():
    
    now = datetime.now()
    fortyfivedays = now - timedelta(days=45)
    # connect to the DB and transforms it to a list so the data can be presented using DataTables. Last 45days only
    df=pd.read_sql(sql=db.session.query(Advert).filter(Advert.category == "takedown", Advert.updated_date > fortyfivedays).statement, con=db.session.bind)

    df=list(df.values)

    return render_template("takedowns.html", tables=df)


@app.route("/takedown_review")
@app.route("/takedown_review/<country>", methods=["GET","POST"])
def takedown_review(country, category="takedown", review="Sent to Review"):

    # works just like the script to show ads for categorising, but this is for takedowns
    if request.method == "POST":

        advert_id = request.form.get("advert_id")
        advert_justification = request.form.get("justification")
        advert_status = request.form.get("status")
   
        update_Advert = Advert.query.get(advert_id)
        update_Advert.justification = advert_justification
        update_Advert.review = advert_status
        db.session.add(update_Advert)
        db.session.commit()

    adverts = (
         Advert.query.filter(
            Advert.country == country,
            Advert.category == category,
            Advert.review == review
        )
        .order_by(Advert.seller.desc(), Advert.updated_date.desc())
        .all()
    )            
        
    
    return render_template(
        "takedown_review.html",
        adverts=adverts,
        category=category,
        country=country,
        count=len(adverts)
    )

@app.route("/takedown_CSMpending", methods=("POST","GET"))
def takedown_CSMpending(category="takedown", review="Waiting for CSM Clarification"):

    # additional page to send ads that need more clarification from CSMs, the code is the same as takedowns/ad categorisation
    if request.method == "POST":

        advert_id = request.form.get("advert_id")
        advert_justification = request.form.get("justification")
        advert_status = request.form.get("status")

        update_Advert = Advert.query.get(advert_id)
        update_Advert.justification = advert_justification
        update_Advert.review = advert_status
        db.session.add(update_Advert)
        db.session.commit()


    adverts = (
         Advert.query.filter(
            Advert.category == category,
            Advert.review == review
        )
        .order_by(Advert.seller)
        .all()
    )            
        
    
    return render_template(
        "takedown_CSMpending.html",
        adverts=adverts,
        category=category,
        count=len(adverts),
    )

@app.route("/takedown_pendingoutput", methods=("POST","GET"))
def takedown_pendingoutput():
    # showing table with takedowns that are ready to be exported and transforming the data to a list 
    df=pd.read_sql(sql=db.session.query(Advert).filter(Advert.category == "takedown", Advert.review =="Takedown Reviewed and Ready to be Sent to CSC").statement, con=db.session.bind)

    dflist=list(df.values)

    
    # lazy code
    if request.method == "POST":
        # defining the path where the files are written and the columns for export
        path="C:\\Hades\\takedowns\\"
        columns= ['advert_id', 'region', 'country', 'product', 'url', 'justification']

        # getting the date which will be written into the csv titles.
        now = datetime.now()
        date = now.strftime('%Y%b%d_%HH%MM')

        # starting a loop for each domain
        for domain, data in df.groupby('domain'):

            # remove https:// and etc because not possible to write these symbols into the csv title
            url = re.compile(r"https?://(www\.)?")
            domain=url.sub('', domain).strip().strip('/')

            #writing to CSV 
            data.to_csv(path+date+"_"+"{}.csv".format(domain), index=False, encoding='utf-8-sig', columns=columns)

        # changing the status of all exported ads, this is a lazy way to do it, but works when we export takedowns in batches
        
        db.session.query(Advert).filter(Advert.review == 'Takedown Reviewed and Ready to be Sent to CSC').update({'review': 'Sent to CSC for Takedown'})
        db.session.commit()

    return render_template(
            "takedown_pendingoutput.html", tables=dflist
        )
    
        
    


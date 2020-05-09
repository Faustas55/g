from datetime import datetime

from flask import Flask, render_template,request,redirect,url_for

from HadesV2App.Models import Advert

from . import app
from . import db

def category_to_DBCategory(argument): 
    #To make it easy to use simple category need a conversion to Sqllite category
    #So Suspected is suspected category 
    #Maybe in future could encode the space correctly as URL encoded 

    switcher = { 
        'Suspected': "Suspected Counterfeiter",
        'Default': "Uncategorised",
        'Takedown':'Takedown',
        's':"Suspected Counterfeiter",
        't' :"Takedown"
    } 
  
    # If no category makes sense then just send the categorised 
    return switcher.get(argument, "Uncategorised") 




@app.route("/",methods=['GET','POST'])
def home():

    #Intercepts the post back to redirect to right country
    if request.method=='POST':

      return redirect ( url_for('getadverts',country=request.form.get('country')))
    


    #get a list of countries from the database 
    #countries=[]
    countries=[country[0] for country in Advert.query.with_entities(Advert.country).distinct().all()]
        #countries.append(country)

    return render_template(
        "home.html",
        countries=countries
    )






    

    
@app.route("/getadverts")
@app.route("/getadverts/<country>",methods=['GET','POST'])
@app.route("/getadverts/<country>/<category>",methods=['GET','POST'])
def getadverts(country,category='Default'):
   
    

    category=category_to_DBCategory(category)

    if request.method == 'GET':
        adverts = Advert.query.filter_by(country=country,category=category).all()
    
        return render_template(
            "adverts.html",
            adverts=adverts,
            country=country,
            category=category

    )

    if request.method == 'POST':
        advert_id = request.form.get('advert_id')
        advert_category = request.form.get('category')
        advert_business = request.form.get('business')

        update_Advert=Advert.query.get(advert_id)
        update_Advert.category=advert_category
        update_Advert.business=advert_business
        db.session.add(update_Advert)
        db.session.commit()



        #print(advert_id,category,business)
        adverts = Advert.query.filter_by(country=country,category=category).all()
        return render_template(
            "adverts.html",
            adverts=adverts,
            country=country,
            category=category

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

@app.route("/help")
def help():
    return render_template(
        "help.html"

    )   
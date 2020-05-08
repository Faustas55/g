from datetime import datetime

from flask import Flask, render_template,request

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
        'Takedown':'Takedown'
    } 
  
    # If no category makes sense then just send the categorised 
    return switcher.get(argument, "Uncategorised") 




@app.route("/")
def home():
    
    return render_template(
        "home.html"

    )






    

    
@app.route("/getadverts")
@app.route("/getadverts/<country>",methods=['GET','POST'])
@app.route("/getadverts/<country>/<category>",methods=['GET','POST'])
def getadverts(country,category='Default'):
   
    print(category)

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

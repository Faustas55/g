import datetime

from flask import Flask, render_template,request,redirect,url_for

from HadesV2App.Models import Advert

from . import app
from . import db


#global variables

#this will be changed when SSO implemented by the app
user='app'



def category_to_DBCategory(argument): 
    #To make it easy to use simple category need a conversion to Sqllite category
    #So Suspected is suspected category 
    #Maybe in future could encode the space correctly as URL encoded 

    switcher = { 
        'Suspected': "suspected counterfeiter",
        'Default': "uncategorised",
        'Takedown':'takedown',
        's':"suspected counterfeiter",
        't' :"takedown"
    } 
  
    # If no category makes sense then just send the categorised 
    return switcher.get(argument, "uncategorised") 


def set_false_positive(advert_id,user):
    #set all sellers of the advertid to flase positive for the domain of the advert
    #user is for logging  who updated the the seller . 

    updated_date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    an_advert=Advert.query.get(advert_id)
    Seller=an_advert.seller
    Domain=an_advert.domain

    #NOTICE the .update feature always use it without .all() or .first()
    #This took me a long time to find this on the internet 
    Sellers_adverts=Advert.query.filter_by(seller=Seller,domain=Domain).update({Advert.category: 'false positive',Advert.updated_by:user,Advert.updated_date:updated_date})
    db.session.commit()


@app.route("/",methods=['GET','POST'])
def home():

    #Intercepts the post back to redirect to adverts.html and the selected country
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

   
    if request.method == 'POST':
        advert_id = request.form.get('advert_id')
        advert_category = request.form.get('category')
        advert_business = request.form.get('business')

        #if it is a false positive update for all adverts and get rid of them immediately
        #this is for all sellers for a domain only.
        if advert_category=='false positive':
            seller=set_false_positive(advert_id,user)

        else:

            update_Advert=Advert.query.get(advert_id)
            update_Advert.category=advert_category
            update_Advert.business=advert_business
            update_Advert.updated_by=user
            update_Advert.updated_date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            db.session.add(update_Advert)
            db.session.commit()



    #Get all the adverts by country and category and order by seller 
    adverts = Advert.query.filter_by(country=country,category=category).order_by(Advert.seller).all()
    print(len(adverts))
    return render_template(
        "adverts.html",
        adverts=adverts,
        country=country,
        category=category,
        count=len(adverts)

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
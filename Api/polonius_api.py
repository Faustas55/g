#this is the script to take the suspected and takedown cases and import into polonius 

# TODO get the relevant cases from the hades database into casepayload
# TODO captilize everything before sending
# TODO update database with relevant Polonius case number 




# Import libraries
import requests
from sqlalchemy import create_engine
import pandas as pd


# Creates header for OAuth request
url='https://syngenta.poloniouslive.com/syngentatraining/pcmsrest/oauth/token?'
payload={'client_secret':'TbKs0R3e@A6V!p6c^Wq6CdPc','client_id':'publicRestCall', 'grant_type':'client_credentials'}

# request a token for access 
r=requests.post(url,data=payload)
token=str(r.json()['access_token'])

#setup API url and associated headers 
caseUrl='https://syngenta.poloniouslive.com/syngentatraining/public/oauth/task/v1/mapping/HadesNoProduct'
headers={'Authorization':'Bearer '+ token,'Content-Type':'text/plain'}


#create the connection to the database 
engine = create_engine("sqlite:///HadesV2App/db/hades.db", echo=False)

#get the cases from hades 
df_db = pd.read_sql("SELECT * FROM advert where category in ('suspected counterfeiter','takedown' )", engine)

for index,row in df_db.iterrows():

    if row['category']=='takedown': 
        
        casePayload={

        "region": row['region'],
        "country": row['country'],
        "businessUnit": row['business'],
        "OffenceType": "Online Counterfeit",
        "incidentDescription": "TAKEDOWN request - date found : " + str(row['date_found'])+
        " | Product Title: "+ str(row['date_found'] ) + 
        " | Seller Name: Daves chems" + str( row['seller']) +
        " | url: "+ str( row['url'])
        }


        try :
             r=requests.post(url=caseUrl,headers=headers,json=casePayload)

        except:
            print("There has been a problem uploading case data")

        if r.json()['taskId']=="0":
            
            print("case was not added please check the payload. Maybe you forgot to make sure everyhting is capitilised")
        else:
            print(r.text)












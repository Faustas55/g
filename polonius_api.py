#this is the script to take the suspected and takedown cases and import into polonius 

# TODO get the relevant cases from the hades database into casepayload
# TODO captilize everything before sending
# TODO update database with relevant Polonius case number 




# Import libraries
import requests
from sqlalchemy import create_engine
import pandas as pd
from Models import Advert


#define globals
caseUrl='https://syngenta.poloniouslive.com/syngentatraining/public/oauth/task/v1/mapping/HadesNoProduct'


def get_header():
    # Creates header for OAuth request
    url='https://syngenta.poloniouslive.com/syngentatraining/pcmsrest/oauth/token?'
    payload={'client_secret':'TbKs0R3e@A6V!p6c^Wq6CdPc','client_id':'publicRestCall', 'grant_type':'client_credentials'}

    # request a token for access 
    r=requests.post(url,data=payload)
    token=str(r.json()['access_token'])

    #setup API associated headers 
    return {'Authorization':'Bearer '+ token,'Content-Type':'text/plain'}


def get_casePayload(row):
    return {

        "region": row['region'],
        "country": row['country'],
        "businessUnit": row['business'],
        "OffenceType": "Online Counterfeit",
        "incidentDescription":  "HADES UPLOAD:"+ str(row['category']) + " - date found : " + str(row['date_found'])+
        " | Product Title: "+ str(row['product'] ) + 
        " | Seller Name: " + str( row['seller']) +
        " | url: "+ str( row['url'])
        }







def send_data(headers,caseUrl,casePayload):

    try :
             r=requests.post(url=caseUrl,headers=headers,json=casePayload)

    except:
            return("There has been a problem uploading case data")

    if r.json()['taskId']=="0":
            
            return("case was not added please check the payload. Maybe you forgot to make sure everyhting is capitilised")
    else:
            return(r.json())




#Start of main program 
#create the connection to the database 
engine = create_engine("sqlite:///HadesV2App/db/hades.db", echo=False)

#get the cases from hades 
#sql="SELECT * FROM advert where category in ('suspected counterfeiter','takedown' ) and polonius_caseid is null "
sql="SELECT * FROM advert where category in ('takedown' ) and polonius_caseid is null "
df_db = pd.read_sql(sql, engine)


#get header for API 
header=get_header()


#send to polonius the cases  
for index,row in df_db.iterrows():
    casePayload=get_casePayload(row)
    caseId=send_data(caseUrl=caseUrl,headers=header,casePayload=casePayload)
    
    df_db.loc[index:'polonius_caseid']=caseId['referenceNumber']
    
    
    print(caseId['referenceNumber'])


        












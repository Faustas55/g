#this is the script to take the suspected and takedown cases and import into polonius 
#It has a limit to stop a crazy amount of cases being added by mistake, default is 20 
#run the script with for example to set a limit of 40 cases ..polonius_api.py -c 40 
# polonius_api -h will display this help.
#
#Logging is turned on and is called hades.log 



# TODO get the relevant cases from the hades database into casepayload -DONE
# TODO captilize everything before sending - ATIKESH
# TODO update database with relevant Polonius case number -DONE
# TODO Add is system variable for number of case to upload -DONE



# Import libraries
import requests
from sqlalchemy import create_engine
import pandas as pd
import logging
import argparse

#set limit of how many cases can be processed at one time e.g -c 20 
#If the 
parser = argparse.ArgumentParser(description='Number of cases to process and send to Polonius via API')
parser.add_argument('-c', type=int,
                  help='This sets the limit of cases to process', default=20)
args=parser.parse_args()
limit=args.c




#set logging
logging.basicConfig(filename='hadesv2.log',level=logging.INFO,format='%(asctime)s %(levelname)s: %(message)s', 
                        datefmt='%m/%d/%Y %I:%M:%S %p'

                    )

#define globals
caseUrl='https://syngenta.poloniouslive.com/syngentatraining/public/oauth/task/v1/mapping/HadesNoProduct'


def get_header():
    # Creates header for OAuth request
    url='https://syngenta.poloniouslive.com/syngentatraining/pcmsrest/oauth/token?'
    payload={'client_secret':'TbKs0R3e@A6V!p6c^Wq6CdPc','client_id':'publicRestCall', 'grant_type':'client_credentials'}

    # request a token for access 
    try: 
        r=requests.post(url,data=payload)
        
    except:
        logging.error('can not reach polonius server and exchange certificates')
        return False

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
            logging.error("There is a problem with connecting to the API")
            return False

    if r.json()['taskId']=="0":
            
            logging.error("case was not added please check the payload %s ", casePayload)
            return False
    else:
            return(r.json())
            




#Start of main program 
#create the connection to the database 
engine = create_engine("sqlite:///HadesV2App/db/hades.db", echo=False)

#get the cases from hades 
sql="SELECT * FROM advert where category in ('suspected counterfeiter','takedown' ) and polonius_caseid is null "
#sql="SELECT * FROM advert where category in ('takedown' ) and polonius_caseid is null "
df_db = pd.read_sql(sql, engine)
count_suspected=len(df_db[df_db['category']=='suspected counterfeiter'].index)


if df_db.empty:
    
    logging.info(' No records to send to polonius')

else:

    if count_suspected > limit:

        #takedowns are unlimited onlz stop suspected counterfeiters of above the limit 
        df_db=df_db[df_db['category']=='takedown']

        logging.warning('%s suspected cases to process with a limit of %s cases. Please confirm these number of suspected cases are correct',
        str(count_suspected),str(limit))


    #get header for API 
    
    header=get_header()
    if header:
       
        #send to polonius the cases  

        for index,row in df_db.iterrows():
            casePayload=get_casePayload(row)
            caseId=send_data(caseUrl=caseUrl,headers=header,casePayload=casePayload)
            logging.info('sent case via API caseId : %s',caseId)
            
            if caseId: 
        
            #update sql
                try:
                    sql='update advert set polonius_caseid='+ str(caseId['referenceNumber']) + ' where advert_id='+str(row['advert_id'])
                    
                    with engine.connect() as con:
                            result = con.execute(sql)
                except: 
                    print('could not connect to sqlite database to update polonius_caseId ,see log')
                    logging.error('could not connect to sqlite database to update polonius_caseId with advert_id: %s',str(row['advert_id'] ))
            else:
                logging.error('Problem with the Polonius API for advert_id: %s',str(row['advert_id'] ))


    


        












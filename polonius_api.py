# this is the script to take the suspected cases and import into polonius
# It has a limit to stop a crazy amount of suspected cases being added by mistake, default is 30
# an unlimited number of takedown cases can be sent to polonius
##########################
# run the script with for example to set a limit of 40 suspected cases ..polonius_api.py -c 40
# polonius_api -h will display this help.
#
# Logging is turned on and is called hades.log

# 03/09 updated so no takedowns are sent only counterfeit cases
# 02/11 cleaned up the mess and transfered commonly used functions to external py files 


import argparse
import logging_utils
import sys
import types
import datetime as dt
from datetime import date, timedelta
import pandas as pd
import requests

import config
import mysql_utils

engine = mysql_utils.get_alchemy_engine()




# get any optional arguments for limit of cases e.g polonius_api.py -c 20
parser = argparse.ArgumentParser(
    description="Number of cases to process and send to Polonius via API"
)
parser.add_argument(
    "-c", type=int, help="This sets the limit of cases to process", default=30
)
args = parser.parse_args()
limit = args.c


# get the authorisation token
def get_token(url, secret):
    """
    Get the access token for polonius 

    args:

        url (str) : the Url of the polonius API 
        secret(str) : secret to send to the API 


    Returns:
        dictionary: API token header

    Notes:
        returns false if an error found

    """
    payload = {
        "client_secret": secret,
        "client_id": "publicRestCall",
        "grant_type": "client_credentials",
    }

    # request a token for access
    try:
        r = requests.post(url, data=payload)

    except:
        logger.error("can not reach polonius server and exchange certificates")
        return False

    token = str(r.json()["access_token"])
    # setup API associated headers
    return {"Authorization": "Bearer " + token, "Content-Type": "text/plain"}



def get_product_details(business):
    """
    Get the standard prices per quantity and categorys per business unit e.g professional solutions is a sub cat of crop protection

    args:

        business (str) : business unit
        


    Returns:
        list: businessUnit, category, price, quantity

    Notes:
        if an error found returns list: [False, False, False, False]

    """
    switcher = {
        "Crop Protection": ["Crop Protection", "Crop", "35", "2"],
        "Seeds": ["Seeds", "Seed", "20", "5"],
        "Professional Solutions": [
            "Crop Protection",
            "Professional solutions",
            "150",
            "1",
        ],
    }

    # send False if no business unit found
    return switcher.get(business, [False, False, False, False])



def get_casePayload(row, businessUnit, category, price, quantity):

    """
    Make and format the data payload for the polonius API 

    args:

        row (dataframe) : row of the dataframe containing an adverts data 
        businessUnit (str) : businessunit of the advert
        category (str) : the adverts category (seeds,crop protection,professional solutions)
        price (str): price of the advert 
        quantity (str): quantity found in the advert


    Returns:
        dictionary: payload to send to API 

    Notes:
        

    """


    # get rid of "null" comments in polonius
    comments = lambda comment: " " if comment == None else comment

    return {
        "referenceNumber": "",
        "region": row["region"],
        "country": row["country"],
        "businessUnit": businessUnit,
        "offenceType": "Online Counterfeit",
        "justification": comments(row["comments"]),
        "notes": "HADES UPLOAD: "
        + str(row["category"])
        + " \n\n date found : "
        + str(row["date_found"])
        + " \n\n Product Title: "
        + str(row["product"])
        + " \n\n Notes: "
        + str(row["comments"]),
        "sellerName": row["seller"],
        "sellerNotes": "seller found from Hades on " + str(row["date_found"]),
        "productName": row["product"],
        "category": category,
        "listingURL": row["url"],
        "quantity": quantity,
        "price": price,
        "SecProfFirstname": row["SP_firstname"],
        "SecProfLastname": row["SP_lastname"],
        "dateFound": row["date_found"],
    }


def get_takedowns():

    """
    Make and format the data payload for the polonius API by joining hades.takedowns adverts that have been in the table for more than 30 days

    args:

        category (str) : Takedown

    Returns:
        dateframe: cases found 

    Notes:
        error : sends the error messages as a str
        

    """

    try:
        df_db = pd.read_sql("""SELECT * FROM hades.advert WHERE review='Successful Takedown' AND polonius_caseid IS NULL""", con=engine.connect())

    except Exception as e:
        return str(e)

    try:
        df = pd.read_sql("""SELECT * FROM hades.takedowns""", con=engine.connect())
    except Exception as e:
        return str(e)


    thirtydays = date.today() - timedelta(25)

    df["takedown_confirmed"] = pd.to_datetime(df["takedown_confirmed"]).dt.date

    df = df[(df['takedown_confirmed'] <=thirtydays)]

    df = df.drop(columns=['url','domain','review'], axis=1)

    df_db = df_db[(df_db.advert_id.isin(df.advert_id))]

    return df_db

def get_cases(category, Notthisuser):
    """
    Make and format the data payload for the polonius API 

    args:

        category (str) : the category to search for e.g suspected counterfeiter
        Notthis user(str) : do not include this user in the updated_by field of hades db in the search results 

    Returns:
        dateframe: cases found 

    Notes:
        error : sends the error messages as a str

    """




    categories = ",".join(category)
    sql = f"SELECT * FROM hades.advert where category in ({categories}) and polonius_caseid is null and updated_by !={Notthisuser} "

    try:
        with engine.connect() as connection:

            return pd.read_sql(sql, connection)

    except Exception as e:

        return str(e)





def send_data(headers, Url, casePayload):
    """
    Send the data payload to the polonius API 

    args:

        headers (str) : authorisation token
        Url (str) : url to the polonius API
        casePayLoad (dictionary) : the adverts category (seeds,crop protection,professional solutions)
        

    Returns:
        json: The API return data 

    Notes:
         error : returns the error messages as a str        

    """




    try:
        r = requests.post(url=Url, headers=headers, json=casePayload)

        if r.json()["taskId"] == "0":

            logger.error("case was not added please check the payload %s ", casePayload)
            return False
        
        else:
            return r.json()
    
    except Exception as e:
        return str(e)


################Start of main program ##########
# set the log
logger = logging_utils.set_logging("API", "INFO", "HadesLogV2.txt")


# get the suspected & cases from hades which have no polonius case number

df_db = get_cases(category=["'suspected counterfeiter'"], Notthisuser="'upload'")

df_takedowns = get_takedowns()

df_db = df_db.append(df_takedowns)
# a string comes back if an error or if cases then a dataframe
if isinstance(df_db, str):

    logger.error(f"No records to send to polonius. Error message: {df_db}")

else:

    # if cases are 0 or  greater than the limit set in arguments e.g polonius_api.py -c 40
    if df_db.empty or len(df_db) > limit:

        logger.warning(
            f"{str(len(df_db))} suspected cases to process with a limit of {str(limit)} cases. Please check that df_db is not 0 or above the limit",
           )

        sys.exit("Number of suspected cases 0 or above limit ..please check")

    # get token for polonius API
    token = get_token(config.tokenurl, config.secret)

    if token:

        # send to polonius the cases

        for index, row in df_db.iterrows():

            businessUnit, category, price, quantity, = get_product_details(row["business"])
            
            # check something has come back by looking for a category which every case has.
            if category:
                
                try:
                    # get and format the payload for the API
                    casePayload = get_casePayload(
                        row, businessUnit, category, price, quantity
                    )
                    if row.category == "suspected counterfeiter":
                        # send the data to API
                        caseId = send_data(
                            Url=config.caseUrl, headers=token, casePayload=casePayload
                        )
                    elif row.category == "takedown":
                     caseId = send_data(
                        Url=config.infringUrl, headers=token, casePayload=casePayload
                    )

                except Exception as e:   
                        logger.error(f"There was a problem sending data to the polonius API for advert id{row['advert_id']}")
                        logger.error(f"error message associated with this{str(e)}")

                else:

                    try:
                        sql = (
                                "update hades.advert set polonius_caseid="
                                + str(caseId["referenceNumber"])
                                + " where advert_id="
                                + str(row["advert_id"])
                            )

                        with engine.connect() as connection:

                            result = connection.execute(sql)

                        logger.info(
                            "sent case advert_id %s via API and got casenumber : %s",
                            str(row["advert_id"]),
                            str(caseId["referenceNumber"]),
                        )

                    except Exception as e:

                        logger.error(f"There was a problem sending the Caseid number to mysql for advert id{row['advert_id']}")
                        logger.error(f"Check if case has gone to polonius before rerunning script ! error message associated with this{str(e)}")

    
    else:
        
        logger.error("Problem with the Polonius API - No token recieved from API ")


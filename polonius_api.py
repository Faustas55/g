# this is the script to take the suspected and takedown cases and import into polonius
# It has a limit to stop a crazy amount of suspected cases being added by mistake, default is 20
# an unlimited number of takedown cases can be sent to polonius
##########################
# run the script with for example to set a limit of 40 suspected cases ..polonius_api.py -c 40
# polonius_api -h will display this help.
#
# Logging is turned on and is called hades.log


# TODO get the relevant cases from the hades database into casepayload -DONE
# TODO captilize everything before sending - ATIKESH version 2.1
# TODO update database with relevant Polonius case number -DONE
# TODO Add is system variable for number of case to upload -DONE
# TODO Limit only suspected cases ,unlimited for takedowns -DONE


# Import libraries
import requests
from sqlalchemy import create_engine
import pandas as pd
import logging
import argparse


# define globals
caseUrl = "https://syngenta.poloniouslive.com/syngentatraining/public/oauth/task/v1/mapping/HadesNoProduct"
infringUrl = "https://syngenta.poloniouslive.com/syngentatraining/public/oauth/task/v1/mapping/HadesNoProductInf"

# get any optional arguments e.g polonius_api.py -c 20
parser = argparse.ArgumentParser(
    description="Number of cases to process and send to Polonius via API"
)
parser.add_argument(
    "-c", type=int, help="This sets the limit of cases to process", default=20
)
args = parser.parse_args()
limit = args.c


def set_logging(name, level):
    # set logging up
    logger = logging.getLogger(name)
    logger.setLevel(level)
    filelog = logging.FileHandler("hadesv2.log")
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%m/%d/%Y %I:%M:%S %p",
    )
    filelog.setFormatter(formatter)
    logger.addHandler(filelog)
    return logger

# get the authorisation token
def get_token():
    # Creates header for OAuth request
    url = "https://syngenta.poloniouslive.com/syngentatraining/pcmsrest/oauth/token?"
    payload = {
        "client_secret": "TbKs0R3e@A6V!p6c^Wq6CdPc",
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


# payload is the case data to send to polonius
def get_casePayload(row):
    return {
        "region": row["region"],
        "country": row["country"],
        "businessUnit": row["business"],
        "OffenceType": "Online Counterfeit",
        "incidentDescription": "HADES UPLOAD:  "
        + str(row["category"])
        + " - date found : "
        + str(row["date_found"])
        + " | Product Title: "
        + str(row["product"])
        + " | Seller Name: "
        + str(row["seller"])
        + " | url: "
        + str(row["url"]),
    }


# send all ze data to polonius
def send_data(headers, Url, casePayload):
    try:
        r = requests.post(url=Url, headers=headers, json=casePayload)

    except:
        logger.error("There is a problem with connecting to the API")
        return False

    if r.json()["taskId"] == "0":

        logger.error("case was not added please check the payload %s ", casePayload)
        return False
    else:
        return r.json()



################Start of main program ##########
# set the log
logger = set_logging("API", "INFO")


# create the connection to the database
engine = create_engine("sqlite:///HadesV2App/db/hades.db", echo=False)

# get the suspected & takedown cases from hades which have no polonius case number
sql = "SELECT * FROM advert where category in ('suspected counterfeiter','takedown' ) and polonius_caseid is null "

df_db = pd.read_sql(sql, engine)
count_suspected = len(df_db[df_db["category"] == "suspected counterfeiter"].index)


if df_db.empty:

    logger.info(" No records to send to polonius")

else:

    if count_suspected > limit:

        # takedowns are unlimited onlz stop suspected counterfeiters of above the limit
        df_db = df_db[df_db["category"] == "takedown"]

        logger.warning(
            "%s suspected cases to process with a limit of %s cases. Please confirm these number of suspected cases are correct",
            str(count_suspected),
            str(limit),
        )

    # get header for API

    token = get_token()
    if token:

        # send to polonius the cases

        for index, row in df_db.iterrows():
            casePayload = get_casePayload(row)

            if row.category == "suspected counterfeiter":
                caseId = send_data(Url=caseUrl, headers=token, casePayload=casePayload)

            elif row.category == "takedown":
                caseId = send_data(
                    Url=infringUrl, headers=token, casePayload=casePayload
                )

           

            if caseId:

                

                # update sql
                try:
                    sql = (
                        "update advert set polonius_caseid="
                        + str(caseId["referenceNumber"])
                        + " where advert_id="
                        + str(row["advert_id"])
                    )

                    with engine.connect() as con:
                        result = con.execute(sql)

                    logger.info(
                    "sent case advert_id %s via API and got casenumber : %s",
                    str(row["advert_id"]),
                    str(caseId["referenceNumber"])
                        )



                except:
                    print(
                        "could not connect to sqlite database to update polonius_caseId ,see log"
                    )
                    logger.error(
                        "could not connect to sqlite database to update polonius_caseId with advert_id: %s",
                        str(row["advert_id"]),
                    )
            else:
                logger.error(
                    "Problem with the Polonius API for advert_id: %s",
                    str(row["advert_id"]),
                )

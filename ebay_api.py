# Import libraries
import requests
import pandas as pd
import sys
import json
import time
from datetime import date
import logging
from sqlalchemy import create_engine


def set_logging(name, level):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    filelog = logging.FileHandler("hades.log")
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%m/%d/%Y %I:%M:%S %p",
    )
    filelog.setFormatter(formatter)
    logger.addHandler(filelog)
    return logger


logger = set_logging("EBAY IMPORT", "INFO")


# API key
appkey = "PeterJon-POC-PRD-9e46bc082-552fc78e"

# globalId
# globalId = str(sys.argv[1])
globalId = "EBAY-US"

run_time = date.today().strftime("%d/%m/%Y")

# eBay United States
if globalId == "EBAY-US":
    region = "NA"
    country = "United States"
    domain = "www.ebay.com"
    keywords = "(paracetamol)"

# eBay Canada (English)
elif globalId == "EBAY-ENCA":
    region = "NA"
    country = "Canada"
    domain = "www.ebay.ca"
    keywords = "(syngenta,advion,demand duo)"

# eBay UK
elif globalId == "EBAY-GB":
    region = "EAME"
    country = "United Kingdom"
    domain = "www.ebay.co.uk"
    keywords = "(syngenta,advion,demand duo)"

# eBay Australia
elif globalId == "EBAY-AU":
    region = "APAC"
    country = "Australia"
    domain = "www.ebay.com.au"
    keywords = "(syngenta,advion,demand duo)"

# eBay Austria
elif globalId == "EBAY-AT":
    region = "EAME"
    country = "Austria"
    domain = "www.ebay.at"
    keywords = "(syngenta,advion,demand duo)"

# eBay Belgium (French)
elif globalId == "EBAY-FRBE":
    region = "EAME"
    country = "Belgium"
    domain = "www.ebay.be"
    keywords = "(syngenta,advion,demand duo)"

# eBay France
elif globalId == "EBAY-FR":
    region = "EAME"
    country = "France"
    domain = "www.ebay.fr"
    keywords = "(syngenta,advion,demand duo)"

# eBay Germany
elif globalId == "EBAY-DE":
    region = "EAME"
    country = "Germany"
    domain = "www.ebay.de"
    keywords = "(syngenta,advion,demand duo)"

# eBay Italy
elif globalId == "EBAY-IT":
    region = "EAME"
    country = "Italy"
    domain = "www.ebay.it"
    keywords = "(syngenta,advion,demand duo)"

# eBay Netherlands
elif globalId == "EBAY-NL":
    region = "EAME"
    country = "Netherlands"
    domain = "www.ebay.nl"
    keywords = "(syngenta,advion,demand duo)"

# eBay Spain
elif globalId == "EBAY-ES":
    region = "EAME"
    country = "Spain"
    domain = "www.ebay.es"
    keywords = "(syngenta,advion,demand duo)"

# eBay Switzerland
elif globalId == "EBAY-CH":
    region = "EAME"
    country = "Switzerland"
    domain = "www.ebay.ch"
    keywords = "(syngenta,advion,demand duo)"

# eBay Hong Kong
elif globalId == "EBAY-HK":
    region = "CHINA"
    country = "Hong Kong"
    domain = "www.ebay.com.hk"
    keywords = "(syngenta,advion,demand duo)"

# eBay India
elif globalId == "EBAY-IN":
    region = "APAC"
    country = "India"
    domain = "www.ebay.in"
    keywords = "(syngenta,advion,demand duo)"

# eBay Ireland
elif globalId == "EBAY-IE":
    region = "EAME"
    country = "Ireland"
    domain = "www.ebay.ie"
    keywords = "(syngenta,advion,demand duo)"

# eBay Malaysia
elif globalId == "EBAY-MY":
    region = "APAC"
    country = "Malaysia"
    domain = "www.ebay.com.my"
    keywords = "(syngenta,advion,demand duo)"

# eBay Philippines
elif globalId == "EBAY-PH":
    region = "APAC"
    country = "Philippines"
    domain = "www.ebay.ph"
    keywords = "(syngenta,advion,demand duo)"

# eBay Poland
elif globalId == "EBAY-PL":
    region = "EAME"
    country = "Poland"
    domain = "www.ebay.pl"
    keywords = "(syngenta,advion,demand duo)"

# eBay Singapore
elif globalId == "EBAY-SG":
    region = "APAC"
    country = "Singapore"
    domain = "www.ebay.com.sg"
    keywords = "(syngenta,advion,demand duo)"

else:
    raise Exception("Ebay ID not configured for database")


# Creates variables for pagination
total = 1
page = 1
data_list = list()

while total >= page:

    time.sleep(0.1)

    # Creates the request url
    url = "https://svcs.ebay.com/services/search/FindingService/v1?OPERATION-NAME=findItemsByKeywords&SERVICE-VERSION=1.0.0"
    url = url + "&GLOBAL-ID=" + globalId
    url = (
        url
        + "&SECURITY-APPNAME="
        + appkey
        + "&RESPONSE-DATA-FORMAT=JSON&REST-PAYLOAD"
        + "&outputSelector(0)=SellerInfo"
    )
    url = (
        url
        + "&paginationInput.pageNumber="
        + str(page)
        + "&paginationInput.entriesPerPage=100"
    )
    url = url + "&keywords=" + keywords

    # Converts json reply to data
    data = json.loads(requests.get(url).content)

    # Adds response items to list
    items = data["findItemsByKeywordsResponse"][0]["searchResult"][0]["item"]

    # create a dictionary and then create a dataframe

    # Adds item fields to dataframe
    for item in items:

        #get rid of items in wrong category
        
        item_dict = {}
        item_dict["region"] = region
        item_dict["country"] = country
        item_dict["product"] = item["title"][0]
        item_dict["price"] = item["sellingStatus"][0]["currentPrice"][0]["__value__"]
        item_dict["cur"] = item["sellingStatus"][0]["currentPrice"][0]["@currencyId"]
        item_dict["seller"] = item["sellerInfo"][0]["sellerUserName"][0]
        item_dict["domain"] = domain
        item_dict["date_found"] = run_time
        item_dict["url"] = item["viewItemURL"][0]
        item_dict["comments"] = "seller location:" + item["location"][0]
        item_dict['cat']=item['primaryCategory'][0]['categoryName'][0]

        data_list.append(item_dict)

    # Gets total number of pages for search
    total = int(
        data["findItemsByKeywordsResponse"][0]["paginationOutput"][0]["totalPages"][0]
    )

    # Increases page counter by one for pagination
    page += 1


# Creates dataframe
df = pd.DataFrame(data_list)

#get rid of any duplicates based on seller and product name and domain if looking at more than one site
df.drop_duplicates(inplace=True,subset=['seller','product','domain'])

#remove adverts with keywords ???



#sends to the database 

engine = create_engine("sqlite:///db/hades.db", echo=True)

# try:

df.to_sql("advert", con=engine, if_exists="append", index=False)

# except:
# logger.error('error uploading data into sqllite')

# finally:
#   if engine:
#       engine.close


# data_list.append([item['itemId'][0],


#                         item['sellerInfo'][0]['feedbackScore'][0],
#                         item['sellerInfo'][0]['positiveFeedbackPercent'][0],

#                         item['shippingInfo'][0]['shipToLocations'][0],


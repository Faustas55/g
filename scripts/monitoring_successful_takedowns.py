import datetime
from sqlalchemy import create_engine
import pandas as pd
import glob 
import logging
import re
import json
import requests
import time
import pymysql
import credentials
pymysql.install_as_MySQLdb()
#from configforbackup import username, password, database

def set_logging(name,level):
    logger=logging.getLogger(name)
    logger.setLevel(level)
    filelog = logging.FileHandler('takedown.log')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',datefmt='%m/%d/%Y %I:%M:%S %p')
    filelog.setFormatter(formatter)
    logger.addHandler(filelog)
    return(logger)


logger=set_logging('TAKEDOWN DATA','INFO')

try:
    sqlengine = create_engine('mysql://'+ credentials.username +":" + credentials.password +"@localhost/"+ credentials.database)
    dbConnection = sqlengine.connect()
except MySQLdb.OperationalError as error:
    logger.error(f'can not create engine:{error} ')

def keyword_mlAPI(site_id,keywords):
    # Creates variables for pagination
    data_list = list()
    # Pagination variables
    offset = 0
    total = 0
            
    # Paginates through pages of items    
    while total >= offset:
            
        time.sleep(1)
            
        # Creates the request url
        url = 'https://api.mercadolibre.com/sites/' + site_id + '/search?q=' + keywords + '&offset=' + str(offset)
            
        # Converts json reply to data
        data = json.loads(requests.get(url).content)
                
         # Adds response items to list
        items = data['results']
                
            # Adds item fields to dataframe
        try:
            for item in items:
                time.sleep(0.5)
                seller_id = item['seller']['id']
                url_seller = 'https://api.mercadolibre.com/users/'+ str(seller_id)
                data_seller = json.loads(requests.get(url_seller).content)
                        
                data_list.append([item['id'],
                            item['title'],
                            item['price'],
                            item['currency_id'],
                            item['available_quantity'],
                            item['sold_quantity'],
                            data_seller['nickname'],
                            item['seller_address']['state']['name'] + ', ' + item['seller_address']['city']['name'],
                            data_seller['country_id'],
                            data_seller['seller_reputation']['transactions']['ratings']['positive']*100,
                            data_seller['registration_date'][0:10],
                            item['permalink'],
                            ]) 
                            
                        
                # Gets total number of pages for search
                total = data['paging']['total']
                    
                # Increases page counter by one for pagination
                offset += data['paging']['limit']
        except KeyError:
            break

    df = pd.DataFrame(data_list, columns=['itemno','product','price','cur','stock','sold','seller','seller_location','seller_country','seller_rating','seller_register','url'])
    
    return df
def mltakedowns():

    """
    function that takes daily MercadoLibre API (all countries) results and compares them to ads sent to infringement enforcement
    
    Args:
        none
    
    Returns:
        pd dataframe only with ads that DO NOT appear on Mercadolibre
        
    """

    #defining path and only picking up files with today's date
    path= r'C:\Splunk\online\ml_api'
    today_string = datetime.datetime.today().strftime('%d-%m-%Y')
    all_files=glob.glob(path + "/*" + today_string + ".csv")
    #appending data to list
    li = []
    for filename in all_files:
        df = pd.read_csv(filename, index_col=None, header=0)
        li.append(df)
        
    #list to dataframe
    mlAPI = pd.concat(li, axis=0, ignore_index=True)

    #get hades results
    hadessql="SELECT product, advert_id, url, domain, review, country FROM hades.advert WHERE category='takedown' AND review='Successful Takedown'"
    frame = pd.read_sql(hadessql, dbConnection)
    
    #select rows that begin with www.mercadolibre
    mlads = frame[frame['domain'].apply(lambda x: x.startswith('www.mercadolibre'))]

    random_fifty=mlads.sample(n=10)
    #compare hades vs API results
    relisted_takedowns_API_bulk = mlads[(mlads['url'].isin(mlAPI['url']))].reset_index(drop=True)

    relisted_random_takedowns = relisted_takedowns_API_bulk.append(random_fifty)
    #sending these to additionalML function to re-run the search using the product title
    relisted_takedowns_custom_search=additionalCheckML(relisted_random_takedowns)
    #compare new ads with the initial list
    relisted_takedowns_ML = relisted_random_takedowns[(relisted_random_takedowns['url'].isin(relisted_takedowns_custom_search['url']))].reset_index(drop=True)

    return  relisted_takedowns_ML, mlAPI

def additionalCheckML(additional_check_df):
    #remove all special characters
    additional_check_df['product'] = additional_check_df['product'].str.lower().str.split().apply(lambda x: [re.sub(r'\W+',' ', y) for y in x])
    #splitting strings based on whitespaces, but this creates lists within a list
    additional_check_df['product'] = additional_check_df['product'].apply(lambda x: [re.split('\s+', s) for s in x])  
    #flattening the list
    additional_check_df['product'] = additional_check_df['product'].apply(lambda x: [item for sublist in x for item in sublist])  
    #list to strings
    additional_check_df['product'] = [','.join(map(str, l)) for l in additional_check_df['product']]

    #replaces commas with " "
    additional_check_df['product'] = additional_check_df['product'].str.replace(","," ")
    
    list_product = additional_check_df['product'].tolist()
    list_country = additional_check_df['country'].tolist()

    appended_data=[]

    for product, country in zip(list_product, list_country):
        if country == "Honduras":
            site_id = 'MHN'
            keywords = "\""  + "[" + product + "]" + "\""
            individualMLsearch = keyword_mlAPI(site_id, keywords)
            appended_data.append(individualMLsearch)
        
        elif country == 'El Salvador':
            site_id = 'MSV'
            keywords = "\""  + "[" + product + "]" + "\""
            individualMLsearch = keyword_mlAPI(site_id, keywords)
            appended_data.append(individualMLsearch)

        elif country == 'Dominica':
            site_id = 'MRD'
            keywords = "\""  + "[" + product + "]" + "\""
            individualMLsearch = keyword_mlAPI(site_id, keywords)
            appended_data.append(individualMLsearch)
            
        elif country == 'Colombia':
            site_id = 'MCO'
            keywords = "\""  + "[" + product + "]" + "\""
            individualMLsearch = keyword_mlAPI(site_id, keywords)
            appended_data.append(individualMLsearch)

        elif country == 'Venezuela':
            site_id = 'MLV'
            keywords = "\""  + "[" + product + "]" + "\""
            individualMLsearch = keyword_mlAPI(site_id, keywords)
            appended_data.append(individualMLsearch)
            
        elif country == 'Ecuador':
            site_id = 'MEC'
            keywords = "\""  + "[" + product + "]" + "\""
            individualMLsearch = keyword_mlAPI(site_id, keywords)
            appended_data.append(individualMLsearch)
            
            
        elif country == 'Nicaragua':
            site_id = 'MNI'
            keywords = "\""  + "[" + product + "]" + "\""
            individualMLsearch = keyword_mlAPI(site_id, keywords)
            appended_data.append(individualMLsearch)
            

        elif country == 'Bolivia':
            site_id = 'MBO'
            keywords = "\""  + "[" + product + "]" + "\""
            individualMLsearch = keyword_mlAPI(site_id, keywords)
            appended_data.append(individualMLsearch)
            

        elif country == 'Argentina':
            site_id = 'MLA'
            keywords = "\""  + "[" + product + "]" + "\""
            individualMLsearch = keyword_mlAPI(site_id, keywords)
            appended_data.append(individualMLsearch)
            
            
        elif country == 'Chile':
            site_id = 'MLC'
            keywords = "\""  + "[" + product + "]" + "\""
            individualMLsearch = keyword_mlAPI(site_id, keywords)
            appended_data.append(individualMLsearch)
            

        elif country == 'Mexico':
            site_id = 'MLM'
            keywords = "\""  + "[" + product + "]" + "\""
            individualMLsearch = keyword_mlAPI(site_id, keywords)
            appended_data.append(individualMLsearch)
            
            
        elif country == 'Paraguay':
            site_id = 'MPY'
            keywords = "\""  + "[" + product + "]" + "\""
            individualMLsearch = keyword_mlAPI(site_id, keywords)
            appended_data.append(individualMLsearch)

        elif country == 'Peru':
            site_id = 'MPE'
            keywords = "\""  + "[" + product + "]" + "\""
            individualMLsearch = keyword_mlAPI(site_id, keywords)
            appended_data.append(individualMLsearch)
            
        elif country == 'Guatemala':
            site_id = 'MGT'
            keywords = "\""  + "[" + product + "]" + "\""
            individualMLsearch = keyword_mlAPI(site_id, keywords)
            appended_data.append(individualMLsearch)
        
        elif country == 'Brazil':
            site_id = 'MLB'
            keywords = "\""  + "[" + product + "]" + "\""
            individualMLsearch = keyword_mlAPI(site_id, keywords)
            appended_data.append(individualMLsearch)
            

        elif country == 'Panama':
            site_id = 'MPA'
            keywords = "\""  + "[" + product + "]" + "\""
            individualMLsearch = keyword_mlAPI(site_id, keywords)
            appended_data.append(individualMLsearch)
            
        elif country == 'Uruguay':
            site_id = 'MLU'
            keywords = "\""  + "[" + product + "]" + "\""
            individualMLsearch = keyword_mlAPI(site_id, keywords)
            appended_data.append(individualMLsearch)
            
        elif country == 'Costa Rica':
            site_id = 'MCR'
            keywords = "\""  + "[" + product + "]" + "\""
            individualMLsearch = keyword_mlAPI(site_id, keywords)
            appended_data.append(individualMLsearch)
        else:
            raise Exception('ML API not configured for country')
    appended_data = pd.concat(appended_data)
    return appended_data

def keyword_ebayAPI(globalId, keywords):
    """
    runs API to check ads that we don't find through our daily data download
    
    Args:
        globalId - Ebay's marketplace ID
        keywords - search term
    
    Returns:
        Results from EBAY API 
        
    """ 
    
    appkey = credentials.ebayappkey
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
        try:
            items = data["findItemsByKeywordsResponse"][0]["searchResult"][0]["item"]

            # create a dictionary and then create a dataframe

            # Adds item fields to dataframe
            for item in items:

                #get rid of items in wrong category

                item_dict = {}
                item_dict["product"] = item["title"][0]
                item_dict["seller"] = item["sellerInfo"][0]["sellerUserName"][0]
                item_dict["url"] = item["viewItemURL"][0]


                data_list.append(item_dict)

            # Gets total number of pages for search
            total = int(
                data["findItemsByKeywordsResponse"][0]["paginationOutput"][0]["totalPages"][0]
            )

            # Increases page counter by one for pagination
            page += 1
        except KeyError:
            break



    # Creates dataframe
    df = pd.DataFrame(data_list)

    return df 

def ebaytakedowns():
    
    """
    function that takes daily EBAY API (all countries) results and compares them to ads sent to infringement enforcement
    
    Args:
        none
    
    Returns:
        pd dataframe only with ads that DO NOT appear on EBAY
        
    """
    #defining path and only picking up files with today's date
    path= r'C:\Splunk\online\ebay_api'
    today_string = datetime.datetime.today().strftime('%d-%m-%Y')
    all_files=glob.glob(path + "/*" + today_string + ".csv")
    #appending data to list
    li = []
    for filename in all_files:
        df = pd.read_csv(filename, index_col=None, header=0)
        li.append(df)
        
    #list to dataframe
    ebayAPI = pd.concat(li, axis=0, ignore_index=True)
    #get hades results
    hadessql="SELECT product, advert_id, url, domain, review, country FROM hades.advert WHERE category='takedown' AND review='Successful Takedown'"
    frame = pd.read_sql(hadessql, dbConnection)
    #select rows that begin with www.ebay
    ebayads = frame[frame['domain'].apply(lambda x: x.startswith('www.ebay'))]
    #random 50 successful takedowns that will be re-run through the API
    random_fifty=ebayads.sample(n=50)
    #compare hades against EBAY api
    relisted_takedowns_API_bulk = ebayads[(ebayads['url'].isin(ebayAPI['url']))].reset_index(drop=True)

    relisted_random_takedowns = relisted_takedowns_API_bulk.append(random_fifty)
 
    
    #sending these to additionalCheckEbay function to re-run the search using the product title
    relisted_takedowns_custom_search=additionalCheckEbay(relisted_random_takedowns)
    
    #compare new ads with the initial list
    relisted_takedowns = relisted_random_takedowns[(relisted_random_takedowns['url'].isin(relisted_takedowns_custom_search['url']))].reset_index(drop=True)
    return relisted_takedowns, ebayAPI

def additionalCheckEbay(additional_check_df):
    """
    some ads that we do not detect are sent to us by an external provider. This function calls an api and looks for
    seeds or product_brand=none ads to check if they are really taken down
    
    Args:
        pd dataframe only with ads that DO NOT appear on EBAY using our API results
    
    Returns:
        pd dataframe only with ads that DO NOT appear on EBAY, combination of our API results and specific searches
        
    """
    
    
    #remove all special characters
    additional_check_df['product'] = additional_check_df['product'].str.lower().str.split().apply(lambda x: [re.sub(r'\W+',' ', y) for y in x])
    #splitting strings based on whitespaces, but this creates lists within a list
    additional_check_df['product'] = additional_check_df['product'].apply(lambda x: [re.split('\s+', s) for s in x])  
    #flattening the list
    additional_check_df['product'] = additional_check_df['product'].apply(lambda x: [item for sublist in x for item in sublist])  
    #list to strings
    additional_check_df['product'] = [','.join(map(str, l)) for l in additional_check_df['product']]

    #replaces commas with " "
    additional_check_df['product'] = additional_check_df['product'].str.replace(","," ")
    
    list_product = additional_check_df['product'].tolist()
    list_country = additional_check_df['country'].tolist()

    appended_data=[]

    #assigns correct variables for API calls based on the country
    for product, country in zip(list_product, list_country):
            if country == "United States":
                globalId = "EBAY-US"
                keywords = "\""  + "(" + product + ")" + "\""
                individualEbaysearch = keyword_ebayAPI(globalId, keywords)
                appended_data.append(individualEbaysearch)
            
            elif country == "Canada":
                globalId = "EBAY-ENCA"
                keywords = "\""  + "(" + product + ")" + "\""
                individualEbaysearch = keyword_ebayAPI(globalId, keywords)
                appended_data.append(individualEbaysearch)
            elif country == "United Kingdom":
                globalId = "EBAY-GB"
                individualEbaysearch = keyword_ebayAPI(globalId, keywords)
                appended_data.append(individualEbaysearch)
            elif country == "Australia":
                globalId = "EBAY-AU"
                keywords = "\""  + "(" + product + ")" + "\""
                individualEbaysearch = keyword_ebayAPI(globalId, keywords)
                appended_data.append(individualEbaysearch)
            elif country == "Austria":
                globalId = "EBAY-AT"
                keywords = "\""  + "(" + product + ")" + "\""
                individualEbaysearch = keyword_ebayAPI(globalId, keywords)
                appended_data.append(individualEbaysearch)
            elif country == "Belgium":
                globalId = "EBAY-FRBE"
                keywords = "\""  + "(" + product + ")" + "\""
                individualEbaysearch = keyword_ebayAPI(globalId, keywords)
                appended_data.append(individualEbaysearch)
            elif country == "France":
                globalId = "EBAY-FR"
                keywords = "\""  + "(" + product + ")" + "\""
                individualEbaysearch = keyword_ebayAPI(globalId, keywords)
                appended_data.append(individualEbaysearch)
            elif country == "Germany":
                globalId = "EBAY-DE"
                keywords = "\""  + "(" + product + ")" + "\""
                individualEbaysearch = keyword_ebayAPI(globalId, keywords)
                appended_data.append(individualEbaysearch)
            elif country == "Italy":
                globalId = "EBAY-IT"
                keywords = "\""  + "(" + product + ")" + "\""
                individualEbaysearch = keyword_ebayAPI(globalId, keywords)
                appended_data.append(individualEbaysearch)
            elif country == "Netherlands":
                globalId = "EBAY-NL"
                keywords = "\""  + "(" + product + ")" + "\""
                individualEbaysearch = keyword_ebayAPI(globalId, keywords)
                appended_data.append(individualEbaysearch)
            elif country == "Spain":
                globalId = "EBAY-ES"
                keywords = "\""  + "(" + product + ")" + "\""
                individualEbaysearch = keyword_ebayAPI(globalId, keywords)
                appended_data.append(individualEbaysearch)
            elif country == "Switzerland":
                globalId = "EBAY-CH"
                keywords = "\""  + "(" + product + ")" + "\""
                individualEbaysearch = keyword_ebayAPI(globalId, keywords)
                appended_data.append(individualEbaysearch)
            elif country == "Hong Kong":
                globalId = "EBAY-HK"
                keywords = "\""  + "(" + product + ")" + "\""
                individualEbaysearch = keyword_ebayAPI(globalId, keywords)
                appended_data.append(individualEbaysearch)
            elif country == "India":
                globalId = "EBAY-IN"
                keywords = "\""  + "(" + product + ")" + "\""
                individualEbaysearch = keyword_ebayAPI(globalId, keywords)
                appended_data.append(individualEbaysearch)
            elif country == "Ireland":
                globalId = "EBAY-IE"
                keywords = "\""  + "(" + product + ")" + "\""
                individualEbaysearch = keyword_ebayAPI(globalId, keywords)
                appended_data.append(individualEbaysearch)
            elif country == "Malaysia":
                globalId = "EBAY-MY"
                keywords = "\""  + "(" + product + ")" + "\""
                individualEbaysearch = keyword_ebayAPI(globalId, keywords)
                appended_data.append(individualEbaysearch)
            elif country == "Philippines":
                globalId = "EBAY-PH"
                keywords = "\""  + "(" + product + ")" + "\""
                individualEbaysearch = keyword_ebayAPI(globalId, keywords)
                appended_data.append(individualEbaysearch)
            elif country == "Poland":
                globalId = "EBAY-PL"
                keywords = "\""  + "(" + product + ")" + "\""
                individualEbaysearch = keyword_ebayAPI(globalId, keywords)
                appended_data.append(individualEbaysearch)
            elif country == "Singapore":
                globalId = "EBAY-SG"
                keywords = "\""  + "(" + product + ")" + "\""
                individualEbaysearch = keyword_ebayAPI(globalId, keywords)
                appended_data.append(individualEbaysearch)
            else:
                raise Exception ('Ebay ID not configured for country')
    #append all dataframes received from 
    appended_data = pd.concat(appended_data)
    return appended_data



relisted_takedowns_ebay, ebayAPI,  = ebaytakedowns()
relisted_takedowns_ML, mlAPI, = mltakedowns()
def oneframe(ebay_takedowns,ml_takedowns):
    #making one dataframe out of two
    if ebay_takedowns.empty & ml_takedowns.empty:
        combined_takedowns=pd.DataFrame
    elif len(ebay_takedowns)!= 0 & ml_takedowns.empty:
        combined_takedowns=ebay_takedowns
    elif ebay_takedowns.empty & len(ml_takedowns)!=0:
        combined_takedowns=ml_takedowns
    else:
        combined_takedowns=ebay_takedowns.append(ml_takedowns, ignore_index=True)
    return combined_takedowns

combined_takedowns=oneframe(relisted_takedowns_ebay, relisted_takedowns_ML)
combined_takedowns=combined_takedowns.drop(columns=['product', 'country'])
combined_takedowns.set_index("advert_id", inplace=True)
if combined_takedowns.empty:
    logger.info('No relisted ads found')
    
else:
    connStr= sqlengine.connect().connection
    cursor = connStr.cursor()
    numberofads=0
    for id_advert in combined_takedowns.index:
        update_sql="""Update hades.advert SET review='Sent to CSC for Takedown' WHERE advert_id=%s"""
        cursor.execute(update_sql, id_advert)
        connStr.commit()
        delete_sql="""DELETE FROM hades.takedowns WHERE advert_id=%s"""
        cursor.execute(delete_sql, id_advert)
        connStr.commit()
        numberofads+=1

    cursor.close()
    connStr.close()


    logger.info('%s Relisted ads found' % numberofads)

        


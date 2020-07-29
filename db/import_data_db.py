# script to import data from the splunk online report
# into hades db on sqlite


# TODO Add a default for Type to distributer if null -RICH 



import sys
import datetime
import logging
import numpy as np
import pandas as pd
import sqlite3
from sqlalchemy import create_engine
from sqlalchemy.types import Integer, Text
from pathlib import Path

#set up database path 
path=Path.cwd()
db_path=path.joinpath('db', 'hades.db')
dbbak_path=path.joinpath('db', 'hades_backup.db')

#set up logging
def set_logging(name,level):
    logger=logging.getLogger(name)
    logger.setLevel(level)
    filelog = logging.FileHandler('hadesv2.log')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',datefmt='%m/%d/%Y %I:%M:%S %p')
    filelog.setFormatter(formatter)
    logger.addHandler(filelog)
    return(logger)


logger=set_logging('IMPORT DATA','INFO')


try:
    #opening a connection to the database. Update with a correct path directory
    MainCon=sqlite3.connect(db_path)
    #opening a connection to the backup file
    BackupCon=sqlite3.connect(dbbak_path)

except sqlite3.OperationalError as error:
    print('error -see log')
    logger.error(f'database has not been backed up: {error}')
    sys.exit()




    #backup


with BackupCon:
    MainCon.backup(BackupCon, pages=0)




#closing connections 
MainCon.close()
BackupCon.close()


try:
    engine = create_engine("sqlite:///db/hades.db", echo=True)
except sqlite3.OperationalError as error:
    logger.error(f'can not create engine:{error} ')

   

# we need to change this to collect the file from where splunk saves it. (I set Splunk to save the file every Monday 11:00am Basel time)
import_file = Path(r"C:\Program Files\Splunk\var\run\splunk\csv\splunk_online_output.csv")

# debugging and test purposes
#import_file = "C:\\temp\\online.csv"

#import filter that categorizes adds by brands and business
filter_brands=pd.read_csv( 
    Path.cwd().joinpath('db', 'filter.csv')
)
# importing a file with countries and regions that will be joined with the main database - F
df_region = pd.read_csv(
    Path.cwd().joinpath('db', 'regioncountry.csv'), keep_default_na=False, na_values=["_"]
)

# We can continue with this intially if we have problems importing with pandas we can use the GUI to import
export_file = Path.cwd().joinpath('db', 'online_transformed.csv')

# These are the columns only needed for the export to csv file
export_cols = [
    "advert_id",
    "region",
    "country",
    "product",
    "price",
    "cur",
    "seller",
    "category",
    "last_seen",
    "type",
    "domain",
    "url",
    "business",
    "product_brand",
    "date_found",
    "polonius_caseid",
    "updated_date",
    "updated_by",
    "firstname",
    "lastname",
    "type"
]


# we need to rename the columns as they are different in the splunk report , plus whilst
# merging new columns are created
rename_cols = {
    "Product_category_for_polonius": "product_brand",
    "Business_y": "business",
    "report_date": "date_found",
    "type_y": "cat",
    "region_y": "region",
    "country_y": "country",
    "price_y": "price",
    "cur_y": "cur",
    "category_y": "category",
    "last_seen_y": "last_seen",
    "url_y": "url",
    "SP_firstname_y":"SP_firstname",
    "SP_lastname_y":"SP_lastname",
    "product_brand_y":"product_brand"
}

# Lets drop all the useless columns from the merge and the splunk report
columns_drop = [
    "advert_id",
    "region_x",
    "country_x",
    "price_x",
    "cur_x",
    "category_x",
    "last_seen_x",
    "type_x",
    "url_x",
    "date_found",
    "polonius_caseid",
    "updated_date",
    "updated_by",
    "_merge",
    "SP_lastname_x",
    "SP_firstname_x",
    "keywords",
    "Business_x",
    "product_brand_x"
]
#dropping columns in df_categories immediately after merging
columns_dfcategories = [
    "suspected_counterfeiter",
    "no_action", 
    'uncategorised\nuncategorised', 
    'uncategorised', 
    'archived',
    'not relevant', 
    'syngenta authorised',
    'authorised',
    'takedown_x',
    'advert_id', 
    'region', 
    'country', 
    'product', 
    'price', 
    'cur',
    'category', 
    'last_seen', 
    'cat', 
    'domain', 
    'url', 
    'date_found',
    'business', 
    'product_brand', 
    'polonius_caseid', 
    'updated_date',
    'updated_by', 
    'type', 
    'SP_firstname', 
    'SP_lastname', 
    'comments',
    'uploaded_date'
]

# getting the advert table and convert into a dataframe ...
df_db = pd.read_sql("SELECT * FROM advert", engine)

#lets get the CS manager table as a df 
df_csm = pd.read_sql("SELECT SP_firstname,SP_lastname,country FROM CSM ",engine)

# read in the csv from splunk
df = pd.read_csv(import_file)
# print(df.head())

#set the default for type ..if null then set as Distributor
df['type']=df.apply(lambda x: 'distributor' if pd.isnull(x['type']) else x['type'],axis=1)


#grouping by sellers by their category and reseting the index so we are able to merge
df_groupedby=df_db.groupby(['seller','category']).size().unstack(level=1, fill_value=0).reset_index()
df_categories = df_db[["seller", "domain","category"]].copy()

#merging, dropping, and renaming the columns so it's easier later on when we join this with the main df
df_categories = pd.merge(df_db, df_groupedby, on="seller", how="right")
df_categories.drop(columns_dfcategories, axis=1, inplace=True)
df_categories.rename(columns={"no action":"no_action", "suspected counterfeiter":"suspected_counterfeiter", "takedown_y":"takedown"}, inplace=True) 
    
 #duplicating the product column which is then used to split the strings into keywords
df['keywords'] = df['product'].str.lower().str.split()

#comparing the filter with the keywords, if there's a hit it gets written into the 'product_brand' column as a list 
df['product_brand'] = df['keywords'].apply(lambda x: [item for item in x if item in filter_brands['product_brand'].tolist()])
# list transformed to string  
df['product_brand'] = df['product_brand'].apply(lambda x: ','.join(map(str, x)))

#deleting everything after a comma if there's another string. Only need 1 keyword for splunk dashboards,but leaving the option to have all keyword hits if we need     
df['product_brand'] = df['product_brand'].str.split(',').str[0]

#replacing all empty values with NaN that then get filled with 'None'
df = df.replace('', np.nan)
df['product_brand'].fillna(value="None", inplace=True)

#merging the filter with the brands to get business information
df=pd.merge(df, filter_brands, on="product_brand", how="left")
df['product_brand']=df['product_brand'].str.title()

#make sure the country is capitilised so there is only one country in the results =< Changed to str.title() to fix capitalization issues
df["country"]=df["country"].str.title()

# merging df with country and region database, renaming the column back into "region" - F
df = pd.merge(df, df_region, on="country", how="left")
df = df.rename(columns={"region_y": "region"})



#right lets add in to the df any responsible country security managers
df = pd.merge(df,df_csm,on="country", how="left")


# drop some more useless columns before we merge again
df.drop(["score", "set_category"], axis=1, inplace=True)

# merge so we only get new adverts .New adverts=new seller + domain + product
df_merge = df_db.merge(
    df, indicator=True, how="outer", on=["seller", "product", "domain"]
)



# take only the right sided ones . these are adverts that are not in the sqlite database ..i.e the new ones
df = df_merge[df_merge["_merge"] == "right_only"]

# check to see if we have any new adverts before proceeding
if not df.empty:
    # drop all the useless columns created by the merge .. i.e the adverts already in database
    df.drop(columns_drop, axis=1, inplace=True)
    

    # rename the columns so it fits the table fields in sqlite
    df = df.rename(columns=rename_cols)
    # merging the seller statistics with the main df
    df= pd.merge(df, df_categories, on=['seller'], how="left")
    df.rename(columns={'no_action_y':'no_action', 'suspected_counterfeiter_y':'suspected_counterfeiter', 'takedown_y':'takedown'}, inplace=True)
    #adds no action all and no action together
    #df['no_action'] = df['no_action'] + df['no_action_all']
    df.drop(columns=['no_action_x', 'takedown_x', 'suspected_counterfeiter_x', 'set_category'], axis=1, inplace=True)
    df.drop_duplicates(subset=['url','domain'],inplace=True)
    # fillna so we get a numerical value instead of none
    df[['no_action', 'suspected_counterfeiter','takedown']]=df[['no_action', 'suspected_counterfeiter','takedown']].fillna(value=0)

    #get rid of duplicates 
    df.drop_duplicates(subset=['seller','domain','product'],inplace=True)
    

    logger.info('number of new cases to upload %s',df.shape[0])
    
    # set category to lowercase
    df["category"] = df["category"].str.lower()
  

    # this is for SQLite rowid which is a primary key, send in a null object and sqlite will sort this out
    df.loc[:, "advert_id"] = None

    # make polonius_caseid null
    df.loc[:, "polonius_caseid"] = None

    # set that the "upload user " has updated
    df.loc[:, "updated_by"] = "upload"
    # and when uploaded
    df.loc[:, "uploaded_date"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    

    
    #make sure the country is capitilised so there is only one country in the results
    df["country"]=df["country"].str.title()

    # get rid of non -relevant sellers adverts

    df=df[df['category'] != 'not relevant']

    # write out the csv to be uploaded ..this is now just a backup
   
    #df.to_csv(export_file, index=False, columns=export_cols)
    # write the adverts back to the table "advert" as one big hit
    
    try:
        df.to_sql(
            "advert",
            con=engine,
            if_exists="append",
            index=False,
            dtype={"business": Text(), "product_brand": Text()},
        )

    except sqlite3.Error as error:
        logger.error(f"error uploading adverts to SQLlite :{error}")
        print('error please check log')
else:
    logger.info("No new adverts found ")
    print('no new adverts')

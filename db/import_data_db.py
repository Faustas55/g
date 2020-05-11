#script to import data from the splunk online report 
# into hades db on sqlite 
#TODO write a script to automatically upload the data into the database 
#TODO remeber when importing data make sure to use UTF-8 specified and not system
#TODO run an Sqlite backup before import

#TODO add in a region if none 


import pandas as pd
import numpy as np
import datetime

import_file='c:\sqlite\db\online.csv'
export_file='c:\sqlite\db\online_transformed.csv'


export_cols=['advert_id','region', 'country', 'product', 'price', 'cur', 'seller',
       'category', 'last_seen', 'type', 'domain', 'url',
       'date_found', 'business', 'product_brand','polonius_caseid','updated_date','updated_by']

rename_cols={'Product_category_for_polonius':'product_brand','Business':'business',
                    'report_date':'date_found','cat':'type'
            }

#read in the csv
df=pd.read_csv(import_file)
print(df.head())



#drop the useless columns 
df.drop(['score','set_category'], axis=1,inplace=True)

#this is for SQLite rowid , it will just update the row id automatically 
df['advert_id']='NULL'


#make polonius_caseid null
df['polonius_caseid']='NULL'
df['updated_by']='upload'
df['updated_date']=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
df=df.rename(columns=rename_cols)

                
#write out the csv to be uploaded
df.to_csv(export_file,index=False, columns=export_cols )

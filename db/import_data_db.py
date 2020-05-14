#script to import data from the splunk online report 
# into hades db on sqlite 

#TODO remeber when importing data make sure to use UTF-8 specified and not system
#TODO run an Sqlite backup before import

#TODO add in a region if none 


import pandas as pd
import numpy as np
import datetime
from sqlalchemy.types import Integer,Text
from sqlalchemy import create_engine
engine = create_engine('sqlite:///HadesV2App/db/hades.db', echo=True)

df_db=pd.read_sql('SELECT * FROM advert', engine)


#we need to change this to collect the file from where splunk saves it 
import_file='c:\sqlite\db\online.csv'

#We can continue with this intially if we have problems importing with pandas we can use the GUI to import
export_file='c:\sqlite\db\online_transformed.csv'


export_cols=['advert_id','region', 'country', 'product', 'price', 'cur', 'seller',
       'category', 'last_seen', 'cat', 'domain', 'url',
       'date_found', 'business', 'product_brand','polonius_caseid','updated_date','updated_by']

rename_cols={'Product_category_for_polonius':'product_brand','Business':'business',
                    'report_date':'date_found','cat_y':'cat','region_y':'region', 'country_y':'country', 
                    'price_y':'price','cur_y':'cur', 'category_y':'category', 'last_seen_y':'last_seen', 'url_y':'url'
            }

columns_drop=['advert_id', 'region_x', 'country_x', 'price_x', 'cur_x',
               'category_x', 'last_seen_x', 'cat_x', 'url_x',
              'date_found', 'business', 'product_brand', 'polonius_caseid',
                     'updated_date', 'updated_by','_merge']


#read in the csv
df=pd.read_csv(import_file)
print(df.head())


#drop the useless columns 
df.drop(['score','set_category'], axis=1,inplace=True)

#merge so we only get new adverts .New adverts=new seller + domain + product
df_merge=df_db.merge(df,indicator=True,how='outer',on=['seller','product','domain'])
print(df_db.shape)
print(df.shape)
print()
print(df_merge[df_merge['_merge']=='right_only'].shape)
#print (df_merge['_merge'].value_counts())
#print (df_merge.columns)

#take only the right sided ones ..i.e the new ones which have got from the merge
df=df_merge[df_merge['_merge']=='right_only']
df.drop(columns_drop,axis=1,inplace=True)


#this is for SQLite rowid , it will just update the row id automatically 
df.loc[:,'advert_id']=None


#make polonius_caseid null
df.loc[:,'polonius_caseid']=None

df.loc[:,'updated_by']='upload'
df.loc[:,'updated_date']=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
df=df.rename(columns=rename_cols)
print(df.columns)
                
#write out the csv to be uploaded
df.to_csv(export_file,index=False, columns=export_cols, )

df.to_sql('advert', con=engine, if_exists='append',
          index=False,dtype={"business": Text(),"product_brand":Text()})
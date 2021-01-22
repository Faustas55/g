#script to monitor out of stock urls for reactivation 
#uses scrapy to look for the out of stock message in page HTML 
#pages obtained from hades mysql 
#if out of stock message not found update hades category=uncategorised 
#richard hyams 2021



from typing import ContextManager
import mysql.connector
import scrapy
import config
import datetime
import contextlib

from scrapy.crawler import CrawlerProcess
from scrapy.spidermiddlewares.httperror import HttpError


###STOP SQL INJECTION ######
#escape the vlaues of the query for update#
uncategorised='uncategorised'
noaction='no action'
uploaddate=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
user='upload'
outofstockcat='Outofstock/Paused'

# **********CONFIGURATION******************* 
# how the script decides if an advert is 404 or the advert has ended - 
# Please add other languages and terms in list below !
searchTerms=['end','terminee', 'No disponible','Not availiable']

## class customised for finding the out of stock -ebay and pasued adverts mercadolibra
class AdvertSpider(scrapy.Spider):

    name='adverts'

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 ',
        'DOWNLOAD_DELAY' :1.5,
        'AUTOTHROTTLE_ENABLED' :True,
        'AUTOTHROTTLE_START_DELAY' : 2,
        'AUTOTHROTTLE_TARGET_CONCURRENCY': 6,
    }

    def start_requests(self):
        
        'urls is defined outside of class'
        for dict in urls:
            advert_id=dict['advert_id']
            url=dict['url']
            
            yield scrapy.Request(url=url,callback=self.parse,errback=self.errback,meta={'advert_id':advert_id},dont_filter=True)

            

                
           

# This is where you add sites and the css so they can be monitored #
#if we start getting a lot of sites will make the def more genralised #

    def parse(self, response):
        
        
        msg='Out of Stock'
        
        #404 response e.g lazarda
        if response.status==404:
            msg='NotFound'

        elif 'ebay' in response.url:
            msg=response.css('span.msgTextAlign::text').get()
        
        elif 'mercadolibre' in response.url:
            msg=response.css('p.item-status-notification__title::text').get()

        elif 'amazon' in response.url:
            msg=response.css('span.a-size-medium.a-color-price::text').get()

        else:
            #any website not in the above checks put back to uncategorised
            msg=None
        
        msg_dict[response.meta['advert_id']]=msg

       
       
       
       

    def errback(self, failure):

        if failure.check(HttpError):
            
            msg_dict[failure.request.meta['advert_id']]='NotFound'




@contextlib.contextmanager
def get_db_connection():

    """
    function to get a mysql database connection 

    Args:
        none

    Returns:
        mysql database connection  


    """

    mydb=mysql.connector.connect(
    host=config.host,
    user=config.username,
    password=config.password ,
    database=config.database

    )

    yield mydb


    mydb.close()





def update_db(sql):
    """
    function to update mysql database

    Args:
        sql(str): sql to update the database

    Returns:
        rows (int): number of rows affected by sql statement  


    """
    with get_db_connection() as mydb:
        mycursor=mydb.cursor()
        mycursor.execute(sql)
        mydb.commit()
        rows= mycursor.rowcount
        mycursor.close()
        return rows



def get_outofstock_adverts(sql):
    """
    function to slect all out of stock adverts

    Args:
        sql(str): sql to select from  the database

    Returns:
        dictionary: items retrieved from the select statement 


    """
    with get_db_connection() as mydb:

        mycursor=mydb.cursor(dictionary=True)

        mycursor.execute(sql)
 
        return mycursor.fetchall()
    




#set up the dictionary outside of class so can pass back the message :-) (strings or lists do not work for some reason)
msg_dict=dict()


#obtain list of urls from hades (where category=out of stock\paused)
urls=get_outofstock_adverts(f"select url,advert_id from advert where category='{outofstockcat}'")
urls=urls[0:10]

#run the spider
process=CrawlerProcess()
process.crawl(AdvertSpider)
process.start()


#check to see if there is no message if so then update status to uncategorised else if not found put to no action and put in comments that is was out of stock 

for key,value in msg_dict.items():
    #out of stock message has gone 
    if value=='' or value ==None:
        comments=f'\\n This advert was being monitored (out of stock) category changed to {uncategorised}'
        rows=update_db(f"update advert set category='{uncategorised}',updated_by='{user}',updated_date='{uploaddate}',comments=CONCAT_WS('',comments,'{comments}') where advert_id='{key}'")

    #404 type situation 
    # listing ended properly not just paused \out of stock    
    elif (value=='NotFound') or list(filter(lambda x:x in value,searchTerms)):
        comments=f'\\n This advert was being monitored (out of stock) but not found or has ended. Category changed to {noaction}'
        rows=update_db(f"update advert set category='{noaction}',updated_by='{user}',updated_date='{uploaddate}',comments=CONCAT_WS('',comments,'{comments}') where advert_id='{key}'")

    
    


    # if none of the conditions aboved true then advert is out of stock \paused \not availiable etc to be tested again e.g next week
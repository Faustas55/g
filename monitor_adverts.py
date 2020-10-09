#script to monitor out of stock urls for reactivation 
#uses scrapy to look for the out of stock message in page HTML 
#pages obtained from hades mysql 
#if out of stock message not found update hades category=uncategorised 
#richard hyams 2020



import mysql.connector
import scrapy
import config

from scrapy.crawler import CrawlerProcess

class AdvertSpider(scrapy.Spider):

    name='adverts'

    def start_requests(self):
        

        for dict in urls:
            advert_id=dict['advert_id']
            url=dict['url']
            yield scrapy.Request(url=url,callback=self.parse,meta={'advert_id':id})


    def parse(self, response):
        
        msg=response.css('span.msgTextAlign::text').get()
        msg_dict[response.meta['advert_id']]=msg
              




def get_outofstock_adverts():

    mydb=mysql.connector.connect(
    host=config.host,
    user=config.username,
    password=config.password ,
    database=config.database

    )

    mycursor=mydb.cursor(dictionary=True)

    mycursor.execute("select url,advert_id from advert where category='Outofstock/Paused'")
 
    return mycursor.fetchall()
    




#set up the dictionary outside of class so can pass back the message :-) (strings or lists do not wor for some reason)

msg_dict=dict()


#obtain list of urls from hades (where category=out of stock)
urls=get_outofstock_adverts()




#urls=['https://www.ebay.com/itm/Advion-Roach-Cockroach-Killer-Bait-Gel-4-Tubes-Free-Tips-Plunger/154078345940?hash=item23dfc8fad4:g:1-kAAOSwKWJfVuZt']



#run the spider
process=CrawlerProcess()
process.crawl(AdvertSpider)
process.start()


#check to see if there is no message if so then update status to uncategorised and put in comments that is was out of stock 

for key,value in msg_dict.items():
    if value=='' or value ==None:
        #update the database for that adver_id 
        pass



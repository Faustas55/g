import scrapy

from scrapy.crawler import CrawlerProcess

class AdvertSpider(scrapy.Spider):

    name='adverts'

    def start_requests(self):
        urls=['https://www.ebay.com/itm/Advion-Roach-Cockroach-Killer-Bait-Gel-4-Tubes-Free-Tips-Plunger/154078345940?hash=item23dfc8fad4:g:1-kAAOSwKWJfVuZt']

        for url in urls:
            yield scrapy.Request(url=url,callback=self.parse)


    def parse(self,response):
        
        msg=response.css('span.msgTextAlign::text').get()
        msg_dict['msg']=msg
              


#set up the dictionary outside of class so can pass back the message :-) (strings or lists do not wor for some reason)

msg_dict=dict()


#run the spider
process=CrawlerProcess()
process.crawl(AdvertSpider)
process.start()


print(msg_dict)

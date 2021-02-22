from selenium import webdriver
from time import sleep
from mysql_utils import get_adverts

#variables to select the relevant adverts 

site='%mercadolibre%'
review='Sent to CSC for Takedown'
fromdate ='2021-01-01'

#set up directory
dir='c:\\temp\\screenshots'


#set up headless chrome browser 
options = webdriver.ChromeOptions() 
options.add_argument("headless")
driver = webdriver.Chrome(chrome_options=options)



#get mercadolibre list from database = takedowns
adverts=get_adverts(f"select url,advert_id,updated_date,category from advert where domain like '{site}' and review='{review}' and updated_date >= '{fromdate}' ")


#setup the unique name  


#for each mercadolibre link get a screenshot 


driver.get('https://articulo.mercadolibre.com.mx/MLM-712227134-advion-mata-cucarachas-30g-efectivo-veneno-gel-jeringa-_JM')
sleep(3)

#S = lambda X: driver.execute_script('return document.body.parentNode.scroll'+X)
driver.set_window_size(2000,5000) # May need manual adjustment                                                                                                                
driver.find_element_by_tag_name('body').screenshot('c:\\temp\\screenshots\\web_screenshot.png')

#update the database with nameofscreenshot 

driver.quit()
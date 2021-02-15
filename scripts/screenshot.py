from selenium import webdriver
from time import sleep
from mysql_utils import get_mysql_connection


def get_adverts_for_screenshot(sql):
    """
    function to slect all out of stock adverts

    Args:
        sql(str): sql to select from  the database

    Returns:
        dictionary: items retrieved from the select statement 


    """
    with get_mysql_connection() as mydb:

        mycursor=mydb.cursor(dictionary=True)

        mycursor.execute(sql)
 
        return mycursor.fetchall()
    



takedown='takedown'
site='mercadolibre'

#set up directory
dir='c:\\temp\\'


#set up headless chrome browser 
options = webdriver.ChromeOptions() 
options.add_argument("headless")
driver = webdriver.Chrome(chrome_options=options)

#get mercadolibre list from database = takedowns
adverts=get_adverts_for_screenshot(f"select url,advert_id from advert where category='{takedown}'")


#setup the unique name 


#for each mercadolibre link get a screenshot 


driver.get('https://articulo.mercadolibre.com.mx/MLM-712227134-advion-mata-cucarachas-30g-efectivo-veneno-gel-jeringa-_JM')
sleep(3)

#S = lambda X: driver.execute_script('return document.body.parentNode.scroll'+X)
driver.set_window_size(2000,5000) # May need manual adjustment                                                                                                                
driver.find_element_by_tag_name('body').screenshot('c:\\temp\\web_screenshot.png')

#update the database with nameofscreenshot 

driver.quit()
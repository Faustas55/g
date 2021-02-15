from selenium import webdriver
from time import sleep


#set up directory
dir=

#set up headless chrome browser 
options = webdriver.ChromeOptions() 
options.add_argument("headless")
driver = webdriver.Chrome(chrome_options=options)

#get mercadolibre list from database = takedowns

#setup the unique name 


#for each mercadolibre link get a screenshot 


driver.get('https://articulo.mercadolibre.com.mx/MLM-712227134-advion-mata-cucarachas-30g-efectivo-veneno-gel-jeringa-_JM')
sleep(3)

#S = lambda X: driver.execute_script('return document.body.parentNode.scroll'+X)
driver.set_window_size(2000,5000) # May need manual adjustment                                                                                                                
driver.find_element_by_tag_name('body').screenshot('c:\\temp\\web_screenshot.png')

#update the database with nameofscreenshot 

driver.quit()
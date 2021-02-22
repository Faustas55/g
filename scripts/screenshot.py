from selenium import webdriver
from time import sleep
from mysql_utils import get_adverts
import os

from random import randint


def lst_find_dupl(list1,list2):
    """
    function to find the duplicates in the list and return the duplicates 
    or non duplicates matches between the lists

    Args:
        list(strings(list1)): list of strings to compare 
        list(strings(list2)): list of strings to compare
        

    Returns:
        list(items_dup) : items that match between two lists
        list(items_nondup) : items that do not match between two lists

    """
    items_dup=[]
    items_nondup=[]
    for item in list1:
            if item in list2:
                items_dup.append(item)
            else: 
                items_nondup.append(item)
    
    return items_dup,items_nondup        


    


#variables to select the relevant adverts 

site='%mercadolibre%'
review='Sent to CSC for Takedown'
fromdate ='2021-01-01'

#set up directory to add in screenshots 
dir='c:\\temp'
path=os.path.join(dir,'screenshots')

#keep a list of already done screenshots to stop repeating 
files=[]

#set up headless chrome browser to render the pages before screenshots
options = webdriver.ChromeOptions() 
options.add_argument("headless")
driver = webdriver.Chrome(chrome_options=options)



#get mercadolibre list from database = takedowns
adverts=get_adverts(f"select url,advert_id from advert where domain like '{site}' and review='{review}' and updated_date >= '{fromdate}' ")

#has it already been screenshotted in the past ?
# get list of file names 
with os.scandir(path) as listOfEntries:
    for entry in listOfEntries:
        # print all entries that are files
        if entry.is_file():
            files.append(entry.name.strip('.png'))

#check files against advert ids 

advert_ids=[str(dict['advert_id']) for dict in adverts]

lst_dupl,lst_non_dupl=lst_find_dupl(advert_ids,files)  

#for each mercadolibre link get a screenshot 

for dict in adverts:

    url,advert_id = dict.values()
    
    if str(advert_id) in lst_non_dupl:
        driver.get(url)
        sleep(randint(2, 10))

    #S = lambda X: driver.execute_script('return document.body.parentNode.scroll'+X)
        driver.set_window_size(2000,5000) # May need manual adjustment                                                                                                                
        driver.find_element_by_tag_name('body').screenshot(os.path.join(path,str(advert_id)+'.png'))
        print(f'Advert {advert_id} screenshotted and saved as {str(advert_id)+".png"}')

driver.quit()
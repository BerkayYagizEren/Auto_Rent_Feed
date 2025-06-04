import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup
import requests


RENTAL_LIST_WEBSITE='https://appbrewery.github.io/Zillow-Clone/'
GOOGLE_FORM_LINK='https://docs.google.com/forms/d/e/1FAIpQLScP2fkXhSedqTI7_eFKzfS4BJ2bApDflIpnTkinhlZDCo5CAA/viewform?usp=dialog'
INDEX=0

data=requests.get(RENTAL_LIST_WEBSITE)
soup=BeautifulSoup(data.text,'html.parser')


website_address_list=soup.select(selector='.StyledPropertyCardPhotoBody a')
#print(i.get('href'))
price_list=soup.find_all(class_='PropertyCardWrapper__StyledPriceLine')
#print(i.text)
address_list=soup.select(selector='address')
#print(i.text.strip())
my_dict={}
for j in range(len(address_list)):
    my_dict[j]={}


for i in range(len(address_list)):
    my_dict[i]['website_address']=website_address_list[i].get('href').strip()
    my_dict[i]['address']=address_list[i].text.strip()
    try:
        my_dict[i]['price'] = int(price_list[i].text[1:6].replace(',', ''))
    except:
        my_dict[i]['price'] = int(price_list[i].text[1:6].replace('+', ''))



options=webdriver.ChromeOptions()
options.add_experimental_option('detach',True)

website=webdriver.Chrome(options=options)
website.get(GOOGLE_FORM_LINK)


while INDEX<len(website_address_list):
    time.sleep(2)
    address_of_property = website.find_elements(By.CLASS_NAME, 'zHQkBf')[0]

    price_per_month = website.find_elements(By.CLASS_NAME, 'zHQkBf')[1]

    link = website.find_elements(By.CLASS_NAME, 'zHQkBf')[2]

    send_button = website.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span')

    address_of_property.send_keys(my_dict[INDEX]['address'])
    price_per_month.send_keys(my_dict[INDEX]['price'])
    link.send_keys(my_dict[INDEX]['website_address'])
    send_button.click()
    time.sleep(2)
    send_another_message = website.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
    send_another_message.click()
    INDEX+=1












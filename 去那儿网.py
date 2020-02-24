#注意：去那儿网机票价格在pc端中是变化的，可以通过破解css进行反爬。
# 但是子m端，机票价格并为加密，可以直接爬取。附上m端的网址https://m.flight.qunar.com/ncs/page/flightlist?

import pymongo
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
browser=webdriver.Firefox()
browser.get('https://www.qunar.com/?ex_track=auto_4e0d874a')
dict_data={}
def get_requests():
    input=WebDriverWait(browser,5).until(EC.presence_of_element_located((By.XPATH,'//input[@class="cinput textbox"]')))
    input.send_keys('成都')
    input.send_keys(Keys.ENTER)
    browser.find_element_by_xpath('//button[@class="button-search"]').click()

    browser.implicitly_wait(5)#需要等待时间，否则容易没有数据
    destnation = browser.find_elements_by_xpath('//div[@class="a-city"]')
    date=browser.find_elements_by_xpath('//span[@class="date"]')
    price=browser.find_elements_by_xpath('//div[@class="a_low_prc js-all-pr"]')

    #价格转换，price_b是网页显示的价格和源代码隐藏的价格的集合。
    #price_after是网页显示的价格，转换为列表方便替换
    for i in range(len(price)):
        price_b=price[i].find_elements_by_xpath('.//b[contains(@style,"left:")]')
        price_after=list(price_b[0].text)
        print('price_b[0]',price_b[0].text)
        for item in price_b:
            b_attr=item.get_attribute('style')
            if b_attr == 'left: -64px;':#替换网页价格的第一位数字
                price_after[0] = item.text
            elif b_attr == 'left: -48px;':#替换网页价格的第二位数字
                price_after[1]=item.text
            elif b_attr == 'left: -32px;':#替换网页价格的第三位数字
                price_after[2] = item.text
            elif b_attr == 'left: -16px;':#替换网页价格的第四位数字
                price_after[3] = item.text
        print(price_after)
        data={
            'destnation':destnation[i].text,
            'date':date[i].text,
            'price':''.join(str(i) for i in price_after)
        }
        save(data)

def save(data):
    MONGO_DB='localhost'
    MONGO_TABLE='去那儿网'
    client=pymongo.MongoClient(MONGO_DB)
    db=client[MONGO_TABLE]
    db['机票价格'].insert(data)

get_requests()

from pandas import DataFrame
from requests import get
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from pandas import DataFrame, read_excel, concat, ExcelWriter, NA


def init_browser():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('--no-sandbox')
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument('--disable-blink-features=AutomationControlled')
    # s = Service('/usr/bin/google-chrome-stable') #('/root/bot/pachka-bot/chromedriver-linux64/chromedriver')
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)#, service=s)
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
    })
    return driver


def check():
    answer = ''
    comp_df = read_excel(f'./data/table.xlsx')
    comp_list = comp_df.to_dict('records')
    driver = init_browser()

    for comp in comp_list:
        name = comp['name']
        url = comp['link']
        price = comp['price']

        trying = 0
        while trying != 5:
            driver.get(url)
            sleep(trying+1)
            html = driver.page_source
        
            soup = BeautifulSoup(html)
            
            try:
                comp_price = soup.findAll('div', class_='priceBlockPriceWrap--G4F0p priceBlockPriceWrapWallet--rjb9S')[0].get_text() 
                print(comp_price)
                
                comp_price = int(comp_price.split('₽')[0].split('\\')[0])
                break
            except:
                try:
                    comp_price = soup.findAll('div', class_='priceBlockPriceWrap--G4F0p priceBlockPriceWrapWallet--rjb9S')[0].get_text() 
                    print(comp_price.split('₽')[0].split()[0] + comp_price.split('₽')[0].split()[1])

                    comp_price = int(comp_price.split('₽')[0].split()[0] + comp_price.split('₽')[0].split()[1])
                    print(comp_price)
                    break
                except:
                    trying += 1
                    if trying == 5:
                        comp_price = 1000000000
                        break

                #         raise Exception(
                #             'ВБ сломался'
                #         )
                
        print(f'{comp_price=}')
        if comp_price <= price:
            answer = answer + f'{name} {url}\nПо цене {comp_price}\n'

    driver.quit()

    return answer
from selenium import webdriver
import os
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import json
import time
import schedule
from random import randrange
from mail import send_email

chrome_options = Options()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)

uname = os.environ.get("USERNAME")
pw = os.environ.get("PASSWD")


def auto_temp():
    print ('Sending temperature')

    #login phase
    driver.get('https://tts.sutd.edu.sg')
    driver.find_element_by_name('ctl00$pgContent1$uiLoginid')
    un = driver.find_element_by_name('ctl00$pgContent1$uiLoginid')
    un.send_keys(uname)
    pwf = driver.find_element_by_name('ctl00$pgContent1$uiPassword')
    pwf.send_keys(pw)
    driver.find_element_by_name('ctl00$pgContent1$btnLogin').click()

    #move to directory
    driver.find_element_by_xpath('//a[text()="Temperature Taking"]').click()
    time.sleep(0.1)

    #put in details
    driver.switch_to.window(driver.window_handles[1])
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'pgContent1_uiTemperature')))
    sel = select.Select(driver.find_element_by_id('pgContent1_uiTemperature'))
    sel.select_by_visible_text('Less than or equal to 37.6°C')
    driver.find_element_by_name('ctl00$pgContent1$btnSave').click()

    #send email
    send_email()
    
    #exit
    driver.quit()

schedule.every().day.at("10:00").do(auto_temp)
schedule.every().day.at("17:00").do(auto_temp)

if __name__ == "__main__":
    while True:
        print('Running')
        schedule.run_pending()
        time.sleep(10)
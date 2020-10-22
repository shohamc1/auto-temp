# -*- coding: utf-8 -*-
from selenium.webdriver.support import select
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common import exceptions
import os
import json
import time
from mail import send_email

def auto_temp():
    uname = os.environ.get("USERNAME")
    pw = os.environ.get("PASSWD")

    CHROMEDRIVER_PATH = "/app/.chromedriver/bin/chromedriver"
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("--headless")
    chrome_bin = os.environ.get("GOOGLE_CHROME_BIN", "chromedriver")
    chrome_options.binary_location = chrome_bin
    driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)

    # Login phase
    driver.get('https://tts.sutd.edu.sg')
    time.sleep(0.1)
    driver.find_element_by_name('ctl00$pgContent1$uiLoginid')
    un = driver.find_element_by_name('ctl00$pgContent1$uiLoginid')
    un.send_keys(uname)
    pwf = driver.find_element_by_name('ctl00$pgContent1$uiPassword')
    pwf.send_keys(pw)
    driver.find_element_by_name('ctl00$pgContent1$btnLogin').click()
    time.sleep(0.1)

    # Move into directory
    driver.find_element_by_xpath('//a[text()="Temperature Taking"]').click()
    time.sleep(0.1)

    # Insert details
    driver.switch_to.window(driver.window_handles[1])
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'pgContent1_uiTemperature')))
    sel = select.Select(driver.find_element_by_id('pgContent1_uiTemperature'))
    sel.select_by_visible_text('Less than or equal to 37.6°C')
    driver.find_element_by_name('ctl00$pgContent1$btnSave').click()
    time.sleep(0.1)

    #exit
    driver.quit()

def daily_dec():
    uname = os.environ.get("USERNAME")
    pw = os.environ.get("PASSWD")

    CHROMEDRIVER_PATH = "/app/.chromedriver/bin/chromedriver"
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("--headless")
    chrome_bin = os.environ.get("GOOGLE_CHROME_BIN", "chromedriver")
    chrome_options.binary_location = chrome_bin
    driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)

    # Login phase
    driver.get('https://tts.sutd.edu.sg')
    time.sleep(0.1)
    driver.find_element_by_name('ctl00$pgContent1$uiLoginid')
    un = driver.find_element_by_name('ctl00$pgContent1$uiLoginid')
    un.send_keys(uname)
    pwf = driver.find_element_by_name('ctl00$pgContent1$uiPassword')
    pwf.send_keys(pw)
    driver.find_element_by_name('ctl00$pgContent1$btnLogin').click()
    time.sleep(0.1)

    # Move into directory
    driver.find_element_by_xpath('//a[text()="Daily Declaration"]').click()
    time.sleep(0.1)

    # Insert details
    driver.switch_to.window(driver.window_handles[1])
    driver.find_element_by_name('ctl00$pgContent1$Notice').click()
    driver.find_element_by_id('pgContent1_rbVisitOtherCountryNo').click()
    driver.find_element_by_id('pgContent1_rbNoticeNo').click()
    driver.find_element_by_id('pgContent1_rbContactNo').click()
    driver.find_element_by_id('pgContent1_rbMCNo').click()
    driver.find_element_by_id('pgContent1_btnSave').click()
    time.sleep(0.1)

    driver.quit() 

def handle_stale(func):
    '''Used to rerun specific function for 5 times if element has gone stale / cannot be found'''
    isStale = True
    while isStale:
        i = 1
        try:
            func()
            isStale = False
        except Exception as e:
            i+=1
            print(f"Failed to declare / record temperature!, {e}")
            print(f"Retrying... Attempt {i}")
            if i >= 5:
                print(f"Failed to declare / record temperature!, {e}. Attempt {i}")
                send_email(isSuccessful=False)
                isStale = False

def temp_and_dec():
    handle_stale(auto_temp)
    handle_stale(daily_dec)
    send_email()

def temp_only():
    handle_stale(auto_temp)
    send_email()

if __name__ == "__main__":
    temp_and_dec()

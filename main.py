from selenium.webdriver.support import select
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
import json
import time

with open('info.json') as f:
    info = json.load(f)
    uname = info['uname']
    pw = info['pw']
    brow = info['browser']

dir_path = os.path.dirname(os.path.realpath(__file__))

if brow == "firefox":
    driver = webdriver.Firefox(executable_path=(dir_path + '\geckodriver.exe'))
elif brow == "chrome":
    driver = webdriver.Chrome(executable_path=(dir_path + '\chromedriver.exe'))
else:
    print('browser tag invalid')

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

#exit
driver.quit()
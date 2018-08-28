import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import time
import pandas as pd
from pull_excel import loadPandasDf
import random
from selenium.webdriver.common.by import By
df = loadPandasDf()

browser = webdriver.Chrome()

username = 'skmenon@college.harvard.edu'
password = '######'

# TEST

browser.get('https://portal.my.harvard.edu/psp/hrvihprd/EMPLOYEE/EMPL/h/?tab=HU_CLASS_SEARCH')
if browser.title == 'HarvardKey Login':
    user = browser.find_element_by_name(username)
    user.send_keys('skmenon@college.harvard.edu')
    pw = browser.find_element_by_name('password')
    pw.send_keys(password)
    pw.send_keys(Keys.RETURN)
time.sleep(3)


search_bar = browser.find_element_by_id('IS_SCL_SearchTxt')
search_bar.send_keys(str(160758) + Keys.RETURN)

# Click top element
browser.find_element_by_xpath("//div[contains(@class, 'isSCL_ResultItem')]").click()

# ids = browser.find_elements_by_xpath('//*[@id]')

# Course Title
browser.find_element_by_class_name('isSCL_RBC').text # TITLE
# FAS or other
browser.find_element_by_class_name('isSCL_RBDP').text
# Prof
browser.find_element_by_class_name('isSCL_RBI').text
# FAS
browser.find_element_by_class_name('isSCL_RBDP').text
# Catagory
browser.find_element_by_class_name('isSCL_RBS').text
# Semester
browser.find_element_by_class_name('isSCL_RBT').text
# term
browser.find_element_by_class_name('isSCL_Session').text
# description
browser.find_element_by_class_name('isSCL_RBD').text
 # Time
browser.find_element_by_class_name('isSCL_RBSET').text
# location
browser.find_element_by_class_name('isSCL_LBLOC').text.split('\n')[0]
# GMaps link
browser.find_element_by_xpath("//div[contains(@class, 'isSCL_LBLOC')]//a[@tile='View walking directions on Google Maps']").get_attribute('href')
# Day of week:
browser.find_element_by_xpath("//li[@class='selected']").text
# Q Guide Score
[x.text for x in browser.find_elements_by_xpath("//div[contains(@data-label, 'Overall:')]") if len(x.text) > 0][0]

# links = [x.text for x in browser.find_elements_by_tag_name('a')]
# display(links)
# for add in browser.find_elements_by_tag_name('a'):
#     if len(add.text) > 0:
#         print("{0} text, tag name: {1}".format(add.text, add.get_attribute('class')))

# display(links)

def findInfo(courseNum, browser, dict):
    # go to search page
    browser.get('https://portal.my.harvard.edu/psp/hrvihprd/EMPLOYEE/EMPL/h/?tab=HU_CLASS_SEARCH')
    # find search bar
    search_bar = browser.find_element_by_id('IS_SCL_SearchTxt')
    search_bar.send_keys(courseNum + Keys.RETURN)
    # click top result
    browser.find_element_by_xpath("//div[contains(@class, 'isSCL_ResultItem')]").click()
    # Search for relevant info and add to dictionary
    # Prof
    dict['Prof'].append(browser.find_element_by_class_name('isSCL_RBI').text)
    # FAS
    dict['Prof'].append(browser.find_element_by_class_name('isSCL_RBDP').text)
    # Semester
    dict['Semester'].append(browser.find_element_by_class_name('isSCL_RBT').text)
    # description
    dict['Description'].append(browser.find_element_by_class_name('isSCL_RBD').text)
     # Time
    dict['Time'].append(browser.find_element_by_class_name('isSCL_RBSET').text)
    # location
    dict['Location'].append(browser.find_element_by_class_name('isSCL_LBLOC').text.split('\n')[0])
    # GMaps link
    dict['Google Maps'].append(browser.find_element_by_xpath("//div[contains(@class, 'isSCL_LBLOC')]//a[@tile='View walking directions on Google Maps']").get_attribute('href'))
    # Day of week:
    dict['Day of Week'].append(browser.find_element_by_xpath("//li[@class='selected']").text)
    # Q Guide Score
    dict['Q Guide Score'].append([x.text for x in browser.find_elements_by_xpath("//div[contains(@data-label, 'Overall:')]") if len(x.text) > 0][0])



for ii in ids:
    print(ii.tag_name)
    # ii.get_attribute('id')

# New Page, Scrape Data

browser = webdriver.Chrome()

addnRows = {'Description': [], 'Time':[], 'Location':[], 'Google Maps':[],
            'Day of Week':[], 'Q Guide Score':[], 'Prof': [], 'Semester':[]}

for courseNum in df['Course #']:
    time.sleep(2 + random.uniform(0.2, 3.5))
    findInfo(courseNum, browser, addnRows)


# TODO: figure out how to select first link or something

browser.quit()

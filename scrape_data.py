import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
from pull_excel import loadPandasDf
import random
df = loadPandasDf()
from selenium.common.exceptions import TimeoutException, UnexpectedAlertPresentException
from collections import OrderedDict

browser = webdriver.Chrome()
browser.quit()
username = 'skmenon@college.harvard.edu'
password = '######'

# TEST


browser.get('https://portal.my.harvard.edu/psp/hrvihprd/EMPLOYEE/EMPL/h/?tab=HU_CLASS_SEARCH')
if browser.title == 'HarvardKey Login':
    user = browser.find_element_by_name('username')
    user.send_keys('skmenon@college.harvard.edu')
    pw = browser.find_element_by_name('password')
    pw.send_keys(password)
    pw.send_keys(Keys.RETURN)
time.sleep(3)

def makeStr(lst):
    return " ".join(OrderedDict.fromkeys(lst))

search_bar = browser.find_element_by_id('IS_SCL_SearchTxt')
search_bar.send_keys(str(127050) + Keys.RETURN)

# Click top element
browser.find_element_by_xpath("//div[contains(@class, 'isSCL_ResultItem')]").click()
browser.find_element_by_xpath("//*[contains(@class,'isSCL_ResultItem')]").click()
browser.find_element_by_xpath("//*[contains(concat(' ', @class, ' '), ' isSCL_ResultItem ')]").click()

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
# Day of week: #TODO: multiple days of the week
makeStr([x.text for x in browser.find_elements_by_xpath("//li[@class='selected']") if len(x.text) > 0])
x = ''
try:
    days = WebDriverWait(browser, 20).until(EC.presence_of_all_elements_located((By.XPATH, "//li[@class='selected']")))
    x = makeStr([x.text for x in days if len(x.text) > 0])
except:
    x = '-1'
x
# Q Guide Score
[x.text for x in browser.find_elements_by_xpath("//div[contains(@data-label, 'Overall:')]") if len(x.text) > 0][0]

# links = [x.text for x in browser.find_elements_by_tag_name('a')]
# display(links)
# for add in browser.find_elements_by_tag_name('a'):
#     if len(add.text) > 0:
#         print("{0} text, tag name: {1}".format(add.text, add.get_attribute('class')))

# display(links)

# try:
#     lightBox = WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[contains(@class,'isSCL_ResultItem')]")))
# except TimeoutException:

def retry(courseNum, browser, dict):
    browser.refresh()
    findInfo(courseNum, browser, dict)

def findInfo(courseNum, browser, dict):
    browser.get('https://portal.my.harvard.edu/psp/hrvihprd/EMPLOYEE/EMPL/h/?tab=HU_CLASS_SEARCH')
    search_bar = WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.ID, 'IS_SCL_SearchTxt')))
        # find search bar
        # search_bar = browser.find_element_by_id('IS_SCL_SearchTxt')
    search_bar.send_keys(courseNum + Keys.RETURN)
    # click top result
    try:
        lightBox = WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[contains(concat(' ', @class, ' '), ' isSCL_ResultItem ')]")))
        lightBox.click()
    except UnexpectedAlertPresentException:
        WebDriverWait(browser, 4).until(EC.alert_is_present())
        alert = browser.switch_to.alert
        alert.accept()
        return retry(courseNum, browser, dict)
    except TimeoutException:
        print('timed out -- bad courseNum: {0}'.format(courseNum))
        return(-1)
    except:
        lightBox = WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[contains(concat(' ', @class, ' '), ' isSCL_LBSecComp ')]")))
        lightBox.click()
    # Search for relevant info and add to dictionary
    try:
        # Prof
        dict['Prof'].append(browser.find_element_by_class_name('isSCL_RBI').text)
    except:
        return(-1)
    # FAS
    dict['Prof'].append(browser.find_element_by_class_name('isSCL_RBDP').text)
    # Semester
    dict['Semester'].append(browser.find_element_by_class_name('isSCL_RBT').text)
    # description
    dict['Description'].append(browser.find_element_by_class_name('isSCL_RBD').text)
     # Time
    dict['Time'].append(browser.find_element_by_class_name('isSCL_RBSET').text)
    # location
    location = WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'isSCL_LBLOC')))
    dict['Location'].append(location.text.split('\n')[0])
    # GMaps link
    gMaps = WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'isSCL_LBLOC')]//a[@tile='View walking directions on Google Maps']")))
    dict['Google Maps'].append(gMaps.get_attribute('href'))
    # Day of week:
    try:
        days = WebDriverWait(browser, 20).until(EC.presence_of_all_elements_located((By.XPATH, "//li[@class='selected']")))
        days = makeStr([x.text for x in days if len(x.text) > 0])
        print('days: {0}, courseNum: {1}'.format(days, courseNum))
        dict['Day of Week'].append(days)
    except TimeoutException:
        dict['Day of Week'].append('-1')
    # Q Guide Score
    try:
        qGuide = WebDriverWait(browser, 20).until(EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@data-label, 'Overall:')]")))
        dict['Q Guide Score'].append([x.text for x in qGuide if len(x.text) > 0][0])
    except:
        dict['Q Guide Score'].append('-1')
    return(0)

def boot():
    browser = webdriver.Chrome()
    browser.get('https://portal.my.harvard.edu/psp/hrvihprd/EMPLOYEE/EMPL/h/?tab=HU_CLASS_SEARCH')
    title = WebDriverWait(browser, 20).until(EC.title_is('HarvardKey Login'))
    user = WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.NAME, 'username')))
    pw = WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.NAME, 'password')))
    user.send_keys(username)
    pw.send_keys(password)
    pw.send_keys(Keys.RETURN)
    return browser

# for ii in ids:
#     print(ii.tag_name)
    # ii.get_attribute('id')

# New Browser



# initialize



browser = boot()

addnRows = {'Description': [], 'Time':[], 'Location':[], 'Google Maps':[],
            'Day of Week':[], 'Q Guide Score':[], 'Prof': [], 'Semester':[]}

# df.index[df['Course #'] == '203876'].tolist()
# df['Title'][75]

rec = {'Bad CourseNums': []}
for courseNum in df['Course #']:
    time.sleep(2 + random.uniform(0.2, 3.5))
    if findInfo(courseNum, browser, addnRows) == -1:
        rec['Bad CourseNums'].append(courseNum)
display(rec)
display(addnRows)

len(addnRows['Semester'])

addnRows['Prof'] = [x for x in addnRows['Prof'] if x != 'FAS']

display(addnRows)

browser.quit()

import datetime
import os
import time

from dateutil import parser
from kiteconnect import KiteConnect, KiteTicker
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import pandas as pd
import urllib.parse as urlparse


class ZerodhaAccessToken:
    def __init__(self, api_key, api_secret, password, zerodha_id, pin):
        self.apiKey          = api_key
        self.apiSecret       = api_secret
        self.accountUserName = zerodha_id
        self.accountPassword = password
        self.securityPin     = int(pin)
        #self.lastlogintime   = last_login_time
        #self.lastaccesstoken = last_access_token
        #self.access_token    = self.getaccesstoken()
        

    def generate_access_token(self, login_url):

        try:
            #chrome_driver_path =   r'/usr/bin/chromedriver'.format(os.getcwd())
            
            options = webdriver.ChromeOptions()
           
            options.add_argument('--no-sandbox')
            options.add_argument('--headless')
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            #options.add_argument("--remote-debugging-port=9222")

            ## chrome driver object
            driver = webdriver.Chrome(options=options)
            
            ## load the url into chrome
            driver.get(login_url)

            ## wait to load the site
            wait = WebDriverWait(driver, 20)
            #time.sleep(5)

            ## Find User Id field and set user id
            wait.until(EC.presence_of_element_located((By.XPATH, '//input[@type="text"]')))\
                .send_keys(self.accountUserName)

            ## Find password field and set user password
            wait.until(EC.presence_of_element_located((By.XPATH, '//input[@type="password"]')))\
                .send_keys(self.accountPassword)

            ## Find submit button and click
            wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@type="submit"]')))\
                .submit()
            
            ## Find pin field and set  pin value
            time.sleep(2)
            wait.until(EC.presence_of_element_located((By.XPATH, '//input[@type="password"]'))).click()
            driver.find_element_by_xpath('//input[@type="password"]').send_keys(self.securityPin)

            ## Final Submit
            wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@type="submit"]'))).submit()

            ## wait for redirection
            wait.until(EC.url_contains('status=success'))

            ## get the token url after success
            tokenurl = driver.current_url
            parsed = urlparse.urlparse(tokenurl)
            driver.close()
            return urlparse.parse_qs(parsed.query)['request_token'][0]

        except Exception as ex:
            print(ex)
            raise

    def getaccesstoken(self):
        
        try:
            kite = KiteConnect(api_key = self.apiKey)
            #check  if the token already exists
            #self.lastlogintime = pd.to_datetime(self.lastlogintime)
            #if self.lastlogintime.date() == datetime.datetime.now().date() and self.lastlogintime.time() > datetime.time(8,0,0):
            #    print('token exists',self.accountUserName)
            #    request_token = self.lastaccesstoken
            #    return request_token
            #else:
                #generating new token
            request_token = self.generate_access_token(kite.login_url())

            data = kite.generate_session(request_token, api_secret= self.apiSecret)

            access_token = data['access_token'] 

            return access_token

        except Exception as ex:
            print(ex)
            raise

